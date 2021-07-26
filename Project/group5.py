#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from termcolor import cprint
from kille import Strategy, print_board, complete_board, other_stone, play_game
from functools import partial
import numpy as np

def other_stone(stone):
    return "X" if stone == "O" else "O"

def get_random_board(n, turn_count=None):
    board = np.array([["-"]*n for _ in range(n)])
    moves = random.randint(1, n*n/2) if not turn_count else turn_count
    stone = "X"
    for _ in range(moves):
        row_idx = col_idx = -1
        while row_idx < 0 and board[row_idx][col_idx] != "-":
            row_idx = random.randint(0, n-1)
            col_idx = random.randint(0, n-1)
        board[row_idx][col_idx] = stone
        stone = other_stone(stone)
    if complete_board(board):
        board = get_random_board(n)
    return board


# In[ ]:


# In[ ]:
# =============================================================================
# All of your helper functions go here!
def check_col(board, char):
  char_won = False
  length = len(board)
  for i in range(length):
    char_count = 0
    for j in range(length):
      if board[j][i] == char:
        char_count = char_count + 1
      else:
        char_count = 0
    if char_count == 5:
      char_won = True
  return char_won

def check_row(board, char):
  char_won = False
  length = len(board)
  for i in range(length):
    char_count = 0
    for j in range(length):
      if board[i][j] == char:
        char_count = char_count + 1
      else:
        char_count = 0

    if char_count == 5:
      char_won = True
  return char_won


def check_diagonal_up_down(board, char):
  char_won = False
  length = len(board)
  row = 0
  col = 0
  char_count = 0
  while row < length and col < length:
    if board[row][col] == char:
      char_count = char_count + 1
    row = row + 1
    col = col + 1
    if char_count == 5:
      char_won = True
  return char_won

def check_diagonal_down_up(board, char):
  char_won = False
  length = len(board)
  row = length - 1
  col = 0
  char_count = 0
  while row >= 0 and col < length:
    if board[row][col] == char:
      char_count = char_count + 1
    row = row - 1
    col = col + 1
    if char_count == 5:
      char_won = True
  return char_won

def game_state(board):
  x_won = False
  o_won = False
  x_won_row = check_row(board, "X")
  x_won_col = check_col(board, "X")
  x_won_updown_diag = check_diagonal_up_down(board, "X")
  x_won_downup_diag = check_diagonal_down_up(board, "X")
  o_won_row = check_row(board, "O")
  o_won_col = check_col(board, "O")
  o_won_updown_diag = check_diagonal_up_down(board, "O")
  o_won_downup_diag = check_diagonal_down_up(board, "O")

  if x_won_row or x_won_col or  x_won_updown_diag or x_won_downup_diag:
    x_won = True
  if o_won_row or o_won_col or o_won_updown_diag or o_won_downup_diag:
    o_won = True

  if x_won == False and o_won == False:
    #print("returning None")
    return None
  if x_won == True and o_won == True:
    #print("returning ERROR")
    return "ERROR"
  if x_won == True:
    #print("return X")
    return "X"
  if o_won == True:
    #print("return O")
    return "O"
    
def consecutive_k(input_list, k, stone):
    length = len(input_list)
    stone_count = 0
    for i in range(length):
      if input_list[i] == stone:
        stone_count = stone_count + 1
      else:
        stone_count = 0
      if stone_count == k :
        return True
    return False

def get_column(board, col_idx):
  col_list = list()
  for i in range(len(board)):
    col_list.append(board[i][col_idx])
  return col_list


def is_empty(board):
  for i in range(len(board)):
    for j in range(len(board)):
      if board[i][j] != "-":
        return False
  return True

def get_downdiag(board, row_idx, col_idx):
    return [board[row_idx + i][col_idx + i] for i in range(min(len(board) - row_idx, len(board) - col_idx))]

def get_updiag(board, row_idx, col_idx):
  diag = list()
  row = row_idx
  i = 0
  while row >= 0:
    diag.append(board[row_idx-i][col_idx-1+i])
    i = i + 1
    row = row - 1
  return diag

# =============================================================================


# In[1]:


def student_eval(board, stone):
  length = len(board)
  stone_prob = 0
  student_prob = 0
  #print("given stone", other_stone(stone))
  student_stone = ""
  if stone == "X":
    student_stone = "O"
  else:
    student_stone = "X"
  if game_state(board) == stone:
      return 999
  if game_state(board) == student_stone:
      return -999
  if is_empty(board):
    return 0
  #print(student_stone, "'s turn")

  for i in range(length):
    row = board[i]
    col = get_column(board, i)
    for j in range(length):
      hor_slice = list(row[j:j+5])
      vert_slice = list(col[j:j+5])
      down_diag = get_downdiag(board, i, j)
      #up_diag = get_updiag(board, i, j)
      #up_diag_slice = list(up_diag[j:j+5])
      down_diag_slice = list(down_diag[j:j+5])

      #stone in horizontal slice
      if (len(hor_slice) == 5) and (stone in hor_slice) and (student_stone not in hor_slice):
        stone_count = hor_slice.count(stone)
        if stone_count == 1:
           stone_prob = stone_prob + 10

        if stone_count == 2:
           stone_prob = stone_prob + 20
           if consecutive_k(hor_slice, 2, stone):
             stone_prob = stone_prob + 40
        
        if stone_count == 3:
           stone_prob = stone_prob + 30
           if consecutive_k(hor_slice, 3, stone):
             stone_prob = stone_prob + 60

        if stone_count == 4:
           stone_prob = stone_prob + 40 + 999
