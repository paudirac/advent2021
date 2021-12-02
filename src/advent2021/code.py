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
    Position,
    AimPosition,
)

def day_2_1(lns):
    submarine = Submarine(Position(x=0, y=0))
    commands = tokenize(lns)
    for cmd in commands:
        submarine.process(cmd)
    return submarine.position.x * submarine.position.y

def day_2_2(lns):
    submarine = Submarine(AimPosition(x=0, y=0, aim=0))
    commands = tokenize(lns)
    for cmd in commands:
        submarine.process(cmd)
    return submarine.position.x * submarine.position.y


DAYS = {
    '1.1': count_larger,
    '1.2': lambda l: count_larger(sliding_sum(l, window=3)),
    '2.1': day_2_1,
    '2.2': day_2_2,
}

PARSER = {
    '1.1': lambda f: as_list(int_lines(f)),
    '1.2': lambda f: as_list(int_lines(f)),
    '2.1': lambda f: lines(f),
    '2.2': lambda f: lines(f),
}

