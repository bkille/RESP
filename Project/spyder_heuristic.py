#!/usr/bin/env python
# coding: utf-8

# In[3]:


from termcolor import cprint

def print_board(board, bolded=None):
    """A debugging function to print you board in a pretty way"""
    n = len(board)
    # For every row but the last
    for row_idx, row in enumerate(board[:-1]):
        # Print the row as a string with a line below
        if bolded and row_idx==bolded[0]:
            cprint("|".join(row[:bolded[1]]) + '|' if bolded[1] != 0 else '', None, attrs=["underline"], end='')
            cprint(row[bolded[1]], "green", attrs=["underline", "bold"], end='')
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

def live_k(row, k, stone):
    consecutive_k = [stone] * k
    if k < 4:
        return sum(consecutive_k in (row[i+j:i+j+k] for j in range(5-k+1)) and row[i:i+5].count('-') == 5-k for i in range(len(row) -  5))
    if k == 4:
        return int("-" + stone*4 + "-" in "".join(row))
    return 0


def dead_k(row, k, stone):
    consecutive_k = [stone] * k
    c = row[:5].count(stone) == k and row[:5].count("-") == 5 - k and row[0] == stone
    c += row[-5:].count(stone) == k and row[-5:].count("-") == 5 - k and row[-1] == stone
    return c + sum(row[i:i+5].count(stone) == k and consecutive_k not in (row[i+j:i+j+k] for j in range(5-k+1)) and row[i:i+5].count('-') == 5-k for i in range(len(row) -  4))

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


def iter_seqs(board):
    for row in board:
        yield list(row)

    for col_idx in range(len(board)):
        yield [row[col_idx] for row in board]

    for row_idx in range(len(board)):
        d = get_updiag(board, row_idx, 0)
        if len(d) >= 5:
            yield d
        d = get_downdiag(board, row_idx, 0)
        if len(d) >= 5:
            yield d

    for col_idx in range(len(board[0])):
        d = get_updiag(board, len(board) - 1, col_idx)
        if len(d) >= 5:
            yield d
        d = get_downdiag(board, 0, col_idx)
        if len(d) >= 5:
            yield d


def complete_board(board):
    return winner_stone(board, "X") or winner_stone(board, "O") or not any('-' in row for row in board)

def isolated(board, row, col):
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x == 0 and y == 0 or (not (0 <= row+x < len(board))) or (not (0 <= col+y < len(board))):
                continue
            try:
                if board[row+x][col+y] != "-":
                    return False
            except:
                pass
    return True
# In[24]:


import random
import heapq
import numpy as np
from tqdm import tqdm
import copy

