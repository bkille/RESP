#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 23:03:19 2021

@author: bkille
"""


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

def student_eval(board, stone):
    probability = 0
    #Determines if anyone won a row
    for row in board:
      if row_winner(row) == stone:
        probability = 10
        break
      elif row_winner(row) != stone:
        probability = -10
        break
    #Determines if anyone won a column
    for col_idx in range(len(board)):
      if column_winner(board, col_idx) == stone:
        probability = 10
        break
      elif column_winner(board, col_idx) != stone:
        probability = -10
        break

      if winner_stone(board, stone) == True:
        probability = 10
      elif winner_stone(board, stone) == False:
        probability = -10

    return probability # Replace this!