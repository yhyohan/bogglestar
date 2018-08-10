
import os
import time
from django.conf import settings
from boggle.apps.core.models import Board, BORDER, LETTERS

dictionary_url = os.path.join(settings.STATIC_ROOT, 'dictionary.txt')
board_url = os.path.join(settings.STATIC_ROOT, 'TestBoard.txt')

""" Restructure the board string into space-separated rows of N letters each. """
# TODO: validate
board_string = open(board_url).read().upper().split(", ")
board_rows =  ["".join(board_string[i:i+4]) for i in range(0, len(board_string), 4)]
board_letters = " ".join(board_rows)
board = Board(board_letters)
# print(board_letters)

def prefixes(word):
    """ A list of the initial sequences of a word, not including the complete word. """
    return [word[:i] for i in range(len(word))]

""" Generate a pair of sets: all the words in the dictionary, and all the prefixes. (Uppercased.) """
WORDS = set(open(dictionary_url).read().upper().split())
PREFIXES = set(p for word in WORDS for p in prefixes(word))

def solve(board):
    """ Find all valid words on a Boggle board (object) """
    # your code here
    result = set()
    N = board.size

    def extend_path(prefix, path):
        if prefix in WORDS:
            result.add(prefix)
        if prefix in PREFIXES:
            for j in board.adjacent_grids(path[-1]): # Explore surrounding neighbors to find prefix matching
                if j not in path and board.grids[j] != BORDER: # unvisited grid
                    if board.grids[j] == '*':
                        for L in LETTERS: extend_path(prefix + L, path + [j])
                    else:
                        extend_path(prefix + board.grids[j], path + [j])

    """ Inspect each grid and recursively extend it - stopping when there is no matching prefix or encountering borders """
    for (i, L) in enumerate(board.grids):
        if L != BORDER:
            if L == '*':
                for L2 in LETTERS: extend_path(L2, [i])
            else:
                extend_path(L, [i])

    return result

ts = time.time()
VALID_WORDS = solve(board)
te = time.time()

print(VALID_WORDS)
print(len(VALID_WORDS))
print("solved in: {} seconds".format(te-ts))
