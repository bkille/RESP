#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from termcolor import cprint

def print_board(board, bolded=None):
    """A debugging function to print you board in a pretty way"""
    n = len(board)
    # For every row but the last
    for row_idx, row in enumerate(board[:-1]):
        # Print the row as a string with a line below
        if bolded and row_idx==bolded[0]:
            cprint("|".join(row[:bolded[1]]), None, attrs=["underline"], end='|' if bolded[1] != 0 else '')
            cprint(row[bolded[1]], None, attrs=["underline", "bold"], end='')
            if bolded[1] != len(row) - 1:
                cprint("|" + "|".join(row[bolded[1]+1:]), None, attrs=["underline"], end='')
            print()
        else:
            cprint("|".join(row), None, attrs=["underline"])
    row = board[-1]
    if bolded and bolded[0] == len(board) - 1:
        print("|".join(row[:bolded[1]]), end='|' if bolded[1] != 0 else '')
        cprint(row[bolded[1]], None, attrs=["bold"], end='')
        if bolded[1] != len(row) - 1:
            cprint("|" + "|".join(row[bolded[1]+1:]), None, end='')
        print()
    else:
        print("|".join(row))


def other_stone(stone):
    return "X" if stone == "O" else "O"

def consecutive_k(row, k, stone):
    desired_row = [stone] * k
    return sum(desired_row == row[i:i+k] for i in range(len(row) - k + 1))

def get_downdiag(board, row_idx, col_idx):
    return [board[row_idx + i][col_idx + i] for i in range(min(len(board) - row_idx, len(board) - col_idx))]

def get_updiag(board, row_idx, col_idx):
    return [board[row_idx - i][col_idx + i] for i in range(min(row_idx + 1, len(board) - col_idx))]

def winner_stone(board, stone):
    k_count = 0
    k = 5
    for row in board:
        row = list(row)
        k_count += consecutive_k(row, k, stone)

    for col_idx in range(len(board)):
        bl = [row[col_idx] for row in board]
        k_count += consecutive_k(bl, k, stone)

    for row_idx in range(len(board)):
        bl = get_updiag(board, row_idx, 0)
        k_count += consecutive_k(bl, k, stone)
        bl = get_downdiag(board, row_idx, 0)
        k_count += consecutive_k(bl, k, stone)

    for col_idx in range(len(board[0])):
        bl = get_updiag(board, len(board) - 1, col_idx)
        k_count += consecutive_k(bl, k, stone)
        bl = get_downdiag(board, 0, col_idx)
        k_count += consecutive_k(bl, k, stone)
    
    return k_count > 0

def complete_board(board):
    return winner_stone(board, "X") or winner_stone(board, "O") or not any('-' in row for row in board)


# In[ ]:


import random
import heapq
import numpy as np
from tqdm.notebook import tqdm
import copy

class Strategy:
    def __init__(self, stone, eval_function, max_depth=1):
        self.stone = stone
        self.opponent_stone = other_stone(stone)
        self.max_depth = max_depth
        self.nodes = 0
        self.pruned = 0
        self.eval_function=eval_function 
    
    def alphabeta_search(self, board, depth, stone, alpha, beta):
        if depth == 0 or complete_board(board):
            score = self.eval_function(board, stone)
            score = -score if stone == self.opponent_stone else score
            self.nodes += 1
            return score, (None, None)
        
        row_arr, col_arr = np.where(board == '-')
        open_spaces = list(zip(row_arr, col_arr))
        if stone == self.stone:
            best_score = -np.infty
            best_move = (None, None)
            lop = len(open_spaces)
            c = 0
            for row, col in open_spaces:
                new_board = copy.deepcopy(board)
                new_board[row][col] = stone
                score, move = self.alphabeta_search(new_board, depth-1, other_stone(stone), alpha, beta)
                best_score = max(score, best_score)
                if best_score >= beta:
                    self.pruned += (lop - c)**depth
                    break
                elif best_score > alpha:
                    best_move = (row, col)
                    alpha = best_score
        else:
            best_score = np.infty
            best_move = (None, None)
            lop = len(open_spaces)
            c = 0
            for row, col in open_spaces:
                c += 1
                new_board = copy.deepcopy(board)
                new_board[row][col] = stone
                score, move = self.alphabeta_search(new_board, depth-1, other_stone(stone), alpha, beta)
                best_score = min(score, best_score)
                if best_score <= alpha:
                    self.pruned += (lop - c)**depth
                    break
                elif best_score < beta:
                    best_move = (row, col)
                    beta = best_score
                
        self.nodes += 1
        return best_score, best_move
        
                    
    def get_move(self, board, max_nodes = 100):
        score, move = self.alphabeta_search(board, self.max_depth, self.stone, -np.inf, np.inf)
        return move
            


