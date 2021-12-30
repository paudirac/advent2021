import attr
import typing
import logging

log = logging.getLogger(__name__)
log.debug(f'loading {__name__}')

from collections import namedtuple

def is_small(name):
    return name != 'start' and all(c.islower() for c in name)

class Cave(namedtuple('Cave', 'name')):

    @property
    def is_small(self):
        return is_small(self.name)

    def __repr__(self):
        return self.name

    @property
    def is_start(self):
        return False

    @property
    def is_end(self):
        return False

class Start(Cave):

    @property
    def is_start(self):
        return True

class End(Cave):

    @property
    def is_end(self):
        return True

def cave(name):
    if name == 'start':
        return Start(name)
    elif name == 'end':
        return End(name)
    else:
        return Cave(name)


class Conn:

    def __init__(self, spec):
        self.start, self.end = [cave(name) for name in spec.split('-')]

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

    @property
    def graph(self):
        return {cave: list(self.connections(cave)) for cave in self.caves }

    def get(self, name):
        found = [cave for cave in self.caves if cave.name == name]
        assert len(found) == 1, f"More than one cave called {name}. Expected only one."
        return found[0]


@attr.s(auto_attribs=True, repr=False)
class Node:
    value: Cave
    graph: dict
    parent: Cave = None
    childs: typing.List['Node'] = attr.Factory(list)
    paths: typing.List[str] = attr.Factory(list)

    def __attrs_post_init__(self):
        if self.parent is not None:
            self.parent._add_child(self)

    @property
    def is_root(self):
        return self.parent is None

    @property
    def path_to_parent(self):
        current = self
        path = []
        while not current.is_root:
            path.append(current.value)
            current = current.parent
        return path + [current.value]

    def walk(self, accumulator, continue_walk):
        for child in self.graph[self.value]:
            assert child != self.value, "Child {child} is self! {self.value}"

            if child.is_start:
                continue # next child

            if child.is_end:
                child_node = Node(child, self.graph, parent=self)
                accumulator.accumulate(child_node.chain)
                continue # next child

            if continue_walk(child, self):
                child_node = Node(child, self.graph, parent=self)
                child_node.walk(accumulator=accumulator, continue_walk=continue_walk)

    def _add_child(self, child):
        self.childs.append(child)

    @property
    def chain(self):
        return '-'.join([str(step) for step in reversed(self.path_to_parent)])

    def __repr__(self):
        chain = '-'.join([str(step) for step in reversed(self.path_to_parent)])
        return f'Node({self.value}, chain={chain} paths={self.paths}))'

class AccumulatorCounter:

    def __init__(self):
        self.count = 0

    def accumulate(self, item):
        self.count += 1

class PathAccumulator(AccumulatorCounter):

    def __init__(self):
        super().__init__()
        self.paths = []

    def accumulate(self, item):
        super().accumulate(item)
        self.paths.append(item)

from collections import Counter

def continue_walk_strategy_1(node: Cave, path_so_far: Node):
    if not node.is_small:
        return True

    counts = Counter(path_so_far.path_to_parent)
    appearances = counts[node]
    is_allowed = appearances + 1 <= 1

    return is_allowed

def continue_walk_strategy_2(node: Cave, path_so_far: Node) -> bool:
    assert not node.is_start, "Is start!"
    assert not node.is_end, "Is end!"
    allowed_values = { 1, 2 }
    if not node.is_small:
        return True

    path_so_far_next = [node] + path_so_far.path_to_parent
    counts = Counter(step for step in path_so_far_next
                     if step.is_small and
                     not step.is_start and
                     not step.is_end)

    more_than_twice = [(cave, visits) for cave,visits in counts.items() if visits > 2]
    if len(more_than_twice) > 0:
        return False
    twice = [(cave, visits) for cave, visits in counts.items() if visits == 2]
    if len(twice) > 1:
        return False

    if all(visits == 1 for cave, visits in counts.items() if visits < 2):
        return True

    raise Exception(f'Not should be here {node} {path_so_far.chain} {counts=}')


def build_paths(graph, start, continue_walk=continue_walk_strategy_1):
    root = Node(start, graph, parent=None)
    accumulator = PathAccumulator()
    root.walk(accumulator=accumulator, continue_walk=continue_walk)
    return set(accumulator.paths)

def count_paths(graph, start, continue_walk=continue_walk_strategy_1):
    root = Node(start, graph, parent=None)
    accumulator = AccumulatorCounter()
    root.walk(accumulator=accumulator, continue_walk=continue_walk)
    return accumulator.count



def parse_rough_map(lns):
    rows = list(ln.strip() for ln in lns if len(ln) >0)
    return Map(Conn(spec) for spec in rows)
