class Swarm:

    def __init__(self, positions):
        self._positions = list(positions)

    def __len__(self):
        return len(self._positions)

    def fuel_spent(self, align_to):
        absolute_distances = [abs(pos - align_to) for pos in self._positions]
        return sum(absolute_distances)

    @property
    def bounds(self):
        return min(self._positions), max(self._positions)

    @classmethod
    def from_poitions_spec(cls, spec):
        return cls(int(pos) for pos in spec.split(','))

    def __repr__(self):
        return f'Swarm(positions={self._positions})'

class Aligner:

    def __init__(self, swarm):
        self.swarm = swarm

    def minimum_fuel(self):
        left, right = self.swarm.bounds
        fuel_spenditures = [(to, self.swarm.fuel_spent(align_to=to)) for to in range(left, right + 1)]
        return min(fuel_spenditures, key=lambda tofuel: tofuel[1])

def parse_swarm(lns):
    lns = list(lns)
    assert len(lns) == 1, "Too much data. Expected 1 line of posions, got {len(lns)}"
    return Swarm.from_poitions_spec(lns[0])
