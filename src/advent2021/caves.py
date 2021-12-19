import logging

log = logging.getLogger(__name__)
log.debug(f'loading {__name__}')

from collections import namedtuple

class Cave(namedtuple('Cave', 'name')):

    @property
    def is_small(self):
        return all(c.islower() for c in self.name)

class Conn:

    def __init__(self, spec):
        self.start, self.end = [Cave(name) for name in spec.split('-')]

    @property
    def ends(self):
        return { self.start, self.end }

    def __contains__(self, cave):
        return self.start == cave or self.end == cave

class Map:

    def __init__(self, conns):
        self.conns = list(conns)
        self.caves = set(cave for caves in self.conns for cave in caves.ends)

    def __contains__(self, item):
        assert isinstance(item, Cave), f"{item} not here. Only Caves"
        return item in self.caves

    def connections(self, cave):
        c = set()
        for conn in self.conns:
            if cave in conn:
                ends = conn.ends
                for e in ends:
                    if e != cave:
                        c.add(e)
        return c

def parse_rough_map(lns):
    rows = list(ln for ln in lns if len(ln) >0)
    return Map(Conn(spec) for spec in rows)