# In[ ]:


def row_winner(row):
  # return 'O' if O won
  # return 'X' if X won
  # return None if no winner
  # return ERROR if two winners
  ret_str = None
  x_winner = True
  o_winner = True
  for c in row:
    if c != "X":
      x_winner = False
    if c != "O":
      o_winner = False
  #checks and sets return string to appropriate winning character
  if x_winner:
    ret_str = "X"
  if o_winner:
    ret_str = "O"
  
  return ret_str

def column_winner(board, col_idx):
  # Returns the winner of the (col_idx)th column in the board
  ret_str = None
  x_winner = True
  o_winner = True
  
  for row in board:
    c = row[col_idx]
    if c != "X":
      x_winner = False
    if c != "O":
      o_winner = False
  if x_winner:
    ret_str = "X"
  if o_winner:
    ret_str = "O"
  
  return ret_str

def student_consecutive_k(input_list, k, stone):
    # Your code goes here
    counter = 0
    consecutive = False
    for i in input_list:
      if i == stone:
        counter += 1
      if i != stone:
        counter = 0
      if counter == k:
        consecutive = True
        break
    return consecutive

def get_column(board):
  columns = []
  for column_idx in range(len(board)):
    single_column = []
    for row in board:
      single_column.append(row[column_idx])
    columns.append(single_column)
  return columns

def row_probability(board, stone):
  probability = 0
  # Determines row probabilities for given stone
  for row in board:
    # Determines consecutives row probabilities for given stone
    if student_consecutive_k(row, 1, stone):
      probability = 1
    if student_consecutive_k(row, 2, stone):
      probability = 2
    if student_consecutive_k(row, 3, stone):
      probability = 3
    if student_consecutive_k(row, 4, stone):
      probability = 4
    if student_consecutive_k(row, 5, stone):
      probability = 5
  return probability

def column_probability(board, stone):
  probability = 0
  columns = get_column(board)
  for column in columns:
    if student_consecutive_k(column, 1, stone):
      probability = 1
    if student_consecutive_k(column, 2, stone):
      probability = 2
    if student_consecutive_k(column, 3, stone):
      probability = 3
    if student_consecutive_k(column, 4, stone):
      probability = 4
    if student_consecutive_k(column, 5, stone):
      probability = 5
  return probability

def up_diagonal_probability(board, stone):
  probability = 0
  col_idx = 0
  for row_idx in range(len(board)):
    diagonal = get_updiag(board, row_idx, col_idx)
    if student_consecutive_k(diagonal, 1, stone):
      probability = 1
    if student_consecutive_k(diagonal, 2, stone):
      probability = 2
    if student_consecutive_k(diagonal, 3, stone):
      probability = 3
    if student_consecutive_k(diagonal, 4, stone):
      probability = 4
    if student_consecutive_k(diagonal, 5, stone):
      probability = 5
  
  col_idx = 1
  row_index = len(board) -1
  while col_idx < len(board):
    diagonal = get_updiag(board, row_index, col_idx)
    if student_consecutive_k(diagonal, 1, stone):
      probability = 1
    if student_consecutive_k(diagonal, 2, stone):
      probability = 2
    if student_consecutive_k(diagonal, 3, stone):
      probability = 3
    if student_consecutive_k(diagonal, 4, stone):
      probability = 4
    if student_consecutive_k(diagonal, 5, stone):
      probability = 5
    col_idx += 1
  return probability
  
