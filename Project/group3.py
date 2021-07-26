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
def consecutive_n(input_list, n, stone):
    for i in range(len(input_list)):
      check = 0
      if input_list[i] == stone:
        check = 0
        o = i
        while o < len(input_list) and input_list[o] == stone:
          check = check + 1
          o = o + 1
      if check >= n:
        return True
    return False
def get_column(ttt_board, col_idx):
  coll = len(ttt_board)
  collist = []
  for c in range(0,coll):
    collist.append(ttt_board[c][col_idx])
  return collist
def get_downdiag(board, row_idx, col_idx):
    return [board[row_idx + i][col_idx + i] for i in range(min(len(board) - row_idx, len(board) - col_idx))]
def get_updiag(board, row_idx, col_idx):
    return [board[row_idx - i][col_idx + i] for i in range(min(row_idx + 1, len(board) - col_idx))]
def halfopen_n(input_list, k, stone):
    for i in range(len(input_list)):
      if input_list[i] == stone:
        new_list = input_list[i:i+k]
        if consecutive_n(new_list,k,stone):
          if i-1 > -1 and i+k < len(input_list) and input_list[i-1] == "-":
            if input_list[i+k] == "-":
              return False
            return True
          elif i-1 > -1 and i+k < len(input_list) and input_list[i+k] == "-":
            if input_list[i-1] == "-":
              return False
            return True 
    return False
def oppoblock_n(input_list, k, stone,oppo):
    for i in range(len(input_list)):
      if input_list[i] == stone:
        new_list = input_list[i:i+k]
        if consecutive_n(new_list,k,stone):
          if i-1 > -1 and i+k < len(input_list) and input_list[i-1] == oppo:
            if input_list[i+k] == "-":
              return False
            return True
          elif i-1 > -1 and i+k < len(input_list) and input_list[i+k] == oppo:
            if input_list[i-1] == "-":
              return False
            return True 
    return False


# In[ ]:


def student_eval(board, stone):
    stone = other_stone(stone)
    opponent = other_stone(stone)
    points = 0
    n = len(board)
    scores = {1: 10, 2: 25, 3: 50, 4: 100, 5: 250}
    for row in board:
      row = list(row)
      for i in range(1,6):
        for o in range(len(row)-4):
          rowsect = row[o:o+5]
          if consecutive_n(rowsect,i,stone):
            if rowsect.count("O") == 0:
              points = points - scores[i]
          if consecutive_n(rowsect,i,opponent):
            if rowsect.count("X") == 0:
              points = points + scores[i]
    for r in range(n):
      col = get_column(board,r)
      for i in range(1,6):
        for o in range(len(col)-4):
          colsect = col[o:o+5]
          if consecutive_n(colsect,i,stone):
            points = points - scores[i]
          if consecutive_n(colsect,i,opponent):
            points = points + scores[i]
    for r in range(n):
      for c in range(n):
        downdiag = get_downdiag(board,r,c)
        if len(downdiag) < 5:
          for i in range (1,len(downdiag)):
            for o in range(len(downdiag)):
              if consecutive_n(downdiag,i,stone):
                if downdiag.count("O") == 0:
                  points = points - scores[i]
              if consecutive_n(downdiag,i,opponent):
                if downdiag.count("X") == 0:
                  points = points + scores[i]
        else:
          for i in range (1,6):
            for o in range(len(downdiag)-4):
              if consecutive_n(downdiag,i,stone):
                if downdiag.count("O") == 0:
                  points = points - scores[i]
              if consecutive_n(downdiag,i,opponent):
                if downdiag.count("X") == 0 and oppoblock_n(downdiag,4,opponent,stone):
                  points = points - 100000
                elif downdiag.count("X") == 0:
                  points = points + scores[i]
    for r in range(n):
      for c in range(n-1,-1,-1):
        updiag = get_updiag(board,r,c)
        if len(updiag) < 5:
          for i in range (1,len(updiag)):
            for o in range(len(updiag)):
              if consecutive_n(updiag,i,stone):
                if updiag.count("O") == 0:
                  points = points - scores[i]
              if consecutive_n(updiag,i,opponent):
                if updiag.count("X") == 0:
                  points = points + scores[i]
        else:
          for i in range (1,6):
            for o in range(len(updiag)-4):
              if consecutive_n(updiag,i,stone):
                if updiag.count("O") == 0:
                  points = points - scores[i]
              if consecutive_n(updiag,i,opponent):
                if updiag.count("X") == 1 and oppoblock_n(updiag,4,opponent,"X"):
                  points = points - 100000
                elif updiag.count("X") == 0:
                  points = points + scores[i]  
    return points


