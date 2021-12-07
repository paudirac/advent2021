import logging
log = logging.getLogger(__name__)

class Population:

    def __init__(self, clocks):
        self.clocks = list(clocks)
        self.day = 0

    @classmethod
    def from_clocks(cls, clocks):
        return cls(clocks)

    def __len__(self):
        return len(self.clocks)

    def get_old(self, days=1):
        for _ in range(days):
            log.debug(f'{self.day=} {len(self)}')
            new_born = []
            def evolve(clock):
                if clock == 0:
                    new_born.append(8)
                    return 6
                else:
                    return clock - 1
            evolved = [evolve(clock) for clock in self.clocks]
            self.clocks = evolved + new_born
            self.day += 1

    def __repr__(self):
        return f'Population(day={self.day}, clocks={self.clocks}, len={len(self)})'

def parse_initial_population(lns):
    clocks = list(lns)
    assert len(clocks) == 1, "Bad input data. Expected 1 line, got {len(clocks)}"
    return Population(int(remaining) for remaining in clocks[0].split(','))
