import logging

log = logging.getLogger(__name__)

from dataclasses import dataclass
from collections import namedtuple

def _clean_specs(lns):
    import re
    _IS_BLANK = re.compile(r'\s+$')

    def is_blank(line):
        return _IS_BLANK.match(line) or len(line) == 0

    return list(ln for ln in lns if not is_blank(ln))

@dataclass(frozen=True)
class LineDef:
    x0: int
    y0: int
    x1: int
    y1: int

    @property
    def is_horizontal(self):
        return self.y0 == self.y1

    @property
    def is_vertical(self):
        return self.x0 == self.x1

    @classmethod
    def from_spec(cls, spec):
        left, right = spec.split('->')
        x0,y0 = left.strip().split(',')
        x1, y1 = right.strip().split(',')
        return LineDef(int(x0), int(y0), int(x1), int(y1))


Position = namedtuple('Position', 'x y')

class Diagram:

    def __init__(self, bounds):
        self.bounds = bounds
        self.positions = self._initialize_positions(self.bounds, value=0)

    def get(self, position):
        return self.positions[position]

    def _initialize_positions(self, bounds, value):
        top_left, bottom_right = bounds
        xs = range(top_left.x, bottom_right.x + 1)
        ys = range(top_left.y, bottom_right.y + 1)
        return { Position(x,y): value for x in xs for y in ys }

    def draw(self, line):
        min_x = min(line.x0, line.x1)
        max_x = max(line.x0, line.x1)
        min_y = min(line.y0, line.y1)
        max_y = max(line.y0, line.y1)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                pos = Position(x,y)
                self.positions[pos] += 1

    def positions_with(self, condition):
        return [pos for pos,value in self.positions.items() if condition(value)]

class Lines:

    def __init__(self, defs):
        self.defs = list(defs)

    def bounds(self):
        all_xs = set(spec.x0 for spec in self.defs).union(set(spec.x1 for spec in self.defs))
        all_ys = set(spec.y0 for spec in self.defs).union(set(spec.y1 for spec in self.defs))
        min_x = min(all_xs)
        min_y = min(all_ys)
        max_x = max(all_xs)
        max_y = max(all_ys)
        return Position(min_x, min_y), Position(max_x, max_y)

    def __iter__(self):
        self.__defs_iter = iter(self.defs)
        return self

    def __next__(self):
        return next(self.__defs_iter)

def parse_line_defs(lns):
    specs = _clean_specs(lns)
    return [LineDef.from_spec(spec) for spec in specs]

def new_lines(lns):
    defs = parse_line_defs(lns)
    return Lines(linedef for linedef in defs if linedef.is_horizontal or linedef.is_vertical)
