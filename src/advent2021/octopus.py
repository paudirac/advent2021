import logging
log = logging.getLogger(__name__)

class FlashCounter:

    def __init__(self, flash_count):
        self.flash_count = flash_count

    def receive_flash(self, source):
        log.debug(f'{source=} has flashed')
        self.flash_count += 1

class Octopus:

    def __init__(self, energy_level):
        assert energy_level >= 0 and energy_level <= 9, f"Invalid {energy_level=}. Expected between 0 and 9"
        self.energy_level = energy_level
        self._flash_receiver = None

    def accept_flash_receiver(self, receiver):
        self._flash_receiver = receiver

    def step_begins(self):
        self.already_flashed = False
        self.raise_energy(amount=1)

    def step_ends(self):
        if self.already_flashed:
            self.energy_level = 0

    def raise_energy(self, amount):
        self.energy_level += amount
        if self.energy_level >= 9 and not self.already_flashed:
            self.already_flashed = True
            self.flash()

    def flash(self):
        if self._flash_receiver is not None:
            self._flash_receiver.receive_flash(source=self)

    def __repr__(self):
        return f'Octopus(energy_level={self.energy_level})'

