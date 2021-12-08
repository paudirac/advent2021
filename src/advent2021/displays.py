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
        patterns, all_outputs = spec.split('|')
        outputs = all_outputs.split()
        mappings = [(out, len(out)) for out in outputs if len(out) in EASY_ONES]
        decoder = Decoder.with_normalized_mappings(mappings)
        translated_outputs = [decoder[out] for out in outputs]
        return cls(patterns.strip(), translated_outputs)

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
