#!/usr/bin/env python
# coding: utf-8

# In[15]:


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


# In[14]:

def get_downdiag(ttt_board, row_idx, col_idx): # Can be top and left sides
    dialist = []
    r = row_idx
    c = col_idx
    while r > -1 and c > -1:
      dialist.append(ttt_board[r][c])
      r -= 1
      c -= 1
    return dialist


# In[11]:


def get_updiag(ttt_board, row_idx, col_idx): #Can be bottom and left sides
    dialist = []
    r = row_idx
    c = col_idx
    while r > -1 and c < len(ttt_board):
      dialist.append(ttt_board[r][c])
      r -= 1
      c += 1
    return dialist


# In[10]:


def get_column(ttt_board, col_idx):
  coll = len(ttt_board)
  collist = []
  for c in range(0,coll):
    collist.append(ttt_board[c][col_idx])
  return collist


# In[9]:


def consecutive_five(input_list, stone):
    for i in range(len(input_list)):
      check = 0
      if input_list[i] == stone:
        check = 0
        o = i
        while o < len(input_list) and input_list[o] == stone:
          check = check + 1
          o += 1
      if check >= 5:
        return True
    return False


# In[8]:


def connect_four(input_list, stone):
    for i in range(len(input_list)):
      check = 1
      if input_list[i] == stone:
        check = 0
        o = i
        while o < len(input_list) and input_list[o] == stone:
          check = check + 1
          o += 1
      if check >= 4:
        return True
    return False


# In[5]:


def rowpoints(input_list, stone,opponent):  #This will return how many consecutive stones there are for the stone given
    points = 10
    for i in range(len(input_list)):
      if input_list[i] == stone:
          ##if i-1 > -1 and input_list[i-1] == "-":
            ##points = points + 10
        if i-1 > -1 and input_list[i-1] == stone:
            points = points + 100
          ##elif i+1 < len(input_list) and input_list[i+1] == "-":
            ##points = points + 10
        if i+1 < len(input_list) and input_list[i+1] == stone:
          points = points + 100
        elif i-1 > -1 and i+1 < len(input_list) and (input_list[i-1] == opponent or input_list[i+1] == opponent):
            points = points - points
    return points


# In[6]:


def get_leftconsecutive(row,stone,stone_idx):
  concount = 0
  while stone_idx > -1 and row[stone_idx] == stone:
    concount +=1
    stone_idx -= 1
  return concount


# In[7]:


def get_rightconsecutive(row,stone,stone_idx):
  concount = 0
  while stone_idx < len(row) and row[stone_idx] == stone:
    concount +=1
    stone_idx += 1
  return concount


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
            


# In[34]:


def random_eval(_1, _2):
    return random.random()

