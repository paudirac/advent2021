import pytest

import logging
log = logging.getLogger(__name__)

from advent2021.caves import (
    parse_rough_map,
    Cave,
    Conn,
)

def mk_lines(s):
    for line in s.split('\n'):
        yield line

sample_data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

def test_caves():
    lns = mk_lines(sample_data)
    caves = parse_rough_map(lns)
    assert len(caves.conns) == 7
    assert len(caves.caves) == 6
    assert Cave('start') in caves
    assert Cave('A') in caves
    assert Cave('b') in caves
    assert Cave('c') in caves
    assert Cave('d') in caves
    assert Cave('end') in caves

def test_conns():
    conn = Conn('a-b')
    assert conn.ends == { Cave('a'), Cave('b') }

def test_connections():
    lns = mk_lines(sample_data)
    caves = parse_rough_map(lns)
    assert caves.connections(Cave('start')) == { Cave('A'), Cave('b') }
    assert caves.connections(Cave('A')) == { Cave('start'), Cave('b'), Cave('c'), Cave('end') }
    assert caves.connections(Cave('b')) == { Cave('start'), Cave('A'), Cave('d'), Cave('end') }
    assert caves.connections(Cave('c')) == { Cave('A') }
    assert caves.connections(Cave('d')) == { Cave('b') }
