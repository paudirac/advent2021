import pytest

import logging
log = logging.getLogger(__name__)

sample_data = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

def mk_lines(s):
    for line in s.split('\n'):
        yield line

from advent2021.navigation import (
    parse_subsystem,
    parse_line,
    Stack,
)


def test_parse_navigation_subsystem():
    lns = mk_lines(sample_data)
    subsystem = parse_subsystem(lns)
    assert len(subsystem) == 10

@pytest.mark.parametrize(
    'ln, error', [
        ("{([(<{}[<>[]}>{[]{[(<()>", "Expected ], but found } instead."),
        ("[[<[([]))<([[{}[[()]]]",   "Expected ], but found ) instead."),
        ("[{[{({}]{}}([{[{{{}}([]",  "Expected ), but found ] instead."),
        ("[<(<(<(<{}))><([]([]()",   "Expected >, but found ) instead."),
        ("<{([([[(<>()){}]>(<<{{",   "Expected ], but found > instead."),
    ]
)
def test_parse_line(ln, error):
    chunks, err = parse_line(ln)
    assert err == error

def test_stack():
    s = Stack()
    s.push(42)
    s.push('life')
    s.push('meaning')
    assert len(s) == 3
    assert s.pop() == 'meaning'
    assert len(s) == 2
    assert s.pop() == 'life'
    assert len(s) == 1
    assert s.pop() == 42
    assert len(s) == 0
    with pytest.raises(IndexError):
        s.pop()
