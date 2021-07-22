#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 23:04:53 2021

@author: bkille
"""
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

def get_updiag(ttt_board, row_idx, col_idx): #Can be bottom and left sides
    dialist = []
    r = row_idx
    c = col_idx
    while r > -1 and c < len(ttt_board):
      dialist.append(ttt_board[r][c])
      r -= 1
      c += 1
    return dialist

def get_downdiag(ttt_board, row_idx, col_idx): # Can be top and left sides
    dialist = []
    r = row_idx
    c = col_idx
    while r > -1 and c > -1:
      dialist.append(ttt_board[r][c])
      r -= 1
      c -= 1
    return dialist

def get_column(ttt_board, col_idx):
  coll = len(ttt_board)
  collist = []
  for c in range(0,coll):
    collist.append(ttt_board[c][col_idx])
  return collist

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

def rowpoints(input_list, stone,opponent):  #This will return how many consecutive stones there are for the stone given
    points = 0
    for i in range(len(input_list)):
      if input_list[i] == stone:
          if i-1 > -1 and input_list[i-1] == "-":
            points = points + 10
          elif i+1 < len(input_list) and (input_list[i+1] == "-" or input_list[i+1] == stone):
            points = points + 10
          elif i-1 > -1 and i+1 < len(input_list) and input_list[i-1] == opponent and input_list[i+1] == opponent:
            points = points - points
    return points

def student_eval(board, stone):
  points = 0
  if stone == "X": #Checking which stone the player is
    opponent = "O" #Saying what stone opponent is
  elif stone == "O":  #Checking which stone the player is
    opponent = "X" #Saying what stone opponent is NOTE: I(Ulises) changed the == to = in this line
  k = len(board) #Establishing the n in the nXn board
  rowlist = []
  for r in range(k):
    for c in range(k):
      rowlist.append(board[r][c])
    if consecutive_five(rowlist,stone): # If you won then get 1000 points
      points = points + 1000
      break
    elif consecutive_five(rowlist,opponent): # If opponent won lose 1000 points
      points = points + 1000
      break
    collist = get_column(board, r) # Get list of column at the index of r
    if consecutive_five(collist,stone): # If you won then get 1000 points
      points = points + 1000
    elif  consecutive_five(collist,opponent): # If opponent won then get 1000 points
      points = points - 1000
  for r in range(k):
    for c in range(k-1,-1,-1):
      updiag = get_updiag(board,r,c)
      if consecutive_five(updiag,stone):
        points = points + 1000
      elif consecutive_five(updiag,opponent):
        points = points - 1000
  for r in range(k):
   for c in range(k):
     downdiag = get_downdiag(board,k-1,k-1)
     if consecutive_five(downdiag,stone):
       points = points + 1000
     elif consecutive_five(downdiag,opponent):
       points = points - 1000
  rowlist = []
  for r in range(k):
    for c in range(k):
      rowlist.append(board[r][c])
    if connect_four(rowlist,stone): # If you won then get 1000 points
      points = points + 1000
      break
    elif connect_four(rowlist,opponent): # If opponent won lose 1000 points
      points = points + 1000
      break
    collist = get_column(board, r) # Get list of column at the index of r
    if connect_four(collist,stone): # If you won then get 1000 points
      points = points + 1000
    elif  connect_four(collist,opponent): # If opponent won then get 1000 points
      points = points - 1000
  for r in range(k):
    for c in range(k-1,-1,-1):
      updiag = get_updiag(board,r,c)
      if connect_four(updiag,stone):
        points = points + 1000
      elif connect_four(updiag,opponent):
        points = points - 1000
  for r in range(k):
   for c in range(k):
     downdiag = get_downdiag(board,k-1,k-1)
     if connect_four(downdiag,stone):
       points = points + 1000
     elif connect_four(downdiag,opponent):
       points = points - 1000
  if points != 1000: # 1000 points mean that there is a winner and a loser so no need to check the board anymore
      for r in range(k):
        for c in range(k):
          rowlist.append(board[r][c])
        points = points + rowpoints(rowlist,stone,opponent)
        collist = get_column(board, r)
        points = points + rowpoints(collist,stone,opponent)
      for r in range(k):
        for c in range(k-1,-1,-1):
          updiag = get_updiag(board,r,c)
          points = points + rowpoints(updiag,stone,opponent)
      for r in range(k):
        for c in range(k):
          downdiag = get_downdiag(board,k-1,k-1)
        points = points + rowpoints(downdiag,stone,opponent)
  return points # Replace this!