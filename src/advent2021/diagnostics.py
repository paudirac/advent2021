import re

import logging
log = logging.getLogger(__name__)


_IS_BLANK = re.compile(r'\s+')

def is_blank(line):
    return _IS_BLANK.match(line) or len(line) == 0

def tokenize(lines):
    for line in lines:
        try:
            if not is_blank(line):
                yield line.strip()
        except:
            pass

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

    def filter(self, f):
        return [item for item in self if f(item)]

    def ifilter(self, f):
        return Iterable(self.filter(f))

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
        return f(list(self))

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

def tokenize2(s):
    return [tuple(token) for token in tokenize(s)]

def to_int(arr):
    return int(''.join(arr), base=2)

def power_consumption(tokens):
    tokens = tokenize2(tokens)
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
    return gamma_rate * epsilon_rate


def oxygen_generator_rating(lines):
    rows = tokenize2(lines)
    m2d = Map2D(rows)
    def count01(column):
        zeros = sum(1 for _ in filter(lambda x: x == '0', column))
        ones = sum(1 for _ in filter(lambda x: x == '1', column))
        return zeros, ones
    def mostOr1(pair):
        zeros, ones = pair
        return 1 if ones >= zeros else 0

    filtered = m2d.rows
    for i in range(len(m2d.columns)):
        curr = Map2D(filtered)
        filter_value = curr.icolumns \
                           .imap(count01) \
                           .imap(mostOr1) \
                           .to(lambda cols: cols[i])
        def fi(row):
            fival = row[i] == str(filter_value)
            return fival
        filtered = curr.irows \
                       .filter(fi)
        if len(filtered) == 1:
            break
    assert len(filtered) == 1, "Too much data"
    return to_int(filtered[0])

def co2_scrubber_rating(lines):
    rows = tokenize2(lines)
    m2d = Map2D(rows)
    def count01(column):
        zeros = sum(1 for _ in filter(lambda x: x == '0', column))
        ones = sum(1 for _ in filter(lambda x: x == '1', column))
        return zeros, ones
    def leastOr0(pair):
        zeros, ones = pair
        return 1 if ones < zeros else 0

    filtered = m2d.rows
    for i in range(len(m2d.columns)):
        curr = Map2D(filtered)
        filter_value = curr.icolumns \
                           .imap(count01) \
                           .imap(leastOr0) \
                           .to(lambda cols: cols[i])
        def fi(row):
            fival = row[i] == str(filter_value)
            return fival
        filtered = curr.irows \
                       .filter(fi)
        if len(filtered) == 1:
            break
    assert len(filtered) == 1, "Too much data"
    return to_int(filtered[0])

def life_support_rating(lines):
    ogr = oxygen_generator_rating(lines)
    co2sr = co2_scrubber_rating(lines)
    return ogr * co2sr
