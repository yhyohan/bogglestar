# from django.db import models

# import random
import string
import time
import uuid

from rest_framework import serializers

# Create your models here.
BORDER = '|'
LETTERS = list(string.ascii_uppercase)
POSSIBLE_CHARS = LETTERS + ["*"]

# board_letters = [random.choice(possible_chars) if (x % 5 != 4) else " " for x in range(19)]
# board_letters = "".join(board_letters)

class Board:

    def __init__(self, text):
        """Takes in a string of space-separated rows of N letters each"""
        rows = text.split()
        N = len(rows)
        rows = [BORDER*N] + rows + [BORDER*N]

        self.text = text
        self.grids = ''.join(BORDER + row + BORDER for row in rows)
        self.size = int(len(self.grids)**0.5)

    def adjacent_grids(self, i):
        "Return the indexes (in the board array) of all adjacent cells"
        N = self.size
        return (i-N-1, i-N, i-N+1, i-1, i+1, i+N-1, i+N, i+N+1)

    def display(self):
        "Return a string representation of board."
        N = self.size
        return '\n'.join(self.board[i:i+N] for i in range(0, N**2, N))

    def __repr__(self):
        return self.text + '\n' + self.display()


GAMES = {}

class Game:

    def start(self, board):
        self.id = uuid.uuid4().hex
        self.board = board.text
        self.score = 0
        self.found_words = set()
        self.active = True
        self.gametime = int(time.time())

        self.save()

    @staticmethod
    def get(id):
        return GAMES.get(id)

    def end(self):
        self.active = False
        self.save()

    def save(self):
        GAMES[self.id] = self
        return self

    def update_score(self):
        "Calculate score based on word length ('cat' = 3, 'rare' = 4)"
        self.score = len("".join(self.found_words))

    def __repr__(self):
        return "id={} | {} | {} | score[{}] | {}".format(self.id, self.board, self.active, self.score, self.gametime)


class GameSerializer(serializers.Serializer):
    id = serializers.CharField()
    board = serializers.CharField()
    score = serializers.IntegerField()
    found_words = serializers.ListField()
    active = serializers.BooleanField()
    gametime = serializers.IntegerField()
