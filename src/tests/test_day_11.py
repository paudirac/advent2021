import pytest

import logging
log = logging.getLogger(__name__)

sample_data = """
"""

def mk_lines(s):
    for line in s.split('\n'):
        yield line

from advent2021.octopus import (
    Octopus,
)

def test_each_octopus_has_an_energy_level():
    octopus = Octopus(8)
    assert hasattr(octopus, 'energy_level')

@pytest.mark.parametrize(
    'energy_level',
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,]
)
def test_octopus_energy_level_between_0_and_9_is_ok(energy_level):
    octopus = Octopus(energy_level)
    assert octopus.energy_level == energy_level

def test_octopus_energy_level_outside_0_and_9_is_not_ok():
    with pytest.raises(Exception):
        Octopus(-1)
    with pytest.raises(Exception):
        Octopus(10)

def test_octopus_increases_energy_level_by_1_on_any_step():
    octopus = Octopus(0)
    energy_steps = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
    for _, energy in energy_steps:
        octopus.step_begins()
        assert octopus.energy_level == energy
        octopus.step_ends()

def test_octopus_flashes_beyond_9():
    octopus = Octopus(9)
    octopus.step_begins()
    assert octopus.flashing
    octopus.step_ends()
    assert octopus.energy_level == 0
