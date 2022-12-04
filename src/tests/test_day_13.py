import pytest

import logging
log = logging.getLogger(__name__)

from advent2021.origami import (
    parse_paper_instructions,
)

def mk_lines(s):
    for line in s.split('\n'):
        yield line

sample_data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


def test_parse_origami():
    lns = mk_lines(sample_data)
    paper, instructions = parse_paper_instructions(lns)
    assert paper
    assert len(instructions) == 2
