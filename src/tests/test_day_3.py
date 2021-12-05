import logging
log = logging.getLogger(__name__)

from advent2021.diagnostics import (
    tokenize,
    Map2D,
    power_consumption,
    life_support_rating,
    oxygen_generator_rating,
    co2_scrubber_rating,
    tokenize2,
)

def mk_sample(s):
    for line in s.split('\n'):
        yield line


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
    assert power_consumption(sample) == 198

def xtest_life_support_rating():
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
    assert life_support_rating(sample) == 230

single = (mk_sample("""
10111
    """), 23)
fifth_position = (mk_sample("""
10110
10111
"""), 23)
all_positions = (mk_sample("""
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
    """), 23)


@pytest.mark.parametrize(
    "lines, expected", [
        single,
        fifth_position,
        all_positions,
    ]
)
def test_ogr_single(lines, expected):
    assert oxygen_generator_rating(lines) == expected

def test_co2():
    lines = mk_sample("""
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
    assert co2_scrubber_rating(lines) == 10

def test_filters_oxigen():
    sample = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    rows = tokenize2(sample)
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
    assert filtered[0] == list('10111')

def test_filters_co2():
    sample = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    rows = tokenize2(sample)
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
    assert filtered[0] == list('01010')
