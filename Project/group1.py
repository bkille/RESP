#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[3]:


#### Bryce provided helper functions

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


# In[4]:


# In[ ]:
# =============================================================================
# All of your helper functions go here!
# =============================================================================

#### Devin's functioning consecutive_k.
def is_consecutive_k(input_list, k, stone):
  ret_bool = False
  counter = 0
  
  for v in input_list:
    if counter != k:
      if v == stone:
        counter += 1
      elif v != stone:
        counter = 0
    

  if counter == k:
    ret_bool = True
  return ret_bool

def max(x, y):
    """ returns maximum """

    if x > y:
        return x
    else:
        return y

def min(x, y):
    """ comment """

    if x < y:
        return x
    else:
        return y


# In[146]:


#### Devin's open_k function
def open_k(input_list, k, stone):
    ret_bool = False
    counter = 0

    for i in range(len(input_list[0:])):
      if counter != k:
        if input_list[i] == stone:
          counter += 1
        elif input_list[i] != stone:
          counter = 0
      else:
        if i-k-1 != -1: 
          if input_list[i-k-1] == "-" and input_list[i] == "-":
          
            ret_bool = True
          else:
        
            counter = 0
        else:
          counter = 0
    '''if counter == k:
      ret_bool = True'''
    
    return ret_bool 

#### Devin's functioning open_k modified to function as a halfopen_k.
def halfopen_k(input_list, k, stone):
    ret_bool = False
    counter = 0

    for i in range(len(input_list[0:])):

        if counter != (k):
            if input_list[i] == stone:
                counter += 1
            elif input_list[i] != stone:
                counter = 0
        else:
            #if i-(k)-1 != -1: 
                if input_list[i-k-1] == "-" or input_list[i] == "-":
          
                    ret_bool = True
                else:
        
                    counter = 0
            #else:
                #counter = 0


    if counter == k:
        
        ret_bool = True
        if input_list[i-k-1] == "-" or input_list[i] == "-":
          
                    ret_bool = True
        else:
        
                    counter = 0
                    ret_bool = False
    
    return ret_bool 

#### improved halfopen_k

def whole_halfopen_k(whole_list, k, stone):
    """ returns True if there exists a halfopen_k somewhere in whole_list """

    for i in range(len(whole_list) - k):
        small_list = whole_list[i :  i + k + 1]

        
        if halfopen_k(small_list, k, stone):
            return True

    return False

def whole_open_k(whole_list, k, stone):
    """ returns True if there exists an open_k somewhere in whole_list """

    for i in range(len(whole_list) - k - 1):
        small_list = whole_list[i :  i + k + 2]


        if open_k(small_list, k, stone):
            return True

    return False


#### Checking functions: the same thing I copy pasted that returns a probability of a list

def get_probablity(curr_list, k, stone, opp_stone):
    """
    list: list to check
    k: consecutive_k to check
    stone: stone to check for

    Returns a number between -10 to 10, with a higher number having a higher probability to win
    """

    to_return = 0

    if stone == opp_stone:
        curr_list = remove_opp_spaces(curr_list, k, stone)

    if is_consecutive_k(curr_list, k, stone) and whole_halfopen_k(curr_list, k, stone):
        to_return = k * 2

        if is_consecutive_k(curr_list, k, other_stone(stone)):
            if not whole_halfopen_k(curr_list, k, other_stone(stone)):
                to_return = (k * 2) + 1
    
    #if (open_k(remove_opp_spaces))
    
    return to_return

def remove_opp_spaces(curr_list, k, stone):
    if k == 1:
        return curr_list
    else:
        is_valid = False
        count = 0
        for i in range(len(curr_list)):

            if is_valid:
                count = count + 1
                if curr_list[i] == other_stone(stone):
                    is_valid = False
                    count = 0
            elif curr_list[i] == stone:
                is_valid = True
                start = i
                count = count + 1
            

            if count == k:
                if curr_list[i] == "-":
                    count = 0
                    is_valid = False
            if count == k:
                for j in range(start, i+1):
                    curr_list[j] = stone 
                count = 0
                is_valid = False
        
        return curr_list

### test remove_opp_spaces

# In[232]:


####### REVERT TO THIS EDIT 7/24/2021 11:49PM

