"""
Standard segment mapping
 0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

0: abcefg  (6 segments)
1: cf      (2 segments) *unique
2: acdeg   (5 segments)
3: acdfg   (5 segments)
4: bcdf    (4 segments) *unique
5: abdfg   (5 segments)
6: abdefg  (6 segments)
7: acf     (3 segments) *unique
8: abcdefg (7 segments) *unique
9: abcdfg  (6 segments)
"""

import logging
log = logging.getLogger(__name__)

EASY_ONES = [2, 4, 3, 7]

def normalize_key(s):
    return ''.join(sorted(s))

def is_one(number):
    return len(number) == 2

from functools import wraps

def with_value(value):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return ValuedNumber.from_unvalued(f(*args, **kwargs), value)
        return wrapper
    return decorator

@with_value(1)
def one(numbers):
    return [n for n in numbers if is_one(n)][0]

def is_four(number):
    return len(number) == 4

@with_value(4)
def four(numbers):
    return [n for n in numbers if is_four(n)][0]

def is_seven(number):
    return len(number) == 3

@with_value(7)
def seven(numbers):
    return [n for n in numbers if is_seven(n)][0]

def is_eight(number):
    return len(number) == 7

@with_value(8)
def eight(numbers):
    return [n for n in numbers if is_eight(n)][0]

def is_six(number, vii, viii, blank):
    return len(number) == 6 and viii - vii - number == blank

@with_value(6)
def six(numbers, vii, viii, blank):
    return [n for n in numbers if is_six(n, vii=vii, viii=viii, blank=blank)][0]

@with_value(5)
def five(numbers):
    a, b, c = [n for n in numbers if len(n) == 5]
    if a + b not in numbers:
        return c
    if a + c not in numbers:
        return b
    else:
        return a

@with_value(2)
def two(numbers, v, viii):
    return [n for n in numbers if len(n) == 5 and n + v == viii][0]

@with_value(3)
def three(numbers, ii, v):
    return [n for n in numbers if len(n) == 5 and n != ii and n != v][0]

@with_value(0)
def zero(numbers, ii, iii, vi):
    a, b = [n for n in numbers if len(n) == 6 and n != vi]
    if a - b == ii - iii:
        return a
    else:
        return b

@with_value(9)
def nine(numbers, ii, iii, vi):
    a, b = [n for n in numbers if len(n) == 6 and n != vi]
    if a - b == ii - iii:
        return b
    else:
        return a

class Number:

    def __init__(self, code):
        if not isinstance(code, set):
            raise ValueError(f'{code} is not a set')
        self.code = code

    def __add__(self, other):
        if not isinstance(other, Number):
            raise ValueError(f'{other} is not a Number')
        return Number(self.code.union(other.code))

    def __sub__(self, other):
        if not isinstance(other, Number):
            raise ValueError(f'{other} is not a Number')
        return Number(self.code.difference(other.code))

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.code == other.code
        else:
            return False

    def __len__(self):
        return len(self.code)

    @classmethod
    def from_str(cls, code_string):
        return cls(set(c for c in code_string))

    def __repr__(self):
        normalized = ''.join(sorted(c for c in self.code))
        return f"""Number(code="{normalized}")"""

class ValuedNumber(Number):

    def __init__(self, code, value):
        super().__init__(code)
        self.value = value

    @classmethod
    def from_unvalued(cls, number, value):
        return cls(number.code, value)


class Decoder(dict):

    def __setitem__(self, key, value):
        nkey = normalize_key(key)
        super().__setitem__(nkey, value)

    def __getitem__(self, key):
        nkey = normalize_key(key)
        if nkey not in self:
            return key
        return super().__getitem__(nkey)

    @classmethod
    def with_normalized_mappings(cls, mappings):
        return cls((normalize_key(k), v) for k,v in mappings)

class Entry:

    def __init__(self, patterns, outputs):
        self.patterns = patterns
        self.outputs = outputs

    @classmethod
    def from_spec(cls, spec):
        all_patterns, all_outputs = spec.split('|')
        patterns = all_patterns.split()
        outputs = all_outputs.split()
        out_mappings = [(out, len(out)) for out in outputs if len(out) in EASY_ONES]
        pat_mappings = [(pat, len(pat)) for pat in patterns if len(pat) in EASY_ONES]
        decoder = Decoder.with_normalized_mappings(out_mappings + pat_mappings)
        translated_outputs = [decoder[out] for out in outputs]
        translated_patterns = [decoder[pat] for pat in patterns]
        return cls(translated_patterns, translated_outputs)

    def __repr__(self):
        return f'Entry(patterns="{self.patterns}", outputs={self.outputs})'

def parse_entry(spec):
    return Entry.from_spec(spec)

class Entries:

    def __init__(self, entries):
        self.entries = list(entries)

    def __len__(self):
        return len(self.entries)

    @property
    def outputs(self):
        return [entry.outputs for entry in self.entries]

    @property
    def all_outputs(self):
        return [out for outputs in self.outputs
                       for out in outputs]

def parse_entries(lns):
    specs = list(lns)
    return Entries(Entry.from_spec(spec) for spec in specs if len(spec) > 0)
