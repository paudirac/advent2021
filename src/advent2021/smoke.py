import pprint
import logging
log = logging.getLogger(__name__)

from collections import namedtuple
Size = namedtuple('Size', 'I J')

class Positions:

    def __init__(self, size):
        self.size = size

    @property
    def xys(self):
        return [(x,y) for y in range(self.size.J) for x in range(self.size.I)]

BasePosition = namedtuple('Position','x y')
class Position(BasePosition):

    def __add__(self, other):
        if not isinstance(other, (Position, BasePosition, tuple)):
            raise TypeError('Usupported operation for {type(other)}')
        assert len(other) == 2, TypeError('Unsupported operation for {type(other)}')
        x0, y0 = self
        x1, y1 = other
        return Position(x0 + x1, y0 + y1)

def inside_bounds(pos, size):
    max_x, max_y = size
    x, y = pos
    return x >= 0 and y >= 0 and x < max_x and y < max_y

def adjacent(position, size):
    up    = position + (0, -1)
    down  = position + (0, 1)
    left  = position + (-1, 0)
    right = position + (1, 0)
    neighbors = [up, down, left, right]
    return [pos for pos in neighbors if inside_bounds(pos, size)]

def is_local_min(pos, m):
    return all(m.get(a) - m.get(pos) > 0 for a in adjacent(pos, m.size))


class HeightMap:

    def __init__(self, data):
        self.data = list(data)
        assert len(self.data) > 0, "No data"
        self.I = len(self.data[0])
        assert all(len(row) == self.I for row in self.data)
        self.J = len(self.data)

    @classmethod
    def from_rows(cls, rows):
        return cls(rows)

    @property
    def size(self):
        return Size(self.I, self.J)

    def get(self, pos):
        if not isinstance(pos, (Position, BasePosition, tuple)):
            raise TypeError('Usupported operation for {type(other)}')
        size = self.size
        x, y = pos
        if not inside_bounds(pos, size):
            raise ValueError(f'{pos} is outside the bounds of {size}')
        return self.data[y][x]

    def map_positions(self, f):
        return [(x, y, f(Position(x,y), self)) for y in range(self.J) for x in range(self.I)]

    def __repr__(self):
        return f'HeightMap(rows={pprint.pformat(self.data)})'

def parse_heightmap(lns):
    rows = list(ln.strip() for ln in lns if len(ln) > 0)
    rows = [[int(c) for c in ln] for ln in rows]
    return HeightMap.from_rows(rows)

def risk_level(point):
    return point + 1
