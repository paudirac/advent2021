"""
This is probably overkill, because vector sum is both commutative and associative.
So components can be summed separately and values can be grouped together at your own will.

But we've here to have some fun, haven't we?
"""
from collections import namedtuple

forward = namedtuple('forward', ['arg'])
down = namedtuple('down', ['arg'])
up = namedtuple('up', ['arg'])

Position = namedtuple('Position', ['x', 'y'])
cmds = (forward, up, down,)

def move(position, movement):
    if isinstance(movement, forward):
        return Position(x=position.x + movement.arg, y=position.y)
    elif isinstance(movement, up):
        return Position(x=position.x, y=position.y - movement.arg)
    elif isinstance(movement, down):
        return Position(x=position.x, y=position.y + movement.arg)
    else:
        raise Exception(f'Invalid movement {movement}')

class Submarine:

    def __init__(self, initial):
        self.position = initial

    def process(self, cmd):
        if isinstance(cmd, cmds):
            self.position = move(self.position, cmd)
        else:
            raise Exception(f'Unknown command {cmd}')

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
