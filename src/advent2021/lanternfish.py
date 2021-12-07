import logging
log = logging.getLogger(__name__)

class Population:

    def __init__(self, clocks):
        clocks = list(clocks)
        self._population = {
            0: sum(1 for clock in clocks if clock == 0),
            1: sum(1 for clock in clocks if clock == 1),
            2: sum(1 for clock in clocks if clock == 2),
            3: sum(1 for clock in clocks if clock == 3),
            4: sum(1 for clock in clocks if clock == 4),
            5: sum(1 for clock in clocks if clock == 5),
            6: sum(1 for clock in clocks if clock == 6),
            7: sum(1 for clock in clocks if clock == 7),
            8: sum(1 for clock in clocks if clock == 8),
        }
        self.day = 0

    @classmethod
    def from_clocks(cls, clocks):
        return cls(clocks)

    def __len__(self):
        return sum(v for v in self._population.values())

    def get_old(self, days=1):
        for _ in range(days):
            log.debug(f'{self.day=} {len(self)}')
            def evolve(clock, n):
                if clock == 0:
                    return (6, n, n)
                else:
                    return clock - 1, n, 0
            evolved_data = [evolve(clock=k, n=v) for k,v in self._population.items()]
            evolved = dict((clock,n) for clock,n,_ in evolved_data if clock != 6)
            self._population = evolved
            self._population[6] = sum(n for clock,n,_ in evolved_data if clock == 6)
            self._population[8] = sum(n for _,_,n in evolved_data)
            self.day += 1

    def __repr__(self):
        return f'Population(day={self.day}, len={len(self)})'

def parse_initial_population(lns):
    clocks = list(lns)
    assert len(clocks) == 1, "Bad input data. Expected 1 line, got {len(clocks)}"
    return Population(int(remaining) for remaining in clocks[0].split(','))
