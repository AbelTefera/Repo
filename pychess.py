#!/usr/bin/python3
import pygame, sys, os

import board
import client

pygame.init()
scr_w, scr_h = (700, 700)
screen = pygame.display.set_mode((scr_w, scr_h))

board = board.Board()
state = 'menu'
states = ['menu', 'sg_game', 'mult_game', 'sg_end_game', 'mult_end_game']
tile_sz = 60
board_w = 8*tile_sz
board_h = board_w
board_st_x = scr_w/2 - board_w/2
board_st_y = scr_h/2 - board_h/2

mult_curr_pl = None


### Event Handling ###
def handle_keydown(event):
  global state
  global board
  global mult_curr_pl
  if event.key == pygame.K_q:
    if state == 'mult_game':
      client.send('close')
    sys.exit()
  if state == 'menu':
    if event.key == pygame.K_s:
      state = 'sg_game'
    if event.key == pygame.K_m:
      state = 'mult_game'
      client.setup()
      if int(client.client_id) < int(client.pair_id):
        mult_curr_pl = 'W'
      else:
        mult_curr_pl = 'B'
  elif state == 'sg_game':
    if event.key == pygame.K_r:
      board.reset()
    elif event.key == pygame.K_s:
      board.rm_pc_exp('Q')

def handle_keyup(event):
  pass

# TODO refactor
def get_board_pos(x, y):
  global tile_sz
  global board_st_x, board_st_y
  global board_w, board_h
  pos = -1
  if board_st_x<=x and x<=(board_st_x+board_w) and board_st_y<=y and y<=(board_st_y+board_h):
    x-=board_st_x
    y-=board_st_y
    pos = int(x/tile_sz + 1) + 8*int(y/tile_sz) - 1
  return pos if 0<=pos and pos<=63 else -1

ms_slc_1 = None # saves first mouse click pos as tile num
ms_slc_2 = None # saves second mouse click pos as tile num
def handle_mousedown(event):
  global state
  global ms_slc_1, ms_slc_2
  global board
  global mult_curr_pl
  x, y = pygame.mouse.get_pos()
  
  # TODO bug when selecting outside the range of the chess board
  if state == 'sg_game': 
    pos = get_board_pos(x, y)
    if ms_slc_1 == None and ms_slc_2 == None: 
      ms_slc_1 = pos if pos != -1 else None # can't be -1 
    elif ms_slc_1 != None and ms_slc_2 == None:
      ms_slc_2 = pos # could be -1 
      if pos != -1:
        board.move(ms_slc_1, ms_slc_2)
      ms_slc_1, ms_slc_2 = None, None
    elif ms_slc_1 != None and ms_slc_2 != None:
      ms_slc_1, ms_slc_2 = None, None
    elif ms_slc_1 == None and ms_slc_2 != None: # should never happen this would be an err
      ms_slc_1, ms_slc_2 = None, None

  ### Refactor ###
  if state == 'mult_game':
    if mult_curr_pl == board.curr_pl:
      pos = get_board_pos(x, y)
      if ms_slc_1 == None and ms_slc_2 == None: 
        ms_slc_1 = pos if pos != -1 else None # can't be -1 
      elif ms_slc_1 != None and ms_slc_2 == None:
        ms_slc_2 = pos # could be -1 
        if pos != -1:
          if board.move(ms_slc_1, ms_slc_2):
            client.send(f'move {ms_slc_1} {ms_slc_2}')
        ms_slc_1, ms_slc_2 = None, None
      elif ms_slc_1 != None and ms_slc_2 != None:
        ms_slc_1, ms_slc_2 = None, None
      elif ms_slc_1 == None and ms_slc_2 != None: # should never happen this would be an err
        ms_slc_1, ms_slc_2 = None, None
    else:
      msg = client.send('read')
      msg = msg.split()
      if msg[0] == 'move':
        board.move(int(msg[1]), int(msg[2]))

def handle_mouseup(event):
  pass

### Draw Screen ###
def draw_img(rel_path, x, y):
  img_path = os.path.join(os.getcwd(), 'res', rel_path)
  img = pygame.image.load(img_path)
  screen.blit(img, (int(x), int(y)))

def draw_menu():
  pass

def pos_to_cords(pos):
  global tile_sz
  global board_st_x, board_st_y
  num = pos%8
  x = num * tile_sz + board_st_x
  y = int(pos/8) * tile_sz + board_st_y
  return (x, y)

def draw_board():
  global board
  global scr_w, scr_h
  global board_w, board_h
  global tile_sz
  global board_st_x, board_st_y
  global ms_slc_1, ms_slc_2
  x = board_st_x
  y = board_st_y
  for i in range(len(board.tiles)):
    pygame.draw.rect(screen, board.tiles[i].shade, (int(x), int(y), tile_sz, tile_sz))
    # draw piece img
    if board.tiles[i].piece != None:
      img_path = f'{board.tiles[i].piece_img()}'
      draw_img(img_path, x, y)
    x += tile_sz
    if ((i+1)%8 == 0):
      x = scr_w/2 - board_w/2
      y += tile_sz
      
  if ms_slc_1 != None: 
    # draws red dot on currently selected tile
    img_path = 'red_dot.png'
    x, y = pos_to_cords(ms_slc_1)
    draw_img(img_path, x, y)
    # draws green dot on all possible moves
    img_path = 'green_dot.png'
    moves_pos = board.all_possible_moves(ms_slc_1)
    if moves_pos:
      moves_cords = [pos_to_cords(pos) for pos in moves_pos]
      for cords in moves_cords:
        draw_img(img_path, cords[0], cords[1])
  
def draw_screen():
  global state
  global screen
  global scr_w, scr_h
  global tile_sz
  if state == 'menu':
    draw_menu()
  elif state == 'sg_game':
    pygame.draw.rect(screen, (255, 255, 255) if board.curr_pl == 'W' else (0, 0, 0), (0, scr_w//2-tile_sz//2, tile_sz, tile_sz))
    draw_board()
  elif state == 'mult_game':
    if client.pair_id != None:
      pygame.draw.rect(screen, (255, 255, 255) if board.curr_pl == 'W' else (0, 0, 0), (0, scr_w//2-tile_sz//2, tile_sz, tile_sz))
      draw_board()
  

### Main ###
def run():
  while(True):
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        handle_keydown(event) 
      elif event.type == pygame.KEYUP:
        handle_keyup(event)
      elif event.type == pygame.MOUSEBUTTONDOWN:
        handle_mousedown(event)
      elif event.type == pygame.MOUSEBUTTONUP:
        handle_mouseup(event)

    screen.fill((0, 0, 0))
    draw_screen()
    pygame.display.flip()


if __name__ == "__main__":
  run()
