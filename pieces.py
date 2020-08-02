import os

import moves

class Piece:
  def __init__(self, color):
    self.color = color

  def is_move_legal(self, from_pos, to_pos, tiles):
    return True

class King(Piece):
  name = 'K'
  
  def __init__(self, color):
    super().__init__(color)
 
  def get_img(self):
    return f'{self.color}_{King.name}.png'

  def is_move_legal(self, from_pos, to_pos, tiles): 
    legal = False
    if abs(from_pos-to_pos) == 1 or abs(from_pos-to_pos) == 8:
      legal = True
    elif abs(from_pos-to_pos) == 9 or abs(from_pos-to_pos) == 7:
      legal = True

    return legal


class Queen(Piece):
  name = 'Q'

  def __init__(self, color):
    super().__init__(color)

  def get_img(self):
    return f'{self.color}_{Queen.name}.png'

  def is_move_legal(self, from_pos, to_pos, tiles): 
    return ( moves.legal_diag_move(from_pos, to_pos, tiles) or
              moves.legal_horz_vert_move(from_pos, to_pos, tiles) )
    

class Bishop(Piece):
  name = 'B'

  def __init__(self, color):
    super().__init__(color) 

  def get_img(self):
    return f'{self.color}_{Bishop.name}.png'
    
  def piece_in_way(from_pos, to_pos, tiles):
    itr = 7 if (from_pos-to_pos)%7 == 0 else 9 # check for whether (from_pos-to_pos)% 7 or 9 == 0
                                               # is done in is_move_legal()
    itr = -1*itr if from_pos > to_pos else itr
    for i in range(from_pos, to_pos, itr):
      if tiles[i].piece != None and tiles[from_pos].shade == tiles[i].shade:
        return True
    return False
    
  def is_move_legal(self, from_pos, to_pos, tiles):
    legal = True
    if Bishop.piece_in_way(from_pos, to_pos, tiles):
      legal = False
    
    return moves.legal_diag_move(from_pos, to_pos, tiles)


class Knight(Piece):
  name = 'N'
  
  def __init__(self, color):
    super().__init__(color)

  def get_img(self):
    return f'{self.color}_{Knight.name}.png'

  def is_move_legal(self, from_pos, to_pos, tiles):
    legal = True
    if (not abs(from_pos-to_pos) == 6 and not abs(from_pos-to_pos) == 10 
      and not abs(from_pos-to_pos) == 15 and not abs(from_pos-to_pos) == 17):
      legal = False

    return legal


class Rook(Piece):
  name = 'R'
  
  def __init__(self, color):
    super().__init__(color)

  def get_img(self):
    return f'{self.color}_{Rook.name}.png' 

  def is_move_legal(self, from_pos, to_pos, tiles): 
    return moves.legal_horz_vert_move(from_pos, to_pos, tiles)

  
class Pawn(Piece):
  name = 'P'

  def __init__(self, color):
    super().__init__(color)
    
  def get_img(self):
    return f'{self.color}_{Pawn.name}.png'

  # TODO add all other rules
  def is_move_legal(self, from_pos, to_pos, tiles):
    if self.color == 'W':
      return from_pos-to_pos == 8
    elif self.color == 'B':
      return from_pos-to_pos == -8


