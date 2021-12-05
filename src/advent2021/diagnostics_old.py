import re

import logging
log = logging.getLogger(__name__)

_IS_BLANK = re.compile(r'\s+')

def is_blank(line):
    return _IS_BLANK.match(line) or len(line) == 0


class Iter:

    def __init__(self, lines):
        self.lines = lines

    def __iter__(self):
        self.__lines_iter = iter(self.lines)
        return self

    def __next__(self):
        current = next(self.__lines_iter)
        try:
            if not is_blank(current):
                proc = self.process(current)
                return proc
        except Exception as e:
            log.exception(e)
            pass
        raise StopIteration

    def process(self, current):
        return current

class Iterable:

    def __init__(self, lines):
        self.lines = list(lines)

    def __iter__(self):
        self.__lines_iter = iter(self.lines)
        return self

    def __next__(self):
        return next(self.__lines_iter)

    def map(self, f):
        return [f(item) for item in self]

    def mapi(self, f):
        mapped = self.map(f)
        return Iterable(mapped)

    def reduce(self, f, initial):
        return


class Tups(Iter):

    def process(self, current):
        curr = super().process(current)
        return tuple(curr)

class Counts(Tups):

    map0 = {
        '0': 1,
        '1': 0,
    }
    map1 = {
        '0': 0,
        '1': 1,
    }

    def process(self, current):
        curr = super().process(current)
        zeros = map(lambda x: self.map0[x], curr)
        ones = map(lambda x: self.map1[x], curr)
        return list(zip(zeros, ones))


def count01(accpair, pair):
    acc_zero, acc_one = accpair
    zero, one = pair
    return acc_zero + zero, acc_one + one


class Accum(Counts):

    def process(self, current):
        curr = super().process(current)
        self._ensure_accum(curr)
        for i in range(len(self.accum)):
            z_accum, o_accum = self.accum[i]
            zero, one = curr[i]
            self.accum[i] = z_accum + zero, o_accum + one
        return self.accum

    def _ensure_accum(self, current):
        if not hasattr(self, 'accum'):
            n = len(current)
            self.accum = [(0, 0)] * n

class Accumulator:

    def __init__(self, initial):
        self.total = initial

    def process(self, f, current):
        self.total = f(self.total, current)

class Reducer:

    def __init__(self, f, initial):
        self.f = f
        self.accumulator = Accumulator(initial)

    def reduce(self, lst):
        for item in lst:
            self.accumulator.process(self.f, item)
        return self.accumulator.total

class MultiReducer:

    def __init__(self, f, initial, n):
        self.f = f
        self.accumulators = []
        for _ in range(n):
            self.accumulators.append(Accumulator(initial))

    def reduce(self, iterator):
        for lst in iterator:
            for i, item in enumerate(lst):
                self.accumulators[i].process(self.f, item)
        return [accumulator.total for accumulator in self.accumulators]

class Most(Accum):

    def process(self, current):
        curr = super().process(current)
        return ['0' if zero > one else '1' for zero, one in curr]

class Least(Accum):

    def process(self, current):
        curr = super().process(current)
        return ['1' if zero > one else '0' for zero, one in curr]

def most(zo):
    zero, one = zo
    return '0' if zero > one else '1'

def least(zo):
    zero, one = zo
    return '1' if zero > one else '0'

def zeroone(row, zeromap={'0': 1, '1': 0}, onemap={'0': 0, '1': 1}):
    zeros = map(lambda x: zeromap[x], row)
    ones = map(lambda x: onemap[x], row)
    return list(zip(zeros, ones))


def lst_to_int(lst):
    return int(''.join(lst), base=2)

def tokenize(lines):
    for line in lines:
        try:
            if not is_blank(line):
                yield line.strip()
        except:
            pass

def gamma_rate(tokens, n=5):
    iterable = Iterable(tokens)
    processed = iterable.mapi(tuple) \
                        .mapi(zeroone)
    reducer = MultiReducer(count01, (0,0), n=n)
    res = reducer.reduce(processed)
    iterable = Iterable(res)
    res = iterable.map(most)
    return lst_to_int(res)

def epsilon_rate(tokens, n=5):
    iterable = Iterable(tokens)
    processed = iterable.mapi(tuple) \
                        .mapi(zeroone)
    reducer = MultiReducer(count01, (0,0), n=n)
    res = reducer.reduce(processed)
    iterable = Iterable(res)
    res = iterable.map(least)
    return lst_to_int(res)


def power_consumption(lns):
    tokens = list(tokenize(lns))
    logging.basicConfig(level=logging.DEBUG)
    gamma = gamma_rate(tokens, n=12)
    epsilon = epsilon_rate(tokens, n=12)
    return gamma * epsilon
