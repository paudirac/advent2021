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

def move_without_aim(position, movement):
    if isinstance(movement, forward):
        return Position(x=position.x + movement.arg, y=position.y)
    elif isinstance(movement, up):
        return Position(x=position.x, y=position.y - movement.arg)
    elif isinstance(movement, down):
        return Position(x=position.x, y=position.y + movement.arg)
    else:
        raise Exception(f'Invalid movement {movement}')

def move_with_aim(position, movement):
    if isinstance(movement, forward):
        return AimPosition(x=position.x + movement.arg, y=position.y + position.aim * movement.arg, aim=position.aim)
    elif isinstance(movement, up):
        return AimPosition(x=position.x, y=position.y, aim=position.aim - movement.arg)
    elif isinstance(movement, down):
        return AimPosition(x=position.x, y=position.y, aim=position.aim + movement.arg)
    else:
        raise Exception(f'Invalid movement {movement}')

class Submarine:

    def __init__(self, initial):
        self.position = initial
        if hasattr(initial, 'aim'):
            self.move = move_with_aim
        else:
            self.move = move_without_aim

    def process(self, cmd):
        move = self.move
        if isinstance(cmd, cmds):
            self.position = move(self.position, cmd)
            log.debug(f'{cmd} {self.position}')
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