def student_eval(board, stone):
  points = 0
  #initializes the stones of each player
  if stone == "X": #Checking which stone the player is
    opponent = "O" #Saying what stone opponent is
  elif stone == "O":  #Checking which stone the player is
    opponent = "X" #Saying what stone opponent is NOTE: I(Ulises) changed the == to = in this line

  n = len(board) #Establishing the n in the nXn board
  
  #Start Top Half
  #checks for a consecutive 5 in a horizontal and vertical orientation
  for r in range(n): #Runs through the rows
    rowlist = [] #This list will store each row
    for c in range(n): #Runs through the each element of column of row index "r"
      rowlist.append(board[r][c]) #Adds the element at (r,c)
    if consecutive_five(rowlist,stone): # If you won then get 1000 points
      points = points + 1000 
      break #Stops for loop
    elif consecutive_five(rowlist,opponent): # If opponent won lose 1000 points
      points = points - 1000 
      break #Stops for loop
    collist = get_column(board, r) # Get list of column at the index of r
    if consecutive_five(collist,stone): # If you won then get 1000 points
      points = points + 1000 
    elif  consecutive_five(collist,opponent): # If opponent won then get 1000 points
      points = points - 1000 

  #checks for a consecutive 5 in a diagonal orientation (bottom left to top right)
  for r in range(n): #Starts at 0 through length of the board
    for c in range(n-1,-1,-1): #Starts at the bottom of the row and works towards the top
      updiag = get_updiag(board,r,c)  
      if consecutive_five(updiag,stone): #Check to see if you won
        points = points + 1000 
      elif consecutive_five(updiag,opponent): #Check to see if opponent won
        points = points - 1000 

  #checks for a consecutive 5 in a diagonal orientation (top left to bottom right)
  for r in range(n): #Starts at zero goes to length of the board
   for c in range(n): #Starts at zero goes to length of the board
     downdiag = get_downdiag(board,n-1,n-1) #Gets a downward diagonal starting at (r,c)
     if consecutive_five(downdiag,stone): 
       points = points + 1000 
     elif consecutive_five(downdiag,opponent): 
       points = points - 1000 
       
  #End Top Half
  #Start Looking for consecutive 4
  for r in range(n): #Exact same as the Entire Top Half
    rowlist = []
    for c in range(n):
      rowlist.append(board[r][c])
    if connect_four(rowlist,stone): # If you won then get 1000 points
      points = points + 1000
    elif connect_four(rowlist,opponent): #Is the opponent one away from winning?
      points = points + 1000 # --> a high number will prompt the bot to minimize the opponent's chances
    collist = get_column(board, r) # Get list of column at the index of r
    if connect_four(collist,stone): 
      points = points + 1000
    elif  connect_four(collist,opponent): 
      points = points + 1000 
    
  for r in range(n):
    for c in range(n-1,-1,-1):
      updiag = get_updiag(board,r,c)
      if connect_four(updiag,stone):
        points = points + 1000
      elif connect_four(updiag,opponent): #Is the opponent one away from winning?
        points = points + 1000 #STOP THE OPPONENT
  for r in range(n):
   for c in range(n):
     downdiag = get_downdiag(board,n-1,n-1)
     if connect_four(downdiag,stone):
       points = points + 1000
     elif connect_four(downdiag,opponent): 
       points = points + 1000 

  #Stop looking for 4's
  #End Checking to see if you won or lost

  
  if points != 1000: # 1000 points mean that there is a winner and a loser so no need to check the board anymore
      for r in range(n): #Runs from 0 to length of the board
        rowlist = []
        for c in range(n): #Runs from 0 to length of the board
          rowlist.append(board[r][c]) #Adds element to the list of the elements in the row
        points = points + rowpoints(rowlist,stone,opponent) #Starts to see how many points are in that row and adds them
        collist = get_column(board, r)
         
        points = points + rowpoints(collist,stone,opponent)
        for i in range(n):
          if rowlist[i] == stone:
            lefthalf = 0
            righthalf = 0
            if i - 1 > -1 and rowlist[i-1] == stone:
              lefthalf = get_leftconsecutive(rowlist,stone,i-1)
            elif i + 1 < n and rowlist[i+1] == stone:
              righthalf = get_rightconsecutive(rowlist,stone,i+1)
            if lefthalf + righthalf >= 4:
              points = points + 1000
            if points >= 1000:
              return points
          elif rowlist[i] == stone:  
            lefthalf = 0
            righthalf = 0
            if i - 1 > -1 and rowlist[i-1] == opponent:
              lefthalf = get_leftconsecutive(rowlist,opponent,i-1)
            elif i + 1 < n and rowlist[i+1] == opponent:
              righthalf = get_rightconsecutive(rowlist,opponent,i+1)
            if (lefthalf + righthalf) >= 4:
              points = points + 1000
            if points >= 1000:
              return points
          ### Checking Columns for 
          for i in range(n):
            if collist[i] == stone:
              lefthalf = 0
              righthalf = 0
              if i - 1 > -1 and collist[i-1] == stone:
                lefthalf = get_leftconsecutive(collist,stone,i-1)
              elif i + 1 < n and collist[i+1] == stone:
                righthalf = get_rightconsecutive(collist,stone,i+1)
              if (lefthalf + righthalf) >= 4:
                points = points + 1000
              if points >= 1000:
                return points
            elif collist[i] == stone:  
              lefthalf = 0
              righthalf = 0
              if i - 1 > -1 and collist[i-1] == opponent:
                lefthalf = get_leftconsecutive(collist,opponent,i-1)
              elif i + 1 < n and rowlist[i+1] == opponent:
                righthalf = get_rightconsecutive(collist,opponent,i+1)
              if (lefthalf + righthalf) >= 4:
                points = points + 1000
              if points >= 1000:
                return points
      for r in range(n):
        for c in range(n-1,-1,-1):
          updiag = get_updiag(board,r,c)    
        points = points + rowpoints(updiag,stone,opponent)
      for r in range(n):
        for c in range(n):
          downdiag = get_downdiag(board,n-1,n-1)
        points = points + rowpoints(downdiag,stone,opponent)    
  return points


# In[35]:

# In[12]:



