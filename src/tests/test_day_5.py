from advent2021.vents import (
    parse_line_defs,
    LineDef,
    new_lines,
    Diagram,
    Position,
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
    assert LineDef.from_spec("0,9 -> 5,9") == LineDef(0, 9, 5, 9)

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

def test_lines():
    lns = mk_lines(sample_data)
    lines = new_lines(lns)
    top_left, bottom_right = lines.bounds()
    assert top_left == (0, 0)
    assert bottom_right == (9, 9)

def test_diagram():
    lns = mk_lines(sample_data)
    lines = new_lines(lns)
    diagram = Diagram(lines.bounds())
    top_left, bottom_right = diagram.bounds
    assert top_left == (0, 0)
    assert bottom_right == (9, 9)
    x0, y0 = top_left
    x1, y1 = bottom_right
    for x in range(top_left.x, bottom_right.x + 1):
        for y in range(top_left.y, bottom_right.y + 1):
            assert diagram.get(Position(x, y)) == 0

def test_position_is_hashable():
    pos1 = Position(42, 0)
    pos2 = Position(42, 0)
    pos3 = Position(42, 42)
    sentinel = object()
    d = {
        pos1: 42,
    }
    assert d[pos1] == 42
    assert d[pos2] == 42
    assert d.get(pos3, sentinel) == sentinel

def test_draw_line_on_diagram():
    lns = mk_lines(sample_data)
    lines = new_lines(lns)
    diagram = Diagram(lines.bounds())
    top_left, bottom_right = diagram.bounds
    assert top_left == (0, 0)
    assert bottom_right == (9, 9)
    line = LineDef.from_spec("0,9 -> 5,9")
    diagram.draw(line)
    assert diagram.get(Position(0,9)) == 1
    assert diagram.get(Position(1,9)) == 1
    assert diagram.get(Position(2,9)) == 1
    assert diagram.get(Position(3,9)) == 1
    assert diagram.get(Position(4,9)) == 1
    assert diagram.get(Position(5,9)) == 1
    greater_or_1 = diagram.positions_with(lambda count: count >= 1)
    assert len(greater_or_1) == 6

def test_at_least_two_lines():
    lns = mk_lines(sample_data)
    lines = new_lines(lns)
    diagram = Diagram(lines.bounds())
    top_left, bottom_right = diagram.bounds
    assert top_left == (0, 0)
    assert bottom_right == (9, 9)
    for line in lines:
        diagram.draw(line)
    at_least_two_lines = lambda count: count >= 2
    pos_with_at_least_two_lines = diagram.positions_with(at_least_two_lines)
    assert len(pos_with_at_least_two_lines) == 5

def test_draw_non_horizontal_or_diagonal_line_on_diagram():
    lns = mk_lines(sample_data)
    lines = new_lines(lns)
    diagram = Diagram(lines.bounds())
    top_left, bottom_right = diagram.bounds
    assert top_left == (0, 0)
    assert bottom_right == (9, 9)
    line = LineDef.from_spec("1,1 -> 3,3")
    diagram.draw(line)
    assert diagram.get(Position(1,1)) == 1
    assert diagram.get(Position(2,2)) == 1
    assert diagram.get(Position(3,3)) == 1
    #line = LineDef.from_spec("9,7 -> 7,9")
    #
def test_draw_non_horizontal_or_diagonal_line_on_diagram_missing_importan_one_joy():
    #👼
    lns = mk_lines(sample_data)
    lines = new_lines(lns)
    diagram = Diagram(lines.bounds())
    top_left, bottom_right = diagram.bounds
    assert top_left == (0, 0)
    assert bottom_right == (9, 9)
    line = LineDef.from_spec("9,7 -> 7,9")
    diagram.draw(line)
    assert diagram.get(Position(9,7)) == 1
    assert diagram.get(Position(8,8)) == 1
    assert diagram.get(Position(7,9)) == 1


import logging
log = logging.getLogger(__name__)

def xtest_at_least_two_lines_also_diagonal():
    log.debug('---------------------------')
    lns = mk_lines(sample_data)
    lines = new_lines(lns, condition=lambda linedef: True)
    diagram = Diagram(lines.bounds())
    top_left, bottom_right = diagram.bounds
    assert top_left == (0, 0)
    assert bottom_right == (9, 9)
    for line in lines:
        diagram.draw(line)
    at_least_two_lines = lambda count: count >= 2
    pos_with_at_least_two_lines = diagram.positions_with(at_least_two_lines)
    log.debug(f'{diagram=}')
    assert len(pos_with_at_least_two_lines) == 12
    log.debug('---------------------------')
