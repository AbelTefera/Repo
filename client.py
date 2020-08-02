from socket import *
import sys

serverIP = 'abebel.com'
serverPORT = 23013
msg_len = 100

def trans_msg(msg):
  msg = msg.decode('utf-8')
  msg = msg.strip()
  return msg

def proc_msg(msg):
  global msg_len
  msg = msg.encode('utf-8')
  msg = msg + ' '.encode('utf-8') * (msg_len - len(msg))
  return msg

client = socket(AF_INET, SOCK_STREAM)
client_id = None
pair_id = None

def setup():
  global client
  global client_id
  client.connect((serverIP, serverPORT))
  client_id = client.recv(msg_len)
  client_id = trans_msg(client_id)
  while pair_id == None:
    send('pair')
  print(f'my id {client_id}, pair id {pair_id}')
  return client_id

def send(msg):
  global client
  global pair_id
  global client_id
  global serverIP, serverPORT
  global msg_len

  if msg == 'close':
    msg = proc_msg(msg)
    client.send(msg)
    client.close()
    sys.exit()
  elif msg == 'read':
    msg = proc_msg(msg)
    client.send(msg)
    recv_msg = client.recv(msg_len)
    recv_msg = trans_msg(recv_msg) 

    '''
    if recv_msg[:len('pair_id')] == 'pair_id':
      pair_id = recv_msg[len(pair_id):]
    '''

    print(recv_msg)
    return recv_msg
  elif msg == 'my_id':
    msg = proc_msg(msg)
    client.send(msg)
    recv_msg = client.recv(msg_len)
    recv_msg = trans_msg(recv_msg)
    print(f'my id is {recv_msg}')
    return recv_msg
  elif msg == 'pair':
    if not pair_id: 
      msg = proc_msg(msg)
      client.send(msg)
      recv_msg = client.recv(msg_len)
      recv_msg = trans_msg(recv_msg)
      if recv_msg == 'no pair':
        print('no pair')
      else:
        pair_id = recv_msg
    else:
      print(f'already paired to {pair_id}') 
  elif msg == 'pair_id':
    print(f'paired to {pair_id}')
  else:
    if pair_id:
      msg = proc_msg(msg)
      to = pair_id
      to = proc_msg(to)
      client.send(msg)
      client.send(to)
    else:
      print('can\'t send msg if not paired')






