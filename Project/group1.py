#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 23:00:33 2021

@author: bkille
"""
import random


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


#### Devin's functioning consecutive_k.
def is_consecutive_k(input_list, k, stone):
  # Your code goes here
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

### Group containing Josue, Devin, Marvyn
def student_eval(board, stone):
    """ returns something """

    if winner_stone(board, stone):
        return 10
    if winner_stone(board, other_stone(stone)):
        return -10

    #### use the diagonals to check, and use consecutive
    #### use the verticals to check, and use consecutive

    #### horizontal checks
    for curr_row in board:
        if is_consecutive_k(curr_row, 4, stone):
            return 8 #### placeholder, will add the open_k and halfopen_k check later
        if is_consecutive_k(curr_row, 3, stone):
            return 6
        if is_consecutive_k(curr_row, 2, stone):
            return 4
        if is_consecutive_k(curr_row, 1, stone):
            return 2

    #### vertical checks
    for i in range(len(board[0])):
        curr_vert = []
        #### creates a list with the vertical elements
        for curr_horz in board:
            curr_vert.append(curr_horz[i])

        if is_consecutive_k(curr_vert, 4, stone):
            return 8 #### placeholder, will add the open_k and halfopen_k check later
        if is_consecutive_k(curr_vert, 3, stone):
            return 6
        if is_consecutive_k(curr_vert, 2, stone):
            return 4
        if is_consecutive_k(curr_vert, 1, stone):
            return 2

    #### down_diag checks
    for i in range(len(board[0])):
        curr_diag = get_downdiag(board, 0, i)

        if is_consecutive_k(curr_diag, 4, stone):
            return 8 #### placeholder, will add the open_k and halfopen_k check later
        if is_consecutive_k(curr_diag, 3, stone):
            return 6
        if is_consecutive_k(curr_diag, 2, stone):
            return 4
        if is_consecutive_k(curr_diag, 1, stone):
            return 2

    for i in range(len(board)):
        curr_diag = get_downdiag(board, i, 0)

        if is_consecutive_k(curr_diag, 4, stone):
            return 8 #### placeholder, will add the open_k and halfopen_k check later
        if is_consecutive_k(curr_diag, 3, stone):
            return 6
        if is_consecutive_k(curr_diag, 2, stone):
            return 4
        if is_consecutive_k(curr_diag, 1, stone):
            return 2

    #### up_diag checks
    for i in range(len(board[-1])):
        curr_diag = get_updiag(board, 0, i)

        if is_consecutive_k(curr_diag, 4, stone):
            return 8 #### placeholder, will add the open_k and halfopen_k check later
        if is_consecutive_k(curr_diag, 3, stone):
            return 6
        if is_consecutive_k(curr_diag, 2, stone):
            return 4
        if is_consecutive_k(curr_diag, 1, stone):
            return 2

    for i in range(len(board)):
        curr_diag = get_downdiag(board, i, 0)

        if is_consecutive_k(curr_diag, 4, stone):
            return 8 #### placeholder, will add the open_k and halfopen_k check later
        if is_consecutive_k(curr_diag, 3, stone):
            return 6
        if is_consecutive_k(curr_diag, 2, stone):
            return 4
        if is_consecutive_k(curr_diag, 1, stone):
            return 2


    return random.random() # Replace this!
    #### No, I don't think I will