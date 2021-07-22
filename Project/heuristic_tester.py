#!/usr/bin/env python
# coding: utf-8

# In[1]:
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
# =============================================================================
# All of your helper functions go here!
# =============================================================================



# In[3]:

def random_eval(_1, _2):
    return random.random()

def student_eval(board, stone):
    # Your code goes here!
    return 0 # Replace this!


# In[ ]:
# =============================================================================
# A playground to run your code against itself (or someone else)
# =============================================================================
import kille
from functools import partial

small_board = np.array([list(x) for x in """
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-""".replace("|", "").split('\n')[1:]])

# The difficulty_setting variable can be anything in [0, 1], with
# higher values meaning a harder bot. 0 is the random bot
# and 1 is the "hardest" bot
difficulty_setting = 0.0
slider_eval = partial(kille.slider_eval, difficulty=difficulty_setting)

p1 = Strategy("X", student_eval, max_depth=1) # Do not change the search depths!
p2 = Strategy("O", slider_eval, max_depth=1)
play_game(small_board, p1, p2) # Start with the small board, it is better for debugging.

# In[ ]:
# =============================================================================
# A playground to see what your code's next move would be and what the evaluation
# and/or the current position is
# =============================================================================

test_board = np.array([list(x) for x in """
O|X|X|X|-|-|X|-
-|O|-|-|-|-|-|-
-|-|O|-|-|-|-|-
-|-|-|O|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-""".replace("|", "").split('\n')[1:]])

p1 = Strategy("X", student_eval, max_depth=1) # Do not change the search depths!
print("Board score", p1.eval_function(test_board, "X"))
print("Next move", p1.get_move(test_board, "X"))


# In[ ]:
# =============================================================================
# Here are some good unit tests...
#
# Remember: For a search depth of 1, your heuristic *won't* be evaluated on
# the boards you see below, rather, it will be evaluated on all of the possible
# boards that can arise from placing an X on the board. Therefore,
# when your function is ran, it will be player "O"s turn.
# =============================================================================
import kille
from functools import partial


# The difficulty_setting variable can be anything in [0, 1], with
# higher values meaning a harder bot. 0 is the random bot
# and 1 is the "hardest" bot
# You should be able to beat the first couple test cases on hard,
# since a win is garaunteed
difficulty_setting = 1.0
slider_eval = partial(kille.slider_eval, difficulty=difficulty_setting)


# Test 1: Easy winning row. Your bot should win in one move.
small_board = np.array([list(x) for x in """
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|X|X|X|X|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-""".replace("|", "").split('\n')[1:]])

p1 = Strategy("X", student_eval, max_depth=1) # Do not change the search depths!
p2 = Strategy("O", slider_eval, max_depth=1)
play_game(small_board, p1, p2)


# In[ ]:

# Test 2: This test is a bit harder.
difficulty_setting = 1.0
slider_eval = partial(kille.slider_eval, difficulty=difficulty_setting)
small_board = np.array([list(x) for x in """
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|X|X|X|X|-
-|-|-|-|-|-|-|-
-|-|-|O|O|O|O|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-""".replace("|", "").split('\n')[1:]])

p1 = Strategy("X", student_eval, max_depth=1) # Do not change the search depths!
p2 = Strategy("O", slider_eval, max_depth=1)
play_game(small_board, p1, p2)


# In[ ]:

# Test 3: A test for playing from the starting position
difficulty_setting = 0.25
slider_eval = partial(kille.slider_eval, difficulty=difficulty_setting)
small_board = np.array([list(x) for x in """
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|X|O|-|-|-
-|-|-|O|X|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-""".replace("|", "").split('\n')[1:]])

p1 = Strategy("X", student_eval, max_depth=1) # Do not change the search depths!
p2 = Strategy("O", slider_eval, max_depth=1)
play_game(small_board, p1, p2)

# In[ ]:

# Test 4: A test for (1) finding diagonal consecutive Xs and
# (2) Realizing the open 4's are almost always winning.
difficulty_setting = 0.25
slider_eval = partial(kille.slider_eval, difficulty=difficulty_setting)
small_board = np.array([list(x) for x in """
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|X|-|-|-|-|-
-|-|-|X|O|-|-|-
-|-|-|O|X|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-""".replace("|", "").split('\n')[1:]])

p1 = Strategy("X", student_eval, max_depth=1) # Do not change the search depths!
p2 = Strategy("O", slider_eval, max_depth=1)
play_game(small_board, p1, p2)

# In[ ]:

