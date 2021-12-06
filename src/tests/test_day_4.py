import logging

log = logging.getLogger(__name__)

from advent2021.bingo import (
    new_game,
    Game,
    Board,
)

def mk_lines(s):
    for line in s.split('\n'):
        yield line

sample_data = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

def test_parse_bingo():
    lines = mk_lines(sample_data)
    game = new_game(lines)
    assert len(game.draws) == 27
    assert list(game.draws) == [
        7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
    ]
    assert len(game.boards) == 3
    log.debug(f'{game.boards=}')

def test_draw():
    lines = mk_lines(sample_data)
    game = new_game(lines)
    draws = [
        7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
    ]
    for drawn in draws:
        game.draw()
        assert game.called == drawn

class BoardMock:

    def __init__(self):
        self.marked_called_with = []

    def mark(self, number):
        self.marked_called_with.append(number)

def test_game_draw_marks_boards():
    m1 = BoardMock()
    m2 = BoardMock()
    game = Game(draws=[1, 2, 3, 4], boards=[m1, m2])
    game.draw()
    game.draw()
    game.draw()
    game.draw()
    assert m1.marked_called_with == [1, 2, 3, 4]
    assert m2.marked_called_with == [1, 2, 3, 4]

def test_mark_board_number_changes_score():
    numbers = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 24, 25,
    ]
    board = Board.from_numbers(numbers)
    assert board.numbers == numbers
    score = sum(n for n in range(1, 25 + 1))
    assert board.score == score
    assert board.final_score == 0
    for n in range(1, 25 + 1):
        board.mark(n)
        score -= n
        assert board.score == score
        assert board.final_score == score * n

def test_complete_row_or_column_wins():
    numbers = [
        1,   2,  3,  4,  5,
        6,   7,  8,  9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 24, 25,
    ]
    board = Board.from_numbers(numbers)
    assert not board.wins
    for n in [6, 7, 8, 9]:
        board.mark(n)
        assert not board.wins
    board.mark(10)
    assert board.wins
    board = Board.from_numbers(numbers)
    assert not board.wins
    for n in [3, 8, 13, 18]:
        board.mark(n)
        assert not board.wins
    board.mark(23)
    assert board.wins

def test_all_boards():
    lines = mk_lines(sample_data)
    game = new_game(lines)
    assert game.winner == None
    while game.winner is None:
        game.draw()
    assert game.winner is not None
    assert game.winner.score == 188
    assert game.winner.final_score == 188 * 24