class Strategy:
    def __init__(self, stone, max_depth=1):
        self.stone = stone
        self.opponent_stone = other_stone(stone)
        self.max_depth = max_depth
        self.nodes = 0
        self.pruned = 0

    def eval_board(self, board, stone):
        max_val = 100000
        op_val = 10000
        retval = 0
        consecutive_5 = 0
        live_dict = {2: 10, 3: 1000, 4: max_val}
        dead_dict = {2: 5, 3: 10, 4: max_val}
        live_count = {2: 0, 3: 0, 4: 0, 5: 0}
        dead_count = {2: 0, 3: 0, 4: 0, 5: 0}
        stone_p = other_stone(stone)
        for seq in iter_seqs(board):
            for k in range(2, 5):
                live_count[k]  += live_k(seq, k, stone)
                dead_count[k] += dead_k(seq, k, stone)
                consecutive_5 += consecutive_k(seq, 5, stone)
        for k in range(2, 5):
            if live_count[k]:
                retval += live_count[k]*live_dict[k]
            if dead_count[k]:
                retval += dead_dict[k]
        #print(live_count, dead_count)
        if consecutive_5:
             return 100000000
        live_dict = {2: 10, 3: 500, 4: op_val}
        dead_dict = {2: 5, 3: 50, 4: op_val / 2}
        live_count = {2: 0, 3: 0, 4: 0, 5: 0}
        dead_count = {2: 0, 3: 0, 4: 0, 5: 0}
        for seq in iter_seqs(board):
            for k in range(2, 5):
                live_count[k]  += live_k(seq, k, stone_p)
                dead_count[k] += dead_k(seq, k, stone_p)
                consecutive_5 += consecutive_k(seq, 5, stone_p)

        for k in range(2, 5):
            if live_count[k]:
                retval -= live_count[k]*live_dict[k]
            if dead_count[k]:
                retval -= dead_dict[k]
        if consecutive_5:
                return -10000000

        return retval

    def minmax_search(self, board, depth, stone, alpha=0, beta=0):
        #print_board(board)
        if depth == 0 or complete_board(board):
            score = self.eval_board(board, stone)
            score = -score if stone == self.opponent_stone else score
            return score, (None, None)

        row_arr, col_arr = np.where(board == '-')
        open_spaces = zip(row_arr, col_arr)

        if stone == self.stone:
            best_score = -np.infty
            best_move = (0,0)
            for row, col in open_spaces:
                new_board = copy.deepcopy(board)
                new_board[row][col] = stone
                score, move = self.minmax_search(new_board, depth-1, other_stone(stone))
                if score >= best_score:
                    best_move = (row, col)
                    best_score = score
        else:
            best_score = np.infty
            best_move = (0,0)
            for row, col in open_spaces:
                new_board = copy.deepcopy(board)
                new_board[row][col] = stone
                score, move = self.minmax_search(new_board, depth-1, other_stone(stone))
                if score <= best_score:
                    best_move = (row, col)
                    best_score = score
        return best_score, best_move


    def alphabeta_search(self, board, depth, stone, alpha, beta):
        if depth == 0 or complete_board(board):
            score = self.eval_board(board, stone)
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
            for row, col in tqdm(open_spaces) if depth == 3 else open_spaces:
                # new_board = copy.deepcopy(board)
                new_board = board
                new_board[row][col] = stone
                tdepth = 1 if isolated(new_board, row, col) else depth
                score, move = self.alphabeta_search(new_board, tdepth-1, other_stone(stone), alpha, beta)
                new_board[row][col] = "-"
                # if depth==3:
                #     print(f"{row},{col} yields {score}, alpha={alpha}, beta={beta}")
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
                # new_board = copy.deepcopy(board)
                new_board = board
                new_board[row][col] = stone
                tdepth = 1 if isolated(new_board, row, col) else depth
                score, move = self.alphabeta_search(new_board, tdepth-1, other_stone(stone), alpha, beta)
                new_board[row][col] = "-"
                best_score = min(score, best_score)
                #print(f"O: New score={score}, Best score={best_score}, alpha={alpha}, beta={beta}")
                if best_score <= alpha:
                    self.pruned += (lop - c)**depth
                    break
                elif best_score < beta:
                    best_move = (row, col)
                    beta = best_score

        #print(f"Returning {best_score}")
        self.nodes += 1
        return best_score, best_move


    def get_move(self, board, max_nodes = 100):
        score, move = self.alphabeta_search(board, self.max_depth, self.stone, -np.inf, np.inf)
        print("\n" + str(score))
        return move



# In[ ]:



x = Strategy("X", max_depth=3)
o = Strategy("O", max_depth=3)
board = np.array([['-'] * 8 for _ in range(8)])


board = np.array([list(x) for x in """
-|-|-|-|-|-|O|-
-|-|X|-|X|-|O|O
-|-|-|-|O|-|O|-
-|-|X|X|X|O|-|-
-|-|-|-|X|-|-|-
-|-|-|O|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|O|X""".replace("|", "").split('\n')[1:]])

print("score", x.eval_board(board, "X"))

print(x.get_move(board))
print(x.nodes)
print(x.pruned)


# In[7]:


def play_game(board, strategy_1, strategy_2):
    player1_turn = True
    turn_count = 0
    n = len(board)
    m = len(board[0])
    while not complete_board(board) and turn_count < m*n:
        if player1_turn:
            row, col = strategy_1.get_move(board)
            board[row][col] = "X"
        else:
            row, col = strategy_2.get_move(board)
            board[row][col] = "O"
        turn_count += 1
        print(turn_count, "X" if player1_turn else "O", f"{row},{col}")
        print_board(board, (row, col))
        player1_turn = not player1_turn
    return complete_board(board)


board = np.array([list(x) for x in """
-|-|-|-|-|-|O|-
-|-|X|-|X|-|-|O
-|-|-|X|O|-|O|-
-|-|X|-|X|O|-|-
-|-|-|-|X|-|-|-
-|-|-|O|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|O|X""".replace("|", "").split('\n')[1:]])
# n = 15
# board = np.array([["-"]*n for _ in range(n)])
# board[n//2][n//2] = "X"
# board[n//2 - 1][n//2 - 1] = "X"
# board[n//2][n//2 - 1] = "O"
# board[n//2 - 1][n//2] = "O"
p1 = Strategy("X", max_depth=1)
p2 = Strategy("O", max_depth=1)
play_game(board, p1, p2)



# In[ ]:
p1 = Strategy("X", max_depth=1)
board = np.array([list(x) for x in """
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
-|-|-|-|O|-|-|-|-|-|-|-|-|-|-
-|-|-|-|-|X|-|-|O|X|-|-|-|-|-
-|-|-|-|-|-|X|O|X|-|-|-|-|-|-
-|-|-|-|-|-|O|X|-|-|-|-|-|-|-
-|-|-|-|-|O|-|-|O|-|-|-|-|-|-
-|-|-|-|-|-|-|-|-|X|-|-|-|-|-
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-""".replace("|", "").split('\n')[1:]])
print_board(board)

for stone in ["O", "X"]:
    for k in range(2,6):
        for row in iter_seqs(board):
            row = list(row)
            if live_k(row, k, stone):
                print(row, "LIVE", k, stone)
            if dead_k(row, k, stone):
                print(row, "DEAD", k, stone)
print(p1.eval_board(board, "X"))


# In[ ]:
p1 = Strategy("X", max_depth=3)
board = np.array([list(x) for x in """
-|-|-|-|-|-|-|-
-|-|X|-|X|-|O|O
-|-|-|-|-|-|O|-
-|-|X|-|X|O|-|-
-|-|-|-|-|-|-|-
-|-|-|O|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|O|X""".replace("|", "").split('\n')[1:]])

import time
from collections import defaultdict
N = 1000
t0 = time.time()
for _ in range(N):
    stone = "X"
    live_count = defaultdict(int)
    dead_count = defaultdict(int)
    consecutive_5 = 0
    for k in range(2, 6):
        for row_idx in range(len(board)):
            bl = get_updiag(board, row_idx, 0)
            live_count[k]  += live_k(bl, k, stone)
            dead_count[k] += dead_k(bl, k, stone)
            consecutive_5 += consecutive_k(bl, 5, stone)
            bl = get_downdiag(board, row_idx, 0)
            live_count[k]  += live_k(bl, k, stone)
            dead_count[k] += dead_k(bl, k, stone)
            consecutive_5 += consecutive_k(bl, 5, stone)

        for col_idx in range(len(board[0])):
            bl = get_updiag(board, len(board) - 1, col_idx)
            live_count[k]  += live_k(bl, k, stone)
            dead_count[k] += dead_k(bl, k, stone)
            consecutive_5 += consecutive_k(bl, 5, stone)
            bl = get_downdiag(board, 0, col_idx)
            live_count[k]  += live_k(bl, k, stone)
            dead_count[k] += dead_k(bl, k, stone)
            consecutive_5 += consecutive_k(bl, 5, stone)
print((time.time() - t0) / N)