# Test n: A very hard test that tests two things:
# (1) above all else, your heuristic should make sure that an X gets placed
# on the diagonal to stop O from winning
# (2) After blocking O, your heuristic should place an X to construct an
# "open 4" on one of the two possible diagonals, thus ensuring a win in ~2 moves
difficulty_setting = 1
slider_eval = partial(kille.slider_eval, difficulty=difficulty_setting)
small_board = np.array([list(x) for x in """
-|-|-|-|-|-|-|-
-|-|-|-|-|-|-|-
-|-|X|-|X|O|-|-
-|-|-|X|O|X|-|-
-|-|-|O|X|-|X|-
-|-|O|-|-|-|-|-
-|X|-|-|-|-|-|-
-|-|-|-|-|-|-|-""".replace("|", "").split('\n')[1:]])

p1 = Strategy("X", student_eval, max_depth=1) # Change this to the slider eval to see how it should play out
p2 = Strategy("O", slider_eval, max_depth=1)
play_game(small_board, p1, p2)


# In[ ]:

# =============================================================================
# Tournament code! This code will run your function against bots of different
# difficulty.
# =============================================================================

from itertools import combinations
from collections import defaultdict, Counter
import random
import copy
import time
from tqdm.notebook import tqdm
import multiprocessing
from prettytable import PrettyTable

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


easy_bot = partial(kille.slider_eval, difficulty=0)
medium_bot = partial(kille.slider_eval, difficulty=0.2)
hard_bot = partial(kille.slider_eval, difficulty=0.5)
hardest_bot = partial(kille.slider_eval, difficulty=1.0)

eval_functions = [
    (easy_bot, "easy bot"),
    (medium_bot, "medium bot"),
    (hard_bot, "hard bot"),
    (hardest_bot, "hardest bot"),
    (student_eval, "My eval")
]
pool = multiprocessing.Pool(2)
all_pairs = list(combinations(eval_functions, 2))
N = 10 # Number of games per matchup

# =============================================================================
# Empty start board
# =============================================================================
win_count = {gname: [] for _, gname in eval_functions}
for e1, e2 in tqdm(all_pairs):
    # print(e1[1], e2[1])
    eval_1, name_1 = e1
    eval_2, name_2 = e2
    f = partial(get_winner_name, e1=e1, e2=e2)
    winners = pool.imap_unordered(f, (0 for _ in range(N)))
    for winner in winners:
        if winner == name_1:
            win_count[name_1].append(name_2)
        elif winner == name_2:
            win_count[name_2].append(name_1)

win_array = np.zeros((len(eval_functions), len(eval_functions)), dtype=object)
for gidx, (_, gname) in enumerate(eval_functions):
    if "bot" in gname:
        continue
    count = Counter(win_count[gname])
    for oidx, (_, opponent) in enumerate(eval_functions):
        if gname == opponent:
            win_array[gidx][oidx] = '-'
            continue
        win_array[gidx][oidx] = count[opponent]

table = PrettyTable()

table.field_names = [str(N)] + [gname for _, gname in eval_functions]
for gidx, (_, gname) in enumerate(eval_functions):
    if "bot" in gname:
        continue
    table.add_row([gname] + list(win_array[gidx]))
print()
print(table)

# =============================================================================
# Random start board
# =============================================================================
win_count = {gname: [] for _, gname in eval_functions}
for e1, e2 in tqdm(all_pairs):
    # print(e1[1], e2[1])
    eval_1, name_1 = e1
    eval_2, name_2 = e2
    f = partial(get_winner_name, e1=e1, e2=e2)
    winners = pool.imap_unordered(f, (random.randint(0, 8*8/2) for _ in range(N)))
    for winner in winners:
        if winner == name_1:
            win_count[name_1].append(name_2)
        elif winner == name_2:
            win_count[name_2].append(name_1)

win_array = np.zeros((len(eval_functions), len(eval_functions)), dtype=object)
for gidx, (_, gname) in enumerate(eval_functions):
    if "bot" in gname:
        continue
    count = Counter(win_count[gname])
    for oidx, (_, opponent) in enumerate(eval_functions):
        if gname == opponent:
            win_array[gidx][oidx] = '-'
            continue
        win_array[gidx][oidx] = count[opponent]

table = PrettyTable()

table.field_names = [str(N)] + [gname for _, gname in eval_functions]
for gidx, (_, gname) in enumerate(eval_functions):
    if "bot" in gname:
        continue
    table.add_row([gname] + list(win_array[gidx]))
print()
print(table)

