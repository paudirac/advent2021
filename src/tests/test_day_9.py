import pytest

import logging
log = logging.getLogger(__name__)

sample_data = """2199943210
3987894921
9856789892
8767896789
9899965678
"""

def mk_lines(s):
    for line in s.split('\n'):
        yield line

from advent2021.smoke import (
    parse_heightmap,
    risk_level,
    Size,
    Positions,
    adjacent,
    Position,
    is_local_min,
    grad,
    walk_from_while,
    less_than_9,
)

def test_risklevel():
    lowpoints = [1, 0, 5, 5]
    risk_levels = [risk_level(point) for point in lowpoints]
    assert risk_levels == [2, 1, 6, 6]
    assert sum(risk_levels) == 15

def test_locations():
    size = Size(4, 3)
    positions = Positions(size)
    xys = positions.xys
    assert xys == [
        (0,0), (1,0), (2, 0), (3, 0),
        (0,1), (1,1), (2, 1), (3, 1),
        (0,2), (1,2), (2, 2), (3, 2),
    ]

def test_position_arithmetic():
    pos1 = Position(0, 0)
    pos2 = Position(1, 0)
    assert pos1 + pos2 == (1, 0)
    assert pos1 + (0, 1) == (0, 1)

def test_adjacent():
    size = Size(4, 3)
    assert adjacent(Position(1, 1), size) == [
        (1, 0), # up
        (1, 2), # down
        (0, 1), # left
        (2, 1), # right
    ]
    assert adjacent(Position(0, 0), size) == [
        (0, 1),
        (1, 0)
    ]
    assert adjacent(Position(3, 0), size) == [
        (3, 1),
        (2, 0),
    ]
    assert adjacent(Position(0, 2), size) == [
        (0, 1),
        (1, 2),
    ]
    assert adjacent(Position(3, 2), size) == [
        (3, 1),
        (2, 2),
    ]
    assert adjacent(Position(1, 0), size) == [
        (1, 1),
        (0, 0),
        (2, 0),
    ]
    assert adjacent(Position(1, 2), size) == [
        (1, 1),
        (0, 2),
        (2, 2),
    ]
    assert adjacent(Position(0, 1), size) == [
        (0, 0),
        (0, 2),
        (1, 1),
    ]
    assert adjacent(Position(3, 1), size) == [
        (3, 0),
        (3, 2),
        (2, 1),
    ]

def test_lowpoints():
    lns = mk_lines(sample_data)
    heightmap = parse_heightmap(lns)
    assert heightmap.size == (10, 5)
    assert heightmap.get(Position(0, 2)) == 9
    assert heightmap.get(Position(8, 4)) == 7
    log.debug(f'{heightmap=}')

    local_mins = heightmap.map_positions(is_local_min)
    low_points = [heightmap.get((x, y)) for x,y,is_min in local_mins if is_min]
    log.debug(f'{low_points=}')
    assert low_points == [1, 0, 5, 5]
    assert sum(map(risk_level, low_points)) == 15

def test_max_basins():
    lns = mk_lines(sample_data)
    heightmap = parse_heightmap(lns)
    local_mins_map = heightmap.map_positions(is_local_min)
    local_mins = [Position(x,y) for x,y,is_min in local_mins_map if is_min]
    log.debug(f'{local_mins=}')
    basins = [walk_from_while(pos, less_than_9, heightmap) for pos in local_mins]
    log.debug(f'{basins=}')
    basins_lengths = sorted([len(basin) for basin in basins], reverse=True)
    log.debug(f'{basins_lengths=}')
    from functools import reduce
    assert reduce(lambda x,y: x * y, basins_lengths[:3]) == 1134

def test_walk_from():
    lns = mk_lines(sample_data)
    heightmap = parse_heightmap(lns)
    basin = walk_from_while(Position(1, 0), less_than_9, heightmap, visited=[])
    log.debug(f'{basin=}')
    assert len(basin) == 3
    basin = walk_from_while(Position(9, 0), less_than_9, heightmap, visited=[])
    assert len(basin) == 9
    log.debug(f'{basin=}')
    basin = walk_from_while(Position(2, 2), less_than_9, heightmap, visited=[])
    assert len(basin) == 14
    log.debug(f'{basin=}')
    basin = walk_from_while(Position(6, 4), less_than_9, heightmap, visited=[])
    assert len(basin) == 9
