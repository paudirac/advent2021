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
    def winner(self):
        if len(self.winners) > 0:
            return self.winners[0]
        else:
            return None

    @property
    def last_winner(self):
        return self.winners[-1]

    @property
    def winners(self):
        won_boards = filter(lambda board: board.wins, self.boards)
        return list(sorted(won_boards, key=lambda board: board.draws_played_till_won))

    @property
    def called(self):
        assert self._drawn_index >= 0, "Invalid draw state. Too few draws"
        assert self._drawn_index < len(self.draws), f"Invalid draw state. Too many draws: {self._drawn_index} vs maximum {len(self.draws)}"
        return self.draws[self._drawn_index]

    @property
    def all_boards_won(self):
        return all(board.wins for board in self.boards)

class Board:

    def __init__(self, numbers):
        self.numbers = numbers
        self.marked = set()
        self._marked = [False for _ in numbers]
        self.last_mark = None
        self.draws_played_till_won = 0

    def mark(self, n):
        if not self.wins:
            self.draws_played_till_won += 1
            try:
                i = self.numbers.index(n)
                self._marked[i] = True
                self.marked.add(n)
                self.last_mark = n
            except: # Not in the list
                pass
        else:
            pass # stop marking the board when won

    @property
    def score(self):
        return sum(n for n in self.numbers if n not in self.marked)

    @property
    def final_score(self):
        #assert self.last_mark is not None, "Invalid end state, no last_mark"
        if self.last_mark is None:
            return 0
        return self.score * self.last_mark

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
            return all(self.numbers[index] in self.marked for index in line_indexes)
            #return all(self._marked[index] for index in line_indexes)
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
    return [int(num.strip()) for num in line.split(',')]

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