#----------------------------------------------------------------
      #stone in vertical slice
      if (len(vert_slice) == 5) and (stone in vert_slice) and (student_stone not in vert_slice):
        stone_count = vert_slice.count(stone)
        if stone_count == 1:
           stone_prob = stone_prob + 10

        if stone_count == 2:
           stone_prob = stone_prob + 20
           if consecutive_k(vert_slice, 2, stone):
             stone_prob = stone_prob + 40
        
        if stone_count == 3:
           stone_prob = stone_prob + 30
           if consecutive_k(vert_slice, 3, stone):
             stone_prob = stone_prob + 60

        if stone_count == 4:
           stone_prob = stone_prob + 40 + 999
#----------------------------------------------------------------
      #stone in down diagonal
      if (len(down_diag_slice) == 5) and (stone in down_diag_slice) and (student_stone not in down_diag_slice):
        stone_count = down_diag_slice.count(stone)
        if stone_count == 1:
           stone_prob = stone_prob + 10

        if stone_count == 2:
           stone_prob = stone_prob + 20
           if consecutive_k(down_diag_slice, 2, stone):
             stone_prob = stone_prob + 40
        
        if stone_count == 3:
           stone_prob = stone_prob + 30
           if consecutive_k(down_diag_slice, 3, stone):
             stone_prob = stone_prob + 60

        if stone_count == 4:
           stone_prob = stone_prob + 40 + 999
        
#----------------------------------------------------------------
      # #stone in up diagonal
      # if (len(up_diag_slice) == 5) and (stone in up_diag_slice) and (student_stone not in up_diag_slice):
      #   stone_count = up_diag_slice.count(stone)
      #   if stone_count == 1:
      #      stone_prob = stone_prob + 10

      #   if stone_count == 2:
      #      stone_prob = stone_prob + 20
      #      if consecutive_k(up_diag_slice, 2, stone):
      #        stone_prob = stone_prob + 40
        
      #   if stone_count == 3:
      #      stone_prob = stone_prob + 30
      #      if consecutive_k(up_diag_slice, 3, stone):
      #        stone_prob = stone_prob + 60

      #   if stone_count == 4:
      #      stone_prob = stone_prob + 40 + 999
#----------------------------------------------------------------
      #student_stone in horizontal slice
      if (len(hor_slice) == 5) and (student_stone in hor_slice) and (stone not in hor_slice):
        student_stone_count = hor_slice.count(student_stone)
        if student_stone_count == 1:
           student_prob = student_prob + 10

        if student_stone_count == 2:
           student_prob = student_prob + 20
           if consecutive_k(hor_slice, 2, student_stone):
             student_prob = student_prob + 40
        
        if student_stone_count == 3:
           student_prob = student_prob + 30
           if consecutive_k(hor_slice, 3, student_stone):
             student_prob = student_prob + 60

        if student_stone_count == 4:
           student_prob = student_prob + 40 + (999**2) #guarantees absolute win
#-----------------------------------------------------------------
      #student_stone in vertical
      if (len(vert_slice) == 5) and (student_stone in vert_slice) and (stone not in vert_slice):
        student_stone_count = vert_slice.count(student_stone)
        if student_stone_count == 1:
           student_prob = student_prob + 10

        if student_stone_count == 2:
           student_prob = stone_prob + 20
           if consecutive_k(vert_slice, 2, student_stone):
             student_prob = student_prob + 40
        
        if student_stone_count == 3:
           student_prob = student_prob + 30
           if consecutive_k(vert_slice, 3, student_stone):
             student_prob = student_prob + 60

        if student_stone_count == 4:
           student_prob = student_prob + 40 + (999**2) 
#-------------------------------------------------------------------
      #student_stone in down diagonal
      if (len(down_diag_slice) == 5) and (student_stone in down_diag_slice) and (stone not in down_diag_slice):
        student_stone_count = down_diag_slice.count(student_stone)
        if student_stone_count == 1:
           student_prob = student_prob + 10

        if student_stone_count == 2:
           student_prob = stone_prob + 20
           if consecutive_k(down_diag_slice, 2, student_stone):
             student_prob = student_prob + 40 + 200
        
        if student_stone_count == 3:
           student_prob = student_prob + 30
           if consecutive_k(down_diag_slice, 3, student_stone):
             student_prob = student_prob + 60 + 300

        if student_stone_count == 4:
           student_prob = student_prob + 40 + (999**2)
#--------------------------------------------------------------------
      #student_stone in up diagonal
      # if (len(up_diag_slice) == 5) and (student_stone in up_diag_slice) and (stone not in up_diag_slice):
      #   student_stone_count = up_diag_slice.count(student_stone)
      #   if student_stone_count == 1:
      #      student_prob = student_prob + 10

      #   if student_stone_count == 2:
      #      student_prob = stone_prob + 20
      #      if consecutive_k(up_diag_slice, 2, student_stone):
      #        student_prob = student_prob + 40 + 200
        
      #   if student_stone_count == 3:
      #      student_prob = student_prob + 30
      #      if consecutive_k(up_diag_slice, 3, student_stone):
      #        student_prob = student_prob + 60 + 300

      #   if student_stone_count == 4:
      #      student_prob = student_prob + 40 + (999**2)

  if student_prob > stone_prob:
    final_prob = student_prob - stone_prob
  if student_prob < stone_prob:
    final_prob = stone_prob - student_prob
  if student_prob == stone_prob:
    final_prob = 0

  #print("final_prob", final_prob)

  return final_prob


# In[2]:


