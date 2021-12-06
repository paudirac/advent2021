import re

_IS_BLANK = re.compile(r'\s+$')

import logging
log = logging.getLogger(__name__)

def is_blank(line):
    return _IS_BLANK.match(line) or len(line) == 0

class Game:

    def __init__(self, draws, boards):
        self.draws = draws
        self.boards = boards
        self._drawn_index = None

    def draw(self):
        self._next()
        for board in self.boards:
            board.mark(self.called)

    def _next(self):
        if self._drawn_index is None:
            self._drawn_index = 0
        else:
            self._drawn_index += 1

    @property
    def called(self):
        return self.draws[self._drawn_index]

class Board:

    def __init__(self, numbers):
        self.numbers = numbers

    def mark(self, called):
        pass

    def __repr__(self):
        r  = '----- Board -----\n'
        r += f'{self.numbers}\n'
        r += '-----------------\n'
        return r

def _draws(line):
    return [int(num) for num in line.split(',')]

def _board(board_data):
    numbers = [int(num) for line in board_data for num in line.split()]
    return Board(numbers)

def _boards(lines):
    boards = []
    board_data = []
    for line in lines:
        if not is_blank(line):
            board_data.append(line)
        else:
            boards.append(_board(board_data))
            board_data = []
    return boards

def new_game(lines):
    lines = list(lines)
    assert len(lines) > 0, "Not enough data!"
    draws = _draws(lines[0])
    assert is_blank(lines[1]), "Invalid data!"
    boards = _boards(lines[2:])
    return Game(draws=draws, boards=boards)
