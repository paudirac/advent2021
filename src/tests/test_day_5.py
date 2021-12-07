from advent2021.vents import (
    parse_line_defs,
    LineDef,

    _parse_line_def,
)

def mk_lines(s):
    for line in s.split('\n'):
        yield line

sample_data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

def test_parse_line_def():
    assert _parse_line_def("0,9 -> 5,9") == LineDef(0, 9, 5, 9)

def test_parse_line_def():
    lns = mk_lines(sample_data)
    line_defs = parse_line_defs(lns)
    assert len(line_defs) == 10
    assert line_defs == [
        LineDef(0,9,5,9),
        LineDef(8,0,0,8),
        LineDef(9,4,3,4),
        LineDef(2,2,2,1),
        LineDef(7,0,7,4),
        LineDef(6,4,2,0),
        LineDef(0,9,2,9),
        LineDef(3,4,1,4),
        LineDef(0,0,8,8),
        LineDef(5,5,8,2),
    ]

def test_is_horizontal_is_vertical():
    horizontal = LineDef(0, 42, 42, 42)
    assert horizontal.is_horizontal
    assert not horizontal.is_vertical
    vertical = LineDef(42, 42, 42, 0)
    assert vertical.is_vertical
    assert not vertical.is_horizontal
    diagonal = LineDef(0, 0, 42, 42)
    assert not diagonal.is_horizontal
    assert not diagonal.is_vertical
