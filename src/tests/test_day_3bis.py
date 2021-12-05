import logging
log = logging.getLogger(__name__)

from advent2021.diagnostics import tokenize

def mk_sample(s):
    for line in s.split('\n'):
        yield line

def transpose(rows):
    J = len(rows)
    I = len(rows[0]) if J else 0
    cols = []
    for i in range(I):
        cols.append([])
    for i in range(I):
        for j in range(J):
            cols[i].append(rows[j][i])
    return cols

def normalize(rows):
    rws = []
    for row in rows:
        cols = []
        for item in row:
            cols.append(item)
        rws.append(cols)
    return rws

class Iterable:

    def __init__(self, items):
        self.items = list(items)

    def __iter__(self):
        self.__items_iter = iter(self.items)
        return self

    def __next__(self):
        return next(self.__items_iter)

    def map(self, f):
        return [f(item) for item in self]

    def imap(self, f):
        mapped = self.map(f)
        return Iterable(mapped)

    def reduce(self, f, initial):
        acc = initial
        for item in self:
            acc = f(acc, item)
        return acc

    def do(self, f):
        for item in self:
            f(item)
        return self

    def to(self, f):
        return f(self)

class Map2D:

    def __init__(self, rows):
        self._rows = normalize(rows)

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return transpose(self._rows)

    def get(self, i, j):
        return self._rows[i][j]

    @property
    def irows(self):
        return Iterable(self.rows)

    @property
    def icolumns(self):
        return Iterable(self.columns)

class SDump(Map2D):

    @property
    def rows(self):
        rws = super().rows
        return [''.join(row) for row in rws]

    @property
    def columns(self):
        cols = super().columns
        return [''.join(column) for column in cols]


def test_dump():
    sample = mk_sample("""
abcd
efgh
ijkl
mnop
qrst
    """)
    tokens = tokenize(sample)
    dump = SDump(tokens)
    assert len(dump.columns) == 4
    assert len(dump.rows) == 5

def test_rows():
    sample = mk_sample("""
abcd
efgh
ijkl
mnop
qrst
    """)
    tokens = tokenize(sample)
    dump = SDump(tokens)
    assert dump.rows == [
        'abcd',
        'efgh',
        'ijkl',
        'mnop',
        'qrst',
    ]

def test_columns():
    sample = mk_sample("""
abcd
efgh
ijkl
mnop
qrst
    """)
    tokens = tokenize(sample)
    dump = SDump(tokens)
    assert dump.columns == [
        'aeimq',
        'bfjnr',
        'cgkos',
        'dhlpt',
    ]

def test_empty():
    dump = Map2D([])
    assert dump.rows == []
    assert dump.columns == []

def test_2dmap():
    dump = Map2D([
        ('a', 42),
        (3, 'b'),
    ])
    assert dump.rows == [
        ['a', 42],
        [3, 'b'],
    ]
    assert dump.columns == [
        ['a', 3],
        [42, 'b'],
    ]


import pytest

def test_random_access():
    sample = mk_sample("""
abcd
efgh
ijkl
mnop
qrst
    """)
    tokens = tokenize(sample)
    dump = SDump(tokens)
    assert dump.get(2,3) == 'l'
    assert dump.get(0,3) == 'd'
    with pytest.raises(IndexError):
        dump.get(0, 4)
    with pytest.raises(IndexError):
        dump.get(5, 0)

def tokenize2(s):
    return [tuple(token) for token in tokenize(s)]

def test_gamma_rate():
    sample = mk_sample("""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
    """)
    tokens = tokenize2(sample)
    dump = Map2D(tokens)
    def count01(column):
        zeros = sum(1 for _ in filter(lambda x: x == '0', column))
        ones = sum(1 for _ in filter(lambda x: x == '1', column))
        return zeros, ones
    def most(tup):
        z, o = tup
        return 0 if z > o else 1
    def identity(x): return x
    def to_int(arr):
        return int(''.join(arr), base=2)
    def second(a,b):
        return b
    gamma_rate = dump.icolumns \
               .imap(count01) \
               .imap(most) \
               .imap(str) \
               .to(to_int)
    assert gamma_rate == 22

def test_epsilon_rate():
    sample = mk_sample("""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
    """)
    tokens = tokenize2(sample)
    dump = Map2D(tokens)
    def count01(column):
        zeros = sum(1 for _ in filter(lambda x: x == '0', column))
        ones = sum(1 for _ in filter(lambda x: x == '1', column))
        return zeros, ones
    def least(tup):
        z, o = tup
        return 0 if z < o else 1
    def identity(x): return x
    def to_int(arr):
        return int(''.join(arr), base=2)
    def second(a,b):
        return b
    epsilon_rate = dump.icolumns \
               .imap(count01) \
               .imap(least) \
               .imap(str) \
               .to(to_int)
    assert epsilon_rate == 9

def test_power_consumption():
    sample = mk_sample("""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
    """)
    tokens = tokenize2(sample)
    dump = Map2D(tokens)
    def count01(column):
        zeros = sum(1 for _ in filter(lambda x: x == '0', column))
        ones = sum(1 for _ in filter(lambda x: x == '1', column))
        return zeros, ones
    def most(tup):
        z, o = tup
        return 0 if z > o else 1
    def least(tup):
        z, o = tup
        return 0 if z < o else 1
    def identity(x): return x
    def to_int(arr):
        return int(''.join(arr), base=2)
    def second(a,b):
        return b
    counts = dump.icolumns \
                 .imap(count01)
    gamma_rate = counts \
               .imap(most) \
               .imap(str) \
               .to(to_int)
    epsilon_rate = counts \
               .imap(least) \
               .imap(str) \
               .to(to_int)
    power_consumption = gamma_rate * epsilon_rate
    assert gamma_rate == 22
    assert epsilon_rate == 9
    assert power_consumption == 198
