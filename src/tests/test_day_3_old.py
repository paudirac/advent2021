from advent2021.diagnostics_old import (
    tokenize,
    Iter,
    Tups,
    Counts,
    Accum,
    Most,
    Least,
    lst_to_int,
    Reducer,
    MultiReducer,
    count01,
    Iterable,
    least,
    most,
    zeroone,
    gamma_rate,
    epsilon_rate,
)

import logging
log = logging.getLogger(__name__)

def mk_sample(s):
    for line in s.split('\n'):
        yield line


def test_parse():
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
    tokens = list(tokenize(sample))
    assert tokens == [
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

def test_iter():
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
    tokens = tokenize(sample)
    gr = Iter(tokens)
    processed = list(gr)
    assert processed == [
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

def test_iterable():
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
    tokens = tokenize(sample)
    iterable = Iterable(tokens)
    assert iterable.map(lambda x: x) == [
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
    assert iterable.map(lambda _: 42) == [
        42, 42, 42,
        42, 42, 42,
        42, 42, 42,
        42, 42, 42,
    ]


def test_tups():
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
    tokens = tokenize(sample)
    iterable = Iterable(tokens)
    assert iterable.map(tuple) == [
        tuple("00100"),
        tuple("11110"),
        tuple("10110"),
        tuple("10111"),
        tuple("10101"),
        tuple("01111"),
        tuple("00111"),
        tuple("11100"),
        tuple("10000"),
        tuple("11001"),
        tuple("00010"),
        tuple("01010"),
    ]

def test_counts():
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
    tokens = tokenize(sample)
    iterable = Iterable(tokens)
    processed = iterable.mapi(tuple) \
                        .map(zeroone)
    assert processed[0] == [(1,0), (1,0), (0,1), (1,0), (1,0)]
    assert processed[1] == [(0,1), (0,1), (0,1), (0,1), (1,0)]


def test_total_counts():
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
    tokens = tokenize(sample)
    iterable = Iterable(tokens)
    processed = iterable.mapi(tuple) \
                        .mapi(zeroone)
    reducer = MultiReducer(count01, (0,0), n=5)
    res = reducer.reduce(processed)
    assert res == [(5, 7), (7, 5), (4, 8), (5, 7), (7, 5)]


    # accum = Accum(tokens)
    # processed = list(accum)
    # assert processed[-1] == [(5, 7), (7, 5), (4, 8), (5, 7), (7, 5)]
    # assert accum.accum == [(5, 7), (7, 5), (4, 8), (5, 7), (7, 5)]

def test_reducer():
    reducer = Reducer(lambda x, y: x + y, 0)
    assert reducer.reduce([1, 2, 3, 4]) == 10
    reducer = Reducer(lambda x, y: x * y, 1)
    assert reducer.reduce([1, 2, 3, 4]) == 24
    reducer = Reducer(lambda x, y: x + str(y), '')
    assert reducer.reduce([1, 2, 3, 4]) == '1234'

def test_multireducer():
    iterator = [
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
    ]
    reducer = MultiReducer(lambda x, y: x + y, 0, n=2)
    assert reducer.reduce(iterator) == [10, 8]
    reducer = MultiReducer(lambda x, y: x * y, 1, n=2)
    assert reducer.reduce(iterator) == [24, 16]
    reducer = MultiReducer(lambda x, y: x + str(y), '', n=2)
    assert reducer.reduce(iterator) == ['1234', '2222']


def test_most_common():
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
    tokens = tokenize(sample)
    iterable = Iterable(tokens)
    processed = iterable.mapi(tuple) \
                        .mapi(zeroone)
    reducer = MultiReducer(count01, (0,0), n=5)
    res = reducer.reduce(processed)
    print(f'{res=}')
    iterable = Iterable(res)
    def most(zo):
        zero, one = zo
        return '0' if zero > one else '1'
    res = iterable.map(most)
    assert res == ['1', '0', '1', '1', '0']

    # most = Most(tokens)
    # processed = list(most)
    # assert processed[-1] == ['1', '0', '1', '1', '0']


def test_least_common():
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
    tokens = tokenize(sample)
    iterable = Iterable(tokens)
    processed = iterable.mapi(tuple) \
                        .mapi(zeroone)
    reducer = MultiReducer(count01, (0,0), n=5)
    res = reducer.reduce(processed)
    print(f'{res=}')
    iterable = Iterable(res)
    def least(zo):
        zero, one = zo
        return '1' if zero > one else '0'
    res = iterable.map(least)
    assert res == ['0', '1', '0', '0', '1']

    # tokens = tokenize(sample)
    # least = Least(tokens)
    # processed = list(least)
    # assert processed[-1] == ['0', '1', '0', '0', '1']


def test_gamma():
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
    tokens = tokenize(sample)
    iterable = Iterable(tokens)
    processed = iterable.mapi(tuple) \
                        .mapi(zeroone)
    reducer = MultiReducer(count01, (0,0), n=5)
    res = reducer.reduce(processed)
    iterable = Iterable(res)
    res = iterable.map(most)
    res = lst_to_int(res)
    assert res == 22
    # tokens = tokenize(sample)
    # most = Most(tokens)
    # processed = list(most)
    # assert lst_to_int(processed[-1]) == 22

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
    tokens = tokenize(sample)
    assert gamma_rate(tokens) == 22



def test_epsion():
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
    tokens = tokenize(sample)
    iterable = Iterable(tokens)
    processed = iterable.mapi(tuple) \
                        .mapi(zeroone)
    reducer = MultiReducer(count01, (0,0), n=5)
    res = reducer.reduce(processed)
    iterable = Iterable(res)
    res = iterable.map(least)
    res = lst_to_int(res)
    assert res == 9
    # least = Least(tokens)
    # processed = list(least)
    # assert lst_to_int(processed[-1]) == 9
    #
def test_epsion_rate():
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
    tokens = tokenize(sample)
    assert epsilon_rate(tokens) == 9
    # least = Least(tokens)
    # processed = list(least)
    # assert lst_to_int(processed[-1]) == 9