def student_eval(board, stone):
    """ 
    Returns a theoretical probability of stone winning
    the provided board in Connect 5, where the higher
    probability is a better win chance 
    """

    if winner_stone(board, stone):
        return 100
    if winner_stone(board, other_stone(stone)):
        return -100
    if not winner_stone(board, stone) and not winner_stone(board, other_stone(stone)) and complete_board(board):
        return 0

    max_return = -13
    max_other_stone = -13

    #### use the diagonals to check, and use consecutive
    #### use the verticals to check, and use consecutive

    #### horizontal checks ####################################################################################################################################
    for curr_list in board:

        curr_row = []
        for i in curr_list:
            curr_row.append(i)
        
        if whole_open_k(curr_row, 3, other_stone(stone)) or whole_halfopen_k(curr_row, 4, other_stone(stone)):
            return -100
        if whole_open_k(curr_row, 4, stone):
            max_return = 11
        
        max_return = max(max_return, get_probablity(curr_row, 4, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_row, 4, other_stone(stone), other_stone(stone)) + 4)

        max_return = max(max_return, get_probablity(curr_row, 3, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_row, 3, other_stone(stone), other_stone(stone)) + 4) 

        max_return = max(max_return, get_probablity(curr_row, 2, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_row, 2, other_stone(stone), other_stone(stone)) + 4)
            

        max_return = max(max_return, get_probablity(curr_row, 1, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_row, 1, other_stone(stone), other_stone(stone)) + 4)

    #### vertical checks ##########################################################################################################################################
    for i in range(len(board[0])):
        curr_vert = []
        #### creates a list with the vertical elements
        for curr_horz in board:
            curr_vert.append(curr_horz[i])

        if whole_open_k(curr_vert, 3, other_stone(stone)) or whole_halfopen_k(curr_vert, 4, other_stone(stone)):
            return -100
        if whole_open_k(curr_vert, 4, stone):
            max_return = 11
        
        max_return = max(max_return, get_probablity(curr_vert, 4, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_vert, 4, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_vert, 3, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_vert, 3, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_vert, 2, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_vert, 2, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_vert, 1, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_vert, 1, other_stone(stone), other_stone(stone)) + 4)
    
    #### down_diag checks ##################################################################################################################################
    for i in range(len(board[0])):
        curr_diag = get_downdiag(board, 0, i)

        if whole_open_k(curr_diag, 3, other_stone(stone)) or whole_halfopen_k(curr_diag, 4, other_stone(stone)):
            return -100
        if whole_open_k(curr_diag, 4, stone):
            max_return = 11

        max_return = max(max_return, get_probablity(curr_diag, 4, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
        
        max_return = max(max_return, get_probablity(curr_diag, 3, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_diag, 2, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_diag, 1, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
    
    for i in range(len(board)):
        curr_diag = get_downdiag(board, i, 0)

        if whole_open_k(curr_diag, 3, other_stone(stone)) or whole_halfopen_k(curr_diag, 4, other_stone(stone)):
            return -100
        if whole_open_k(curr_diag, 4, stone):
            max_return = 11

        max_return = max(max_return, get_probablity(curr_diag, 4, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
        
        max_return = max(max_return, get_probablity(curr_diag, 3, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_diag, 2, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_diag, 1, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)

    #### up_diag checks ##################################################################################################################################
    for i in range(len(board[-1])):
        curr_diag = get_updiag(board, (len(board)) - 1, i)

        if whole_open_k(curr_diag, 3, other_stone(stone)) or whole_halfopen_k(curr_diag, 4, other_stone(stone)):
            return -10
        if whole_open_k(curr_diag, 4, stone):
            max_return = 11

        max_return = max(max_return, get_probablity(curr_diag, 4, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
        
        max_return = max(max_return, get_probablity(curr_diag, 3, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_diag, 2, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_diag, 1, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)

    for i in range(len(board)):
        curr_diag = get_updiag(board, i, 0)

        if whole_open_k(curr_diag, 3, other_stone(stone)) or whole_halfopen_k(curr_diag, 4, other_stone(stone)):
            return -100
        if whole_open_k(curr_diag, 4, stone):
            max_return = 11

        max_return = max(max_return, get_probablity(curr_diag, 4, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
        
        max_return = max(max_return, get_probablity(curr_diag, 3, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_diag, 2, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)
            
        max_return = max(max_return, get_probablity(curr_diag, 1, stone, other_stone(stone)) - 1)
        max_other_stone = max(max_other_stone, get_probablity(curr_diag, 4, other_stone(stone), other_stone(stone)) + 4)

    if max_return == -13:
        return 0
        
    if max_other_stone >= max_return:
        return -1 * max_other_stone
    if max_other_stone == max_return:
        return 0

    if True:
        return max_return

