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
        self.imp.append(item)

    def pop(self):
        return self.imp.pop()

    @property
    def top(self):
        return self.imp[-1]

    def __len__(self):
        return len(self.imp)

    def __str__(self):
        return ''.join(list(reversed(self.imp)))

    def __repr__(self):
        return f'Stack({list(reversed(self.imp))})'

class Completion:

    def __init__(self, completion):
        self.completion = completion

    def __repr__(self):
        return self.completion

    def __eq__(self, other):
        if isinstance(other, Completion):
            return self.completion == other.completion
        elif isinstance(other, str):
            return self.completion == other
        else:
            return False

def parse_line(ln):
    s = Stack()
    for c in ln:
        if c in OPENINGS:
            s.push(c)
        elif c in CLOSINGS:
            if LEFT_PAIR[c] == s.top:
                _ = s.pop()
            else:
                return ((ln, None), ParseError(expected=RIGHT_PAIR[s.top], found=c))
    if len(s) > 0:
        t = str.maketrans(OPENINGS, CLOSINGS)
        return ((ln, str(s).translate(t)), None)
    return ((ln, None), None)

class Subsystem:

    def __init__(self, lines):
        self.lines = list(lines)

    def __len__(self):
        return len(self.lines)

    @property
    def corrupted(self):
        return [(ln, e) for ln, e in self.lines if e is not None]

    @property
    def incomplete(self):
        return [(ln, c) for (ln, c), e in self.lines if e is None and c is not None]

def syntax_error_score(corrupted):
    score = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    return sum(score[e.found] for _,e in corrupted)

def completion_score(completion):
    score = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    total_score = 0
    for c in completion:
        total_score *= 5
        total_score += score[c]
    return total_score


def parse_subsystem(lns):
    return Subsystem(parse_line(ln) for ln in lns if len(ln))
