#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import numpy as np
import termcolor
from termcolor import cprint
from tqdm import tqdm
import copy
import time


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


def print_board(board, bolded=None, lines=False):
    """A debugging function to print you board in a pretty way"""
    n = len(board)
    color = "red"
    # For every row but the last
    cprint(" | " + " ".join(str(col_idx) for col_idx in range(len(board[0]))), attrs=["underline"]) if lines else None
    print(" |") if lines else None
    for row_idx, row in enumerate(board[:-1]):
        # Print the row as a string with a line below
        cprint(f"{row_idx}| ", end="") if lines else None
        if bolded and row_idx==bolded[0]:
            cprint("|".join(row[:bolded[1]]) + '|' if bolded[1] != 0 else '', None, attrs=["underline"], end='')
            cprint(row[bolded[1]], color, attrs=["underline", "bold"], end='')
            if bolded[1] != len(row) - 1:
                cprint("|" + "|".join(row[bolded[1]+1:]), None, attrs=["underline"], end='')
            print()
        else:
            cprint("|".join(row), None, attrs=["underline"])
    row = board[-1]
    cprint(f"{len(board)-1}| ", end="") if lines else None
    if bolded and bolded[0] == len(board) - 1:
        print("|".join(row[:bolded[1]]), end='|' if bolded[1] != 0 else '')
        cprint(row[bolded[1]], color, attrs=["bold"], end='')
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
    c += sum(row[i:i+5].count(stone) == k and consecutive_k not in (row[i+j:i+j+k] for j in range(5-k+1)) and row[i:i+5].count('-') == 5-k for i in range(len(row) -  4))
    if k == 4:
        c += sum(row[i:i+5].count(stone) == k and row[i:i+5].count('-') == 5-k for i in range(len(row) -  4))
    return c

def get_downdiag(board, row_idx, col_idx):
    return [board[row_idx + i][col_idx + i] for i in range(min(len(board) - row_idx, len(board) - col_idx))]

def get_updiag(board, row_idx, col_idx):
    return [board[row_idx - i][col_idx + i] for i in range(min(row_idx + 1, len(board) - col_idx))]


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

def smart_board_eval(board, stone):
    max_val = 100000000
    op_val = 1000000
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

def slider_eval(board, stone, difficulty=0.0):
    if random.random() >= difficulty:
        return random.random()
    else:
        return smart_board_eval(board, stone)


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


def play_game(board, strategy_1, strategy_2, supress_output=False):
    player1_turn = True
    winner = None
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
        if not supress_output:
            print(f"# {turn_count}", "\tPlayer", "X" if player1_turn else "O", f"\tMove: {row},{col}")
            print_board(board, (row, col))
            print("")
        board[row][col] = "X" if player1_turn else "O"
        player1_turn = not player1_turn
    if not winner_stone(board, "O") and  not winner_stone(board, "X"):
        if not supress_output:
         print("Tie!")
    elif winner_stone(board, "O"):
        if not supress_output:
            print("Opponent won!")
        winner = "O"
    else:
        if not supress_output:
            print("Student won!")
        winner = "X"
    return winner



# In[ ]:

# =============================================================================
# Tournament code!
# =============================================================================
from itertools import combinations
from collections import defaultdict, Counter
import multiprocessing
from  functools import partial
from prettytable import PrettyTable

