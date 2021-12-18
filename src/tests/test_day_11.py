import pytest

import logging
log = logging.getLogger(__name__)

def mk_lines(s):
    for line in s.split('\n'):
        yield line

from advent2021.octopus import (
    Octopus,
    FlashCounter,
    Position,
    parse_grid_config,
    Grid,
    ResetGrid,
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
    flash_counter = FlashCounter(flash_count=0)
    assert flash_counter.flash_count == 0
    octopus = Octopus(9)
    octopus.accept_flash_receiver(flash_counter)
    octopus.step_begins()
    octopus.step_ends()
    assert octopus.energy_level == 0
    assert flash_counter.flash_count == 1
    energy_steps = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)]
    for _, energy in energy_steps:
        octopus.step_begins()
        octopus.step_ends()
        assert octopus.energy_level == energy
    octopus.step_begins()
    octopus.step_ends()
    assert octopus.energy_level == 9
    assert flash_counter.flash_count == 1

litte_sample_data = """11111
19991
19191
19991
11111
"""

def test_little_grid():
    lns = mk_lines(litte_sample_data)
    grid_config = parse_grid_config(lns)
    log.debug(f'{grid_config=}')
    log.debug(f'{grid_config[2]=}')
    assert grid_config[2] == [
        (Position(0, 2), 1),
        (Position(1, 2), 9),
        (Position(2, 2), 1),
        (Position(3, 2), 9),
        (Position(4, 2), 1),
    ]

def test_litte_grid_evolution():
    lns = mk_lines(litte_sample_data)
    grid_config = parse_grid_config(lns)
    grid = Grid.from_config(grid_config)
    assert grid.flash_count == 0
    grid.step()
    assert grid.flash_count == 9
    grid.step()
    assert grid.flash_count == 9


sample_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

def test_grid_evolution():
    lns = mk_lines(sample_data)
    grid_config = parse_grid_config(lns)
    grid = Grid.from_config(grid_config)
    assert grid.flash_count == 0
    grid.steps(100)
    assert grid.flash_count == 1656

def test_grid_evolve_till_all_flash():
    lns = mk_lines(sample_data)
    grid_config = parse_grid_config(lns)
    grid = ResetGrid.from_config(grid_config)
    assert grid.flash_count == 0
    grid.stop_when_all_flash()
    assert grid.step_number == 195
