import logging
log = logging.getLogger(__name__)

from advent2021.lanternfish import (
    parse_initial_population,
    Population,
)

def mk_lines(s):
    for line in s.split('\n'):
        yield line

sample_data = """3,4,3,1,2"""

def test_initial_population():
    lns = mk_lines(sample_data)
    population = parse_initial_population(lns)
    assert len(population) == 5
    assert population.clocks == [3,4,3,1,2]
    assert population.day == 0

def test_one_lanternfish():
    population = Population.from_clocks([3])
    log.debug(f'{population}')
    assert len(population) == 1
    assert population.clocks == [3]
    assert population.day == 0

    population.get_old()
    log.debug(f'{population}')
    assert population.day == 1
    assert len(population) == 1
    assert population.clocks == [2]

    population.get_old()
    log.debug(f'{population}')
    assert population.day == 2
    assert len(population) == 1
    assert population.clocks == [1]

    population.get_old()
    log.debug(f'{population}')
    assert population.day == 3
    assert len(population) == 1
    assert population.clocks == [0]

    population.get_old()
    log.debug(f'{population}')
    assert population.day == 4
    assert len(population) == 2
    assert population.clocks == [6, 8]

def test_get_old_18_days():
    lns = mk_lines(sample_data)
    population = parse_initial_population(lns)
    assert len(population) == 5
    assert population.clocks == [3,4,3,1,2]
    assert population.day == 0
    population.get_old(days=18)
    log.debug(f'{population}')
    assert len(population) == 26
    sample_population_clocks_18 = [6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8]
    assert len(population) == len(sample_population_clocks_18)
    assert population.clocks == sample_population_clocks_18
    population.get_old(days=80-18)
    assert population.day == 80
    assert len(population) == 5934
    #log.debug(f'{population}')
