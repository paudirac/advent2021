def constant_rate(_from, to):
    return abs(_from - to)

def increasing_rate(_from, to):
    delta = abs(_from - to)
    return sum(i for i in range(1, delta + 1))

class Swarm:

    def __init__(self, positions):
        self._positions = list(positions)

    def __len__(self):
        return len(self._positions)

    def fuel_spent(self, align_to, individual_cost):
        individual_costs = [individual_cost(pos, align_to) for pos in self._positions]
        return sum(individual_costs)

    @property
    def bounds(self):
        return min(self._positions), max(self._positions)

    @classmethod
    def from_poitions_spec(cls, spec):
        return cls(int(pos) for pos in spec.split(','))

    def __repr__(self):
        return f'Swarm(positions={self._positions})'

class Aligner:

    def __init__(self, swarm, individual_cost=constant_rate):
        self.swarm = swarm
        self.individual_cost = individual_cost

    def minimum_fuel(self):
        left, right = self.swarm.bounds
        individual_cost = self.individual_cost
        fuel_spenditures = [(to, self.swarm.fuel_spent(align_to=to, individual_cost=individual_cost)) for to in range(left, right + 1)]
        return min(fuel_spenditures, key=lambda tofuel: tofuel[1])

def parse_swarm(lns):
    lns = list(lns)
    assert len(lns) == 1, "Too much data. Expected 1 line of posions, got {len(lns)}"
    return Swarm.from_poitions_spec(lns[0])
