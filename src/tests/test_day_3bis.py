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


class Map2D:

    def __init__(self, rows):
        self.rows = list(rows)

    @property
    def columns(self):
        return transpose(self.rows)

    def get(self, i, j):
        return self.rows[i][j]

class SDump(Map2D):

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
    assert dump.columns == [
        'aeimq',
        'bfjnr',
        'cgkos',
        'dhlpt',
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
