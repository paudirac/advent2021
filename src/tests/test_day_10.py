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
    syntax_error_score,
    completion_score,
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

def test_syntax_error_score():
    lns = mk_lines(sample_data)
    subsystem = parse_subsystem(lns)
    assert len(subsystem) == 10
    assert len(subsystem.corrupted) == 5
    assert syntax_error_score(subsystem.corrupted) == 26397

def test_stack_remaining_join():
    s = Stack()
    s.push('a')
    s.push('b')
    s.push('c')
    assert str(s) == 'cba'

@pytest.mark.parametrize(
    'ln, remaining, score', [
        ("[({(<(())[]>[[{[]{<()<>>", "Complete by adding }}]])})].", 288957),
        ("[(()[<>])]({[<{<<[]>>(", "Complete by adding )}>]}).", 5566),
        ("(((({<>}<{<{<>}{[]{[]{}", "Complete by adding }}>}>)))).", 1480781),
        ("{<[[]]>}<{[{[{[]{()[[[]", "Complete by adding ]]}}]}]}>.", 995444),
        ("<{([{{}}[<[[[<>{}]]]>[]]", "Complete by adding ])}>.", 294) ,
    ]
)
def test_parse_incomplete_line(ln, remaining, score):
    log.debug(f'{ln=}')
    log.debug(f'{remaining=}')
    (ln, completion), e = parse_line(ln)
    assert e is None
    assert completion is not None
    assert f"Complete by adding {completion}." == remaining
    assert completion_score(completion) == score

def test_incomplete_lines():
    lns = mk_lines(sample_data)
    subsystem = parse_subsystem(lns)
    assert len(subsystem) == 10
    assert len(subsystem.corrupted) == 5
    assert len(subsystem.incomplete) == 5
    scores = list(sorted([completion_score(c) for _,c in subsystem.incomplete]))
    middle_score = scores[int(len(scores)/2)]
    assert middle_score == 288957
