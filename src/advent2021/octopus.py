import logging
log = logging.getLogger(__name__)

class FlashCounter:

    def __init__(self, flash_count):
        self.flash_count = flash_count

    def receive_flash(self, source):
        self.flash_count += 1

class Octopus:

    def __init__(self, energy_level, pos=None):
        assert energy_level >= 0 and energy_level <= 9, f"Invalid {energy_level=}. Expected between 0 and 9"
        self.energy_level = energy_level
        self._flash_receiver = None
        self.pos = pos

    def accept_flash_receiver(self, receiver):
        self._flash_receiver = receiver

    def step_begins(self):
        log.debug(f'step_begins {self}')
        self.already_flashed = False
        self.raise_energy(amount=1)

    def step_ends(self):
        log.debug(f'step_ends {self}')
        if self.energy_level > 9:
            assert self.already_flashed
            self.energy_level = 0

    def raise_energy(self, amount):
        assert amount == 1
        self.energy_level += amount
        log.debug(f'raised {self}')
        if self.energy_level > 9 and not self.already_flashed:
            self.flash()

    def flash(self):
        log.debug(f'flash {self}')
        if self._flash_receiver is not None:
            if not self.already_flashed:
                log.debug(f'really flash {self}')
                self.already_flashed = True
                self._flash_receiver.receive_flash(source=self)

    def __repr__(self):
        if self.pos is not None:
            return f'Octopus({(self.pos.i, self.pos.j)}, energy_level={self.energy_level})'
        else:
            return f'Octopus(energy_level={self.energy_level})'

from collections import namedtuple
Position = namedtuple('Position', 'i j')

def adjacent_to(position):
    """Return adjacent positions"""
    i, j = position
    return [
        Position(i-1, j-1), Position(i, j-1), Position(i+1, j-1),
        Position(i-1, j),                     Position(i + 1, j),
        Position(i-1, j+1), Position(i, j+1), Position(i+1, j+1),
    ]

from collections import deque

class Stack:

    def __init__(self):
        self.imp = deque()

    def push(self, item):
        self.imp.append(item)

    def pop(self):
        return self.imp.pop()

    def __len__(self):
        return len(self.imp)

    def __contains__(self, item):
        return item in self.imp


class Grid(FlashCounter):

    def __init__(self, octos, flash_count=0):
        self.step_number = 0
        super().__init__(flash_count=0)
        self.octos = dict(octos)
        for octo in self.octos.keys():
            octo.accept_flash_receiver(self)
        self.positions = { v:k for k,v in self.octos.items() }

    def steps(self, number):
        for _ in range(number):
            self.step()

    def step(self):
        self.flash_sources = Stack()
        self.step_number += 1
        log.debug(f'******** begin step {self.step_number}')
        for octo,pos in self.octos.items():
            octo.step_begins()
        while len(self.flash_sources):
            octo = self.flash_sources.pop()
            self.process_flash(octo)
        for octo, pos in self.octos.items():
            octo.step_ends()
        log.debug(f'******** end step {self.step_number}')

    def receive_flash(self, source):
        super().receive_flash(source)
        if source not in self.flash_sources:
            self.flash_sources.push(source)

    def process_flash(self, source):
        location = self.octos[source]
        # log.debug(f'{(location.i, location.j)} flashed')
        adjacent_positions = adjacent_to(location)
        # log.debug(f'flashing to {len(adjacent_positions)} positions')
        log.debug(f'{[(i, j) for i,j in adjacent_positions]}')
        for pos in adjacent_positions:
            log.debug(f'trying to propagate flash to {(pos.i, pos.j)}')
            if pos in self.positions:
                log.debug(f'propagate flash to {(pos.i, pos.j)}')
                self.positions[pos].raise_energy(1)

    @classmethod
    def from_config(cls, config):
        return cls(octos={Octopus(energy, pos): pos for item in config for pos, energy in item})

def parse_grid_config(lns):
    lns = list(ln.strip() for ln in lns if len(ln) > 0)
    lns = list(ln for ln in lns if len(ln))
    return [
        [(Position(i, j), int(energy)) for i, energy in enumerate(ln)]
        for j, ln in enumerate(lns)
    ]
