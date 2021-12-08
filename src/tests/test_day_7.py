import logging
log = logging.getLogger(__name__)

from advent2021.crabs import (
    parse_swarm,
    Aligner,
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
    assert swarm.fuel_spent(align_to=2) == 37
    left, right = swarm.bounds
    fuel_spenditures = [(to, swarm.fuel_spent(align_to=to)) for to in range(left, right + 1)]
    assert all(fuel >= 37 for _,fuel in fuel_spenditures)

def test_minimum_fuel():
    lns = mk_lines(sample_data)
    swarm = parse_swarm(lns)
    aligner = Aligner(swarm)
    (pos, fuel) = aligner.minimum_fuel()
    assert pos == 2
    assert fuel == 37
