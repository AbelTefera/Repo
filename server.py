from socket import *
import threading as th
from random import * 
import time

data = [] # element structure ---> [client_id, message]
clients = {} # key ---> client_id, value ---> client_socket
max_id = 1000

IP = '192.168.1.103'
PORT = 23013
msg_len = 100

server = socket(AF_INET, SOCK_STREAM)
server.bind((IP, PORT))
server.listen(5)

def generate_client_id():
  global clients
  global max_id

  client_id = randint(0, max_id)
  while client_id in clients.keys():
    client_id = randint(0, max_id)

  return str(client_id)

def trans_msg(msg):
  msg = msg.decode('utf-8')
  msg = msg.strip()
  return msg

def proc_msg(msg):
  global msg_len
  msg = msg.encode('utf-8')
  msg = msg + ' '.encode('utf-8') * (msg_len - len(msg))
  return msg

def get_client_id(client):
  global clients
  key_ls = list(clients.keys())
  val_ls = list(clients.values())

  return key_ls[val_ls.index(client)]

def get_msg(client_id):
  for i in range(len(data)):
    if data[i][0] == client_id:
      return data.pop(i)[1]
  return 'no msg'
    
def handle_client(client, addr):
  client_id = generate_client_id()
  clients[client_id] = client
  client.send(proc_msg(client_id))

  while True:
    msg = client.recv(msg_len)
    msg = trans_msg(msg)
    if msg == 'read':
      msg = proc_msg(get_msg(client_id)) if data else proc_msg('empty')
      client.send(msg)
    elif msg == 'close':
      clients.pop(client_id)
      print(f'{client_id} closed connection')
      client.close()
      break
    elif msg == 'my_id':
      msg = proc_msg(get_client_id(client))
      client.send(msg)
    elif msg == 'pair':
      if clients and len(clients) >= 2:
        ls_ids = list(clients.keys())
        ls_ids.remove(client_id)
        pair_id = choice(ls_ids)
        pair_id = proc_msg(pair_id)
        client.send(pair_id)
        data.append([trans_msg(pair_id), f'pair_id{client_id}'])
        print(f'msg {client_id} to {pair_id}')
      else:
        ret_msg = 'no pair'
        ret_msg = proc_msg(ret_msg)
        client.send(ret_msg)
    else:
      recv_id = client.recv(msg_len)
      recv_id = trans_msg(recv_id)
      data.append([recv_id, msg])
      print(f'msg: {data[-1][1]}, to: {data[-1][0]}')

    time.sleep(1)


while True:
  (client, addr) = server.accept()
  if client:
    thread = th.Thread(target=handle_client, args=(client, addr))
    thread.start()
