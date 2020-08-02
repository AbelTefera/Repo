
def legal_diag_move(from_pos, to_pos, tiles):     
  legal = True                                      
  if not (from_pos-to_pos)%9 == 0 and not (from_pos-to_pos)%7 == 0: 
    legal = False           
  elif tiles[from_pos].shade != tiles[to_pos].shade:         
    legal = False                                       

  return legal

def same_row(from_pos, to_pos):
  same_row = False
  if 0<=from_pos and from_pos<=7 and 0<=to_pos and to_pos<=7:
    same_row = True
  elif 8<=from_pos and from_pos<=15 and 8<=to_pos and to_pos<=15:
    same_row = True
  elif 16<=from_pos and from_pos<=23 and 16<=to_pos and to_pos<=23:
    same_row = True
  elif 24<=from_pos and from_pos<=31 and 24<=to_pos and to_pos<=31:
    same_row = True
  elif 32<=from_pos and from_pos<=39 and 32<=to_pos and to_pos<=39:
    same_row = True
  elif 40<=from_pos and from_pos<=47 and 40<=to_pos and to_pos<=47:
    same_row = True
  elif 48<=from_pos and from_pos<=55 and 48<=to_pos and to_pos<=55:
    same_row = True
  elif 56<=from_pos and from_pos<=63 and 56<=to_pos and to_pos<=63:
    same_row = True
    
  return same_row

def legal_horz_vert_move(from_pos, to_pos, tiles):
  legal = True
  if not (from_pos-to_pos)%8 == 0 and not same_row(from_pos, to_pos):
    legal = False

  return legal
