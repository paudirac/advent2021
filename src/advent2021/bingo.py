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
        self.marked = set()
        self._marked = [False for _ in numbers]

    def mark(self, n):
        try:
            i = self.numbers.index(n)
            self._marked[i] = True
            self.marked.add(n)
        except: # Not in the list
            pass

    @property
    def score(self):
        return sum(n for n in self.numbers if n not in self.marked)

    @property
    def wins(self):
        # assumig 5x5 board
        rows = [
            [0,   1,  2,  3,  4],
            [5,   6,  7,  8,  9],
            [10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19],
            [20, 21, 22, 23, 24],
        ]
        cols = [
            [0, 5, 10, 15, 20],
            [1, 6, 11, 16, 21],
            [2, 7, 12, 17, 22],
            [3, 8, 13, 18, 23],
            [4, 9, 14, 19, 24],
        ]
        def line(line_indexes):
            return all(self._marked[index] for index in line_indexes)
        return any(line(row) for row in rows) or any(line(col) for col in cols)

    def __repr__(self):
        r  = '\n----- Board -----\n'
        r += f'{self.numbers}\n'
        r += f'{self._marked}\n'
        r += '-----------------\n'
        return r

    @classmethod
    def from_numbers(cls, numbers):
        assert len(numbers) == 25, f"Invalid assumption, boards not 5x5. Total numbers: {len(numbers)}"
        assert len(set(numbers)) == len(numbers), f"Invalid board data. Repeated numbers in: {numbers}"
        return cls(numbers)

def _draws(line):
    return [int(num) for num in line.split(',')]

def _board(board_data):
    numbers = [int(num) for line in board_data for num in line.split()]
    return Board.from_numbers(numbers)

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
