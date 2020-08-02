from pieces import * 

class Board:
  def __init__(self):
    self.tiles = self.create_board() # Tiles from 0 to 63
    self.curr_pl = 'W'

  def create_board(self):
    tiles = [] 
    W, B = 'W', 'B'
    tiles.append(Tile('light', Rook(B)))
    tiles.append(Tile('dark', Knight(B)))
    tiles.append(Tile('light', Bishop(B)))
    tiles.append(Tile('dark', Queen(B)))
    tiles.append(Tile('light', King(B)))
    tiles.append(Tile('dark', Bishop(B)))
    tiles.append(Tile('light', Knight(B)))
    tiles.append(Tile('dark', Rook(B)))
    
    num = 1
    shade = None 
    for i in range(8, 56):
      if i%8 == 0:
        num = 1 if num == 0 else 0
      if (i+num)%2 == 0:
        shade = 'dark'
      else:
        shade = 'light'

      if 8<=i and i<16:
        tiles.append(Tile(shade, Pawn(B)))
      elif 16<=i and i<48:
        tiles.append(Tile(shade))
      elif 48<=i and i<56:
        tiles.append(Tile(shade, Pawn(W)))

    tiles.append(Tile('dark', Rook(W)))
    tiles.append(Tile('light', Knight(W)))
    tiles.append(Tile('dark', Bishop(W)))
    tiles.append(Tile('light', Queen(W)))
    tiles.append(Tile('dark', King(W)))
    tiles.append(Tile('light', Bishop(W)))
    tiles.append(Tile('dark', Knight(W)))
    tiles.append(Tile('light',Rook(W)))

    return tiles 

  def reset(self):
    self.tiles = self.create_board() # Tiles from 0 to 63
    self.curr_pl = 'W'

  def rm_pc_exp(self, pname):
    for tile in self.tiles:
      if tile.piece != None and tile.piece.name != pname:
        tile.piece = None

  def move_valid(self, from_pos, to_pos):
    valid = True
    from_pc = self.tiles[from_pos].piece
    to_pc = self.tiles[to_pos].piece
    # general checks apply to all moves
    if from_pos == to_pos:
      valid = False
    elif from_pc == None:
      valid = False
    elif to_pc != None and to_pc.color == self.curr_pl:
      valid = False
    elif from_pc.color != self.curr_pl:
      valid = False
    elif from_pos<0 or from_pos>63 or to_pos<0 or to_pos>63:
      valid = False
    # checks specific to type of piece
    else:
      valid = from_pc.is_move_legal(from_pos, to_pos, self.tiles) 
    return valid 

  def move(self, from_pos, to_pos):
    valid = self.move_valid(from_pos, to_pos)
    if valid:
      piece = self.tiles[from_pos].piece
      self.tiles[from_pos].piece = None
      self.tiles[to_pos].piece = piece
      self.curr_pl = 'W' if self.curr_pl == 'B' else 'B'
      return True
    
    return False

  def all_possible_moves(self, from_pos):
    moves_pos = []
    for pos in range(len(self.tiles)):
      if self.move_valid(from_pos, pos):
        moves_pos.append(pos)
    return moves_pos


class Tile:
  light_sh = (254, 206, 158)
  dark_sh = (208, 140, 71)

  def __init__(self, shade='light', piece=None):
    self.piece = piece
    if shade == 'dark':
      self.shade = Tile.dark_sh
    elif shade == 'light':
      self.shade = Tile.light_sh

  def piece_img(self):
    if self.piece != None:
      return self.piece.get_img()
 
    
