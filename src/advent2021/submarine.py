"""
This is probably overkill, because vector sum is both commutative and associative.
So components can be summed separately and values can be grouped together at your own will.

But we've here to have some fun, haven't we?
"""
import logging
log = logging.getLogger(__name__)

from collections import namedtuple

forward = namedtuple('forward', ['arg'])
down = namedtuple('down', ['arg'])
up = namedtuple('up', ['arg'])

Position = namedtuple('Position', ['x', 'y'])
AimPosition = namedtuple('Position', ['x', 'y', 'aim'])
cmds = (forward, up, down,)

class Submarine:

    def __init__(self, initial):
        self.position = initial

    def process(self, cmd):
        if isinstance(cmd, cmds):
            self.position = self._next_move(self.position, cmd)
        else:
            raise Exception(f'Unknown command {cmd}')

    def _next_move(self, current, movement):
        if isinstance(movement, forward):
            return Position(x=current.x + movement.arg, y=current.y)
        elif isinstance(movement, up):
            return Position(x=current.x, y=current.y - movement.arg)
        elif isinstance(movement, down):
            return Position(x=current.x, y=current.y + movement.arg)
        else:
            raise Exception(f'Invalid movement {movement}')


class AimSubmarine(Submarine):

    def _next_move(self, current, movement):
        if isinstance(movement, forward):
            return AimPosition(x=current.x + movement.arg, y=current.y + current.aim * movement.arg, aim=current.aim)
        elif isinstance(movement, up):
            return AimPosition(x=current.x, y=current.y, aim=current.aim - movement.arg)
        elif isinstance(movement, down):
            return AimPosition(x=current.x, y=current.y, aim=current.aim + movement.arg)
        else:
            raise Exception(f'Invalid movement {movement}')


def new_submarine(initial):
    if hasattr(initial, 'aim'):
        return AimSubmarine(initial)
    else:
        return Submarine(initial)

def token(op, arg):
    return {
        'forward': forward,
        'down': down,
        'up': up,
    }[op](arg=arg)

def tokenize(lines):
    for line in lines:
        try:
            op, arg = line.split()
            yield token(op=op,arg=int(arg))
        except:
            pass
