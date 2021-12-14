import logging
log = logging.getLogger(__name__)


class ParseError:

    def __init__(self, expected, found):
        self.expected = expected
        self.found = found

    @property
    def msg(self):
        return f'Expected {self.expected}, but found {self.found} instead.'

    def __repr__(self):
        return self.msg

    def __eq__(self, other):
        if isinstance(other, ParseError):
            return self.msg == other.msg
        elif isinstance(other, str):
            return self.msg == other
        else:
            return False

"""
Grammar to parse: # ref: https://en.wikipedia.org/wiki/Bracket
chunks = chunk*
chunk = round_chunk | square_chunk | curly_chunk | angle_chunk
round_chunk = left_round_bracket [+ chunks ] + right_round_bracket
square_chunk = left_square_bracket [+ chunks ] + right_square_bracket
curly_chunk = left_curly_bracket [+ chunks ] + right_curly_bracket
angle_chunk = left_angle_bracket [+ chunks ] + right_angle_bracket
"""
# but for now, might use a stack

OPENINGS = '([{<'
CLOSINGS = ')]}>'
RIGHT_PAIR = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}
LEFT_PAIR = { v:k for k,v in RIGHT_PAIR.items() }

from collections import deque

class Stack:

    def __init__(self):
        self.imp = deque()

    def push(self, item):
        log.debug(f'push: {item}')
        self.imp.append(item)

    def pop(self):
        log.debug('pop')
        return self.imp.pop()

    @property
    def top(self):
        return self.imp[-1]

    def __len__(self):
        return len(self.imp)

    def __repr__(self):
        return f'Stack({list(reversed(self.imp))})'

def parse_line(ln):
    s = Stack()
    for c in ln:
        log.debug(f'processing {c} {s}')
        if c in OPENINGS:
            s.push(c)
        elif c in CLOSINGS:
            if LEFT_PAIR[c] == s.top:
                _ = s.pop()
            else:
                return (ln, ParseError(expected=RIGHT_PAIR[s.top], found=c))
    return (ln, None)

class Subsystem:

    def __init__(self, lines):
        self.lines = list(lines)

    def __len__(self):
        return len(self.lines)

    @property
    def corrupted(self):
        return [(ln, e) for ln, e in self.lines if e is not None]

def syntax_error_score(corrupted):
    score = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    return sum(score[e.found] for _,e in corrupted)

def parse_subsystem(lns):
    return Subsystem(parse_line(ln) for ln in lns if len(ln))