def get_random_board(n, turn_count=None):
    board = np.array([["-"]*n for _ in range(n)])
    moves = random.randint(1, n*n/2) if turn_count is None else turn_count
    stone = "X"
    board[n//2][n//2] = "X"
    board[n//2 - 1][n//2 - 1] = "X"
    board[n//2 - 1][n//2] = "O"
    board[n//2][n//2 - 1] = "O"
    
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

def get_winner_name(turn_count, e1, e2):
    board = get_random_board(n=8, turn_count=turn_count)
    if random.random() <= 0.5:
        e1, e2 = e2, e1
    eval_x, name_x = e1
    eval_o, name_o = e2
    p1 = Strategy("X", eval_x, max_depth=1)
    p2 = Strategy("O", eval_o, max_depth=1)
    winner = play_game(board, p1, p2, supress_output=True)
    if winner == "X":
        return name_x
    elif winner == "O":
        return name_o


def avg_time(eval_f, N=1000):
    boards = [get_random_board(n=8, turn_count=random.randint(0, 8*8/2)) for _ in range(N)]
    t0 = time.time()
    for board in boards:
        eval_f(board, "X")
    return (time.time() - t0)/N


def get_times():
    from group1 import student_eval as group1_eval
    from group2 import student_eval as group2_eval
    from group3 import student_eval as group3_eval
    from group4 import student_eval as group4_eval
    from group5 import student_eval as group5_eval
    easy_bot = partial(slider_eval, difficulty=0)
    medium_bot = partial(slider_eval, difficulty=0.2)
    hard_bot = partial(slider_eval, difficulty=0.5)
    hardest_bot = partial(slider_eval, difficulty=1.0)

    eval_functions = [
        (easy_bot, "easy bot"),
        (medium_bot, "medium bot"),
        (hard_bot, "hard bot"),
        (hardest_bot, "hardest bot"),
        (group1_eval, "Group 1"),
        (group2_eval, "Group 2"),
        (group3_eval, "Group 3"),
        (group4_eval, "Group 4"),
        (group5_eval, "Group 5")
    ]
    
    for eval_f, bot_name in eval_functions:
        print(f"The eval function for {bot_name} has an average time of {avg_time(eval_f)}s")

def run_tournament(N=10, random_board=False):
    from group1 import student_eval as group1_eval
    from group2 import student_eval as group2_eval
    from group3 import student_eval as group3_eval
    from group4 import student_eval as group4_eval
    from group5 import student_eval as group5_eval

    easy_bot = partial(slider_eval, difficulty=0)
    medium_bot = partial(slider_eval, difficulty=0.2)
    hard_bot = partial(slider_eval, difficulty=0.5)
    hardest_bot = partial(slider_eval, difficulty=1.0)

    eval_functions = [
        (easy_bot, "easy bot"),
        (medium_bot, "medium bot"),
        (hard_bot, "hard bot"),
        (hardest_bot, "hardest bot"),
        (group1_eval, "Group 1"),
        (group2_eval, "Group 2"),
        (group3_eval, "Group 3"),
        (group4_eval, "Group 4"),
        (group5_eval, "Group 5")
    ]
    pool = multiprocessing.Pool(12)
    all_pairs = list(combinations(eval_functions, 2))
    
    win_count = {gname: [] for _, gname in eval_functions}
    for e1, e2 in tqdm(all_pairs):
        # print(e1[1], e2[1])
        eval_1, name_1 = e1
        eval_2, name_2 = e2
        f = partial(get_winner_name, e1=e1, e2=e2)
        winners = pool.imap_unordered(f, (random.randint(0, 8*8/2) if random_board else 0 for _ in range(N)))
        # winners = [f(random.randint(0, 8*8/2)) for x in range(N)]
        for winner in winners:
            if winner == name_1:
                win_count[name_1].append(name_2)
            elif winner == name_2:
                win_count[name_2].append(name_1)

    win_array = np.zeros((len(eval_functions), len(eval_functions)), dtype=object)
    for gidx, (_, gname) in enumerate(eval_functions):
        # if "bot" in gname:
        #     continue
        count = Counter(win_count[gname])
        for oidx, (_, opponent) in enumerate(eval_functions):
            if gname == opponent:
                win_array[gidx][oidx] = '-'
                continue
            win_array[gidx][oidx] = count[opponent]

    table = PrettyTable()

    table.field_names = [str(N)] + [gname for _, gname in eval_functions]
    for gidx, (_, gname) in enumerate(eval_functions):
    #     if "bot" in gname:
    #         continue
        table.add_row([gname] + list(win_array[gidx]))
    print(table)
    

# In[ ]:
# hardest_bot = partial(slider_eval, difficulty=1.0)
# p2 = Strategy("O", hardest_bot, max_depth=3)
# small_board = np.array([list(x) for x in """
# -|-|-|-|-|-|-|-
# -|O|-|-|-|-|-|-
# -|O|X|-|-|X|X|-
# -||-|X|O|-|-|-
# -|O|X|O|X|-|-|-
# -|O|O|-|-|X|-|-
# -|O|-|-|-|-|O|-
# X|-|-|-|-|-|-|-""".replace("|", "").split('\n')[1:]])
# print(p2.get_move(small_board))
