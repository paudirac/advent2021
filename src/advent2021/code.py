import logging
log = logging.getLogger(__name__)

def zip_one(lst):
    return zip(lst, lst[1:])

def count_larger(lst):
    diffs = [b-a for a,b in zip_one(lst)]
    return sum(1 for a in diffs if a >0)

class Chunks:

    def __init__(self, lst, window):
        self.lst = list(lst)
        self.len = len(self.lst)
        self.window = window

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= self.len - self.window + 1:
            raise StopIteration

        ret = self.lst[self.i:self.i + self.window]
        self.i += 1
        return ret

def sliding_sum(sample, window=1):
    # for chunk in Chunks(sample, window):
    #     print(f'{chunk=} {sum(chunk)}')
    return [sum(chunk) for chunk in Chunks(sample, window=window)]

def lines(f):
    for line in f.readlines():
        yield line

def int_lines(f):
    for line in f.readlines():
        yield int(line)

def as_list(g):
    return list(g)

from .submarine import (
    tokenize,
    Submarine,
    new_submarine,
    AimSubmarine,
    Position,
    AimPosition,
)

def day_2_1(lns):
    submarine = new_submarine(Position(x=0, y=0))
    commands = tokenize(lns)
    for cmd in commands:
        submarine.process(cmd)
    return submarine.position.x * submarine.position.y

def day_2_2(lns):
    submarine = new_submarine(AimPosition(x=0, y=0, aim=0))
    commands = tokenize(lns)
    for cmd in commands:
        submarine.process(cmd)
    return submarine.position.x * submarine.position.y

from .diagnostics import power_consumption, life_support_rating

def day_3_1(lns):
    logging.basicConfig(level=logging.DEBUG)
    return power_consumption(lns)

def day_3_2(lns):
    return life_support_rating(lns)

from .bingo import new_game

def day_4_1(lns):
    game = new_game(lns)
    while game.winner is None:
        game.draw()
    return game.winner.final_score

def day_4_2(lns):
    logging.basicConfig(level=logging.DEBUG)
    game = new_game(lns)
    while not game.all_boards_won:
        game.draw()
    assert all(board.wins for board in game.boards), "Not all won"
    return game.last_winner.final_score

from advent2021.vents import (
    new_lines,
    Diagram,
)

def day_5_1(lns):
    lines = new_lines(lns)
    diagram = Diagram(lines.bounds())
    top_left, bottom_right = diagram.bounds
    for line in lines:
        diagram.draw(line)
    at_least_two_lines = lambda count: count >= 2
    pos_with_at_least_two_lines = diagram.positions_with(at_least_two_lines)
    return len(pos_with_at_least_two_lines)

def day_5_2(lns):
    lines = new_lines(lns, condition=lambda linedef: True)
    diagram = Diagram(lines.bounds())
    top_left, bottom_right = diagram.bounds
    for line in lines:
        diagram.draw(line)
    at_least_two_lines = lambda count: count >= 2
    pos_with_at_least_two_lines = diagram.positions_with(at_least_two_lines)
    return len(pos_with_at_least_two_lines)

from .lanternfish import (
    parse_initial_population,
)

def day_6_1(lns):
    population = parse_initial_population(lns)
    population.get_old(days=80)
    return len(population)

def day_6_2(lns):
    population = parse_initial_population(lns)
    population.get_old(days=256)
    return len(population)

from .crabs import (
    parse_swarm,
    Aligner,
    increasing_rate,
)

def day_7_1(lns):
    swarm = parse_swarm(lns)
    aligner = Aligner(swarm)
    (pos, fuel) = aligner.minimum_fuel()
    return f'Minimum fuel: {fuel} to align to position: {pos}'

def day_7_2(lns):
    swarm = parse_swarm(lns)
    aligner = Aligner(swarm, individual_cost=increasing_rate)
    (pos, fuel) = aligner.minimum_fuel()
    return f'Minimum fuel: {fuel} to align to position: {pos}'

from .displays import (
    parse_entries,
    is_easy,
)

def day_8_1(lns):
    entries = parse_entries(lns)
    outputs = entries.outputs
    all_outputs = entries.all_outputs
    easy_ones = [out for out in all_outputs if is_easy(out)]
    return len(easy_ones)

DAYS = {
    '1.1': count_larger,
    '1.2': lambda l: count_larger(sliding_sum(l, window=3)),
    '2.1': day_2_1,
    '2.2': day_2_2,
    '3.1': day_3_1,
    '3.2': day_3_2,
    '4.1': day_4_1,
    '4.2': day_4_2,
    '5.1': day_5_1,
    '5.2': day_5_2,
    '6.1': day_6_1,
    '6.2': day_6_2,
    '7.1': day_7_1,
    '7.2': day_7_2,
    '8.1': day_8_1,
}

PARSER = {
    '1.1': lambda f: as_list(int_lines(f)),
    '1.2': lambda f: as_list(int_lines(f)),
    '2.1': lambda f: lines(f),
    '2.2': lambda f: lines(f),
    '3.1': lambda f: lines(f),
    '3.2': lambda f: lines(f),
    '4.1': lambda f: lines(f),
    '4.2': lambda f: lines(f),
    '5.1': lambda f: lines(f),
    '5.2': lambda f: lines(f),
    '6.1': lambda f: lines(f),
    '6.2': lambda f: lines(f),
    '7.1': lambda f: lines(f),
    '7.2': lambda f: lines(f),
    '8.1': lambda f: lines(f),
}

