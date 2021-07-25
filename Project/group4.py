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
# =============================================================================
def get_column(board, col_idx):
  col_list = []
  for c in (board):
    col_list.append(c[col_idx])

  return col_list

def consecutive_k(input_list, k, stone):
  rep_counter = 0
  consecutive = False
  for s in input_list:
    if s == stone:
      rep_counter += 1
    else:
      rep_counter = 0
    if rep_counter == k:
      consecutive = True
  return consecutive

def get_updiag(board, row_idx, col_idx):
  diag_list = []
  curr_row = row_idx
  curr_col = col_idx
  stop_row = -1
  stop_col = len(board)

  while (curr_row > stop_row) and (stop_col != curr_col):
    curr_val = board[curr_row][curr_col]
    diag_list.append(curr_val)
    curr_row -= 1
    curr_col += 1
  return diag_list
def get_downdiag(board, row_idx, col_idx):
  diagonal_list = []
  curr_row = row_idx
  curr_col = col_idx
  stop_row = len(board)
  stop_col = len(board)

  while (curr_row != stop_row) and (stop_col != curr_col):
    current_value = board[curr_row][curr_col]
    diagonal_list.append(current_value)
    curr_row += 1
    curr_col += 1
  return diagonal_list


# In[ ]:


def random_eval(_1, _2):
    return random.random()

def student_eval(board, stone):
  rep_score = 0
  for row in board:
    if consecutive_k(row,5,stone):
     rep_score += 5
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,5,stone):
      rep_score += 5
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,5,stone):
      rep_score += 5
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,5,stone):
      rep_score += 5
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,5,stone):
      rep_score += 5
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,5,stone):
      rep_score += 5
  for row in board:
    if consecutive_k(row,4,stone):
     rep_score += 4
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,4,stone):
      rep_score += 4
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,4,stone):
      rep_score += 4
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,4,stone):
      rep_score += 4
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,4,stone):
      rep_score += 4
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,4,stone):
      rep_score += 4
  for row in board:
    if consecutive_k(row,3,stone):
     rep_score += 3
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,3,stone):
      rep_score += 3
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,3,stone):
      rep_score += 3
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,3,stone):
      rep_score += 3
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,3,stone):
      rep_score += 3
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,3,stone):
      rep_score += 3
  for row in board:
    if consecutive_k(row,2,stone):
     rep_score += 2
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,2,stone):
      rep_score += 2
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,2,stone):
      rep_score += 2
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,2,stone):
      rep_score += 2
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,2,stone):
      rep_score += 2
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,2,stone):
      rep_score += 2
  for row in board:
    if consecutive_k(row,1,stone):
     rep_score += 1
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,1,stone):
      rep_score += 1
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,1,stone):
      rep_score += 1
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,1,stone):
      rep_score += 1
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,1,stone):
      rep_score += 1
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,1,stone):
      rep_score += 1
  
  for row in board:
    if consecutive_k(row,5,other_stone(stone)):
     rep_score -= 5
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,5,other_stone(stone)):
      rep_score -= 5
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,5,other_stone(stone)):
      rep_score -= 5
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,5,other_stone(stone)):
      rep_score -= 5
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,5,other_stone(stone)):
      rep_score -= 5
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,5,other_stone(stone)):
      rep_score -= 5
  for row in board:
    if consecutive_k(row,4,other_stone(stone)):
     rep_score -= 4
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,4,other_stone(stone)):
      rep_score -= 4
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,4,other_stone(stone)):
      rep_score -= 4
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,4,other_stone(stone)):
      rep_score -= 4
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,4,other_stone(stone)):
      rep_score -= 4
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,4,other_stone(stone)):
      rep_score -= 4
  for row in board:
    if consecutive_k(row,3,other_stone(stone)):
     rep_score -= 3
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,3,other_stone(stone)):
      rep_score -= 3
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,3,other_stone(stone)):
      rep_score -= 3
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,3,other_stone(stone)):
      rep_score -= 3
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,3,other_stone(stone)):
      rep_score -= 3
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,3,other_stone(stone)):
      rep_score -= 3
  for row in board:
    if consecutive_k(row,2,other_stone(stone)):
     rep_score -= 2
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,2,other_stone(stone)):
      rep_score -= 2
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,2,other_stone(stone)):
      rep_score -= 2
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,2,other_stone(stone)):
      rep_score -= 2
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,2,other_stone(stone)):
      rep_score -= 2
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,2,other_stone(stone)):
      rep_score -= 2
  for row in board:
    if consecutive_k(row,1,other_stone(stone)):
     rep_score -= 1
  for i in range(len(board)):
    column = get_column(board,i)
    if consecutive_k(column,1,other_stone(stone)):
      rep_score -= 1
  for row_idx in range(len(board)):
    up_diagonal1 = get_updiag(board, row_idx, 0)
    if consecutive_k(up_diagonal1,1,other_stone(stone)):
      rep_score -= 1
  for col_idx in range(len(board)):
    up_diagonal2 = get_updiag(board, len(board)-1, col_idx)
    if consecutive_k(up_diagonal2,1,other_stone(stone)):
      rep_score -= 1
  for row_idx in range(len(board)):
    down_diagonal1 = get_downdiag(board, row_idx, 0)
    if consecutive_k(down_diagonal1,1,other_stone(stone)):
      rep_score -= 1
  for col_idx in range(len(board)):
    down_diagonal2 = get_downdiag(board, 0, col_idx)
    if consecutive_k(down_diagonal2,1,other_stone(stone)):
      rep_score -= 1


  #other_stone(stone)
  #less than 5

  return rep_score # Replace this!

