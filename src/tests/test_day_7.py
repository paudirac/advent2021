import logging
log = logging.getLogger(__name__)

from advent2021.crabs import (
    parse_swarm,
    Aligner,
    constant_rate,
    increasing_rate,
)

def mk_lines(s):
    for line in s.split('\n'):
        yield line


sample_data = """16,1,2,0,4,2,7,1,2,14"""

def test_parse_swarm():
    lns = mk_lines(sample_data)
    swarm = parse_swarm(lns)
    assert len(swarm) == 10
    left, right = swarm.bounds
    assert left == 0
    assert right == 16

def test_fuel_to_2():
    lns = mk_lines(sample_data)
    swarm = parse_swarm(lns)
    assert swarm.fuel_spent(align_to=2, individual_cost=constant_rate) == 37
    left, right = swarm.bounds
    fuel_spenditures = [(to, swarm.fuel_spent(align_to=to, individual_cost=constant_rate)) for to in range(left, right + 1)]
    assert all(fuel >= 37 for _,fuel in fuel_spenditures)

def test_minimum_fuel():
    lns = mk_lines(sample_data)
    swarm = parse_swarm(lns)
    aligner = Aligner(swarm)
    (pos, fuel) = aligner.minimum_fuel()
    assert pos == 2
    assert fuel == 37

import pytest

@pytest.mark.parametrize(
    '_from, to, fuel',[
        (16, 2, 14,),
        (1, 2, 1,),
        (2, 2, 0,),
        (0, 2, 2,),
        (4, 2, 2,),
        (2, 2, 0,),
        (7, 2, 5,),
        (1, 2, 1,),
        (2, 2, 0,),
        (14, 2, 12,),
    ]
)
def test_constant_rate(_from, to, fuel):
    assert constant_rate(_from, to) == fuel

@pytest.mark.parametrize(
    '_from, to, fuel', [
        (16, 5, 66,),
        (1, 5, 10,),
        (2, 5, 6,),
        (0, 5, 15,),
        (4, 5, 1,),
        (2, 5, 6,),
        (7, 5, 3,),
        (1, 5, 10,),
        (2, 5, 6,),
        (14, 5, 45,),
    ]
)
def test_increasing_rate(_from, to, fuel):
    assert increasing_rate(_from, to) == fuel

def test_minimum_fuel():
    lns = mk_lines(sample_data)
    swarm = parse_swarm(lns)
    aligner = Aligner(swarm, individual_cost=increasing_rate)
    (pos, fuel) = aligner.minimum_fuel()
    assert pos == 5
    assert fuel == 168
