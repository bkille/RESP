#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 23:07:07 2021

@author: bkille
"""


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
    if char_count == length:
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

    if char_count == length:
      char_won = True
  return char_won


def check_diagonal_up_down(board, char):
  char_won = False
  length = len(board)
  row = 0
  col = 0
  char_count = 0
  # if board[row][col] == char:
  #   char_count = char_count + 1
  while row < length and col < length:
    if board[row][col] == char:
      #print("row", row, "col", col)
      char_count = char_count + 1
    row = row + 1
    col = col + 1
    #print("char_count", char_count)
    if char_count == length:
      char_won = True
  return char_won

def check_diagonal_down_up(board, char):
  char_won = False
  length = len(board)
  row = length - 1
  col = 0
  char_count = 0
  #char_count = char_count + 1
  while row >= 0 and col < length:
    if board[row][col] == char:
      #print("row", row, "col", col)
      char_count = char_count + 1
    row = row - 1
    col = col + 1
    if char_count == length:
      char_won = True
    #print("char_count", char_count)
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
    return None
  if x_won == True and o_won == True:
    return "ERROR"
  if x_won == True:
    return "X"
  if o_won == True:
    return "O"


def student_eval(board, stone):
  if stone == "X":
    if game_state(board) == stone:
      return 999
    if game_state(board) == "O":
      return -999
  if stone == "O":
    if game_state(board) == stone:
      return 999
    if game_state(board) == "X":
      return -999

  length = len(board)
  is_empty = True
  for i in range(length):
    for j in range(length):
      if board[i][j] != "" or board[i][j] != "-":
        is_empty = False
  return 0