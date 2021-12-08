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

class Entry:

    def __init__(self, patterns, outputs):
        self.patterns = patterns
        self.outputs = outputs

    @classmethod
    def from_spec(cls, spec):
        patterns, outputs = spec.split('|')
        return cls(patterns.strip(), outputs.split())

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
    return Entries(parse_entry(spec) for spec in specs if len(spec) > 0)

# Assuming active_segments do not contain repeated values
def is_1(active_segments): return len(active_segments) == 2
def is_4(active_segments): return len(active_segments) == 4
def is_7(active_segments): return len(active_segments) == 3
def is_8(active_segments): return len(active_segments) == 7

EASY_CONDITIONS = [is_1, is_4, is_7, is_8]
def is_easy(active_segments):
    return any(check(active_segments) for check in EASY_CONDITIONS)