def down_diagonal_probability(board, stone):
  probability = 0
  row_idx = 0
  col_idx = 0
  while col_idx < len(board):
    diagonal = get_downdiag(board, row_idx, col_idx)
    if student_consecutive_k(diagonal, 1, stone):
      probability = 1
    if student_consecutive_k(diagonal, 2, stone):
      probability = 2
    if student_consecutive_k(diagonal, 3, stone):
      probability = 3
    if student_consecutive_k(diagonal, 4, stone):
      probability = 4
    if student_consecutive_k(diagonal, 5, stone):
      probability = 5
    col_idx += 1
  
  row_idx = 1
  col_idx = 0
  while row_idx < len(board):
    diagonal = get_downdiag(board, row_idx, col_idx)
    if student_consecutive_k(diagonal, 1, stone):
      probability = 1
    if student_consecutive_k(diagonal, 2, stone):
      probability = 2
    if student_consecutive_k(diagonal, 3, stone):
      probability = 3
    if student_consecutive_k(diagonal, 4, stone):
      probability = 4
    if student_consecutive_k(diagonal, 5, stone):
      probability = 5
    row_idx += 1
  
  return probability



# In[ ]:


def random_eval(_1, _2):
    return random.random()

# Emily Gianotti, Vivian Le, and Benjamin Martinez 
def student_eval(board, stone):
  
  # Determines row probabilities
  student_row_prob = row_probability(board, stone)
  opponent_row_prob = - (row_probability(board, other_stone(stone)))
  
  # Determines column probabilities
  student_column_prob = column_probability(board, stone)
  opponent_column_prob = - (column_probability(board, other_stone(stone)))

  # Determines up-diagonal probabilities
  student_up_diag_prob = up_diagonal_probability(board, stone)
  opponent_up_diag_prob = - (up_diagonal_probability(board, other_stone(stone)))

  # Determines down-diagonal probabilities
  student_down_diag_prob = down_diagonal_probability(board, stone)
  opponent_down_diag_prob = - (down_diagonal_probability(board, other_stone(stone)))
  
  # Determines if there are any winners  
  if winner_stone(board, stone) == True:
    probability = 5
  elif winner_stone(board, stone) == False:
    probability = -5
  
  # Determines final probability for the board
  probability = 0
  # Compares row probabilites
  if student_row_prob > abs(opponent_row_prob):
    row_prob = student_row_prob
  else:
    row_prob = opponent_row_prob
  # Compares column probabilites
  if student_column_prob > abs(opponent_row_prob):
    column_prob = student_column_prob
  else:
    column_prob = opponent_column_prob
  # Compoares up diagonal probabilities
  if student_up_diag_prob > abs(opponent_up_diag_prob):
    up_diag_prob = student_up_diag_prob
  else:
    up_diag_prob = opponent_up_diag_prob
  # Compares down diagonal probabilities
  if student_down_diag_prob > abs(opponent_down_diag_prob):
    down_diag_prob =  student_down_diag_prob
  else:
    down_diag_prob = opponent_down_diag_prob
  # Compares final row and final column probabilites
  if abs(row_prob) > abs(column_prob):
    prob_1 = row_prob
  else:
    prob_1 = column_prob
  # Compares final diagonal probabilities
  if abs(up_diag_prob) > abs(down_diag_prob):
    prob_2 = up_diag_prob
  else:
    prob_2 = down_diag_prob
  # Compares final probabilities
  if abs(prob_1) > abs(prob_2):
    final_prob = prob_1
  else:
    final_prob = prob_2


  return final_prob # Returns final probability of the board





# In[ ]:





