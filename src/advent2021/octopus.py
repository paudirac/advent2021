import logging
log = logging.getLogger(__name__)

class Octopus:

    def __init__(self, energy_level):
        assert energy_level >= 0 and energy_level <= 9, f"Invalid {energy_level=}. Expected between 0 and 9"
        self.energy_level = energy_level

    def step_begins(self):
        self.energy_level += 1

    def step_ends(self):
        if self.flashing:
            self.energy_level = 0

    @property
    def flashing(self):
        return self.energy_level >= 9

    def __repr__(self):
        return f'Octopus(energy_level={self.energy_level})'
