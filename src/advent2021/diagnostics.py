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

