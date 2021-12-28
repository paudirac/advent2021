import attr
import typing
import logging

log = logging.getLogger(__name__)
log.debug(f'loading {__name__}')

from collections import namedtuple

class Cave(namedtuple('Cave', 'name')):

    @property
    def is_small(self):
        return self.name != 'start' and all(c.islower() for c in self.name)

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

    @property
    def graph(self):
        return {cave: list(self.connections(cave)) for cave in self.caves }

    def get(self, name):
        found = [cave for cave in self.caves if cave.name == name]
        assert len(found) == 1, f"More than one cave called {name}. Expected only one."
        return found[0]

# class PathVisitor:

#     def __init__(self, caves, start):
#         self.caves = caves
#         self.visited = [start]

#     def visit_all(self):
#         current = self.caves[-1]
#         nexts = self.caves.connections(current)
#         for cave in nexts:

# class Node:

#     def __init__(self, cave, parent):
#         self.cave = cave
#         self.parent = parent
#         self.childs = []

#     def add_child(self, child: Cave):
#         if child.is_small and child in parent:
#             self.childs.append(Stop)
invalid = Cave('X')

def debug(f):
    count = -1
    labels = []
    def wrapper(current, childs, graph, visited):
        nonlocal count
        count = count + 1
        label = f'[{count}]'
        labels.append(label)
        log.debug(f'{label} {current=} {childs=} {visited=}')
        ret = f(current, childs, graph, visited)
        label = labels.pop()
        log.debug(f'{label} {ret=}')
        return ret
    return wrapper

@debug
def _build_tree(current: Cave, childs, graph, visited=set()):
    # if current in visited:
    #     return []
    if current == Cave('end'):
        return [current]
    if current == Cave('start'):
        if current not in visited:
            visited.add(current)
            return [current] + [_build_tree(child, graph[child], graph, visited=visited) for child in childs]
        else:
            return [invalid]
    if current.is_small and current in visited:
        return [current] + [invalid]
    if current.is_small:
        visited.add(current)
    return [current] + [_build_tree(child, graph[child], graph, visited=visited) for child in childs]

# def _build_childs(childs, graph, visited):
#     return [jjk]

def build_tree(graph):
    start = Cave('start')
    childs = graph[start]
    visited = set()
    #return [start + _build_childs(childs, graph, visited)]
    return _build_tree(start, childs, graph, visited=visited)

# class Node:

#     def __init__(self, value, parent):
#         self.value = value
#         self.parent = parent
#         self.children = []

#     def add_child(self, value):
#         node = Node(value, self)
#         self.children.append(node)

#     def __repr__(self):
#         return f'({self.value}, {[str(child) for child in self.children]})'

from collections import deque

class GraphIterator:

    def __init__(self, graph, start, stop_p):
        self.graph = graph
        self.start = start
        self.stop_p = stop_p

    def __iter__(self):
        self.pending = deque([self.start])
        return self

    def __next__(self):
        log.debug(f'{self}')
        stop_p = self.stop_p
        if len(self.pending) > 0:
            current = self.pending.pop()
            children = self.graph[current]
            self.pending.extend(children)
            if stop_p(current):
                self.pending.clear()
            return current
        else:
            raise StopIteration

    def __repr__(self):
        return f'GraphIterator({self.pending})'
# def _build_tree2(current: Node, childs, graph, visited=set()):
#     for child in childs:
#         current.add_child(child)
#     for child in current.children:
#         _build_tree2(child, graph[])

# def build_tree2(graph, start):
#     childs = graph[start]
#     visited = set()
#     root = Node(start, None)
#     _build_tree2(root, childs, graph, visited=visited)
#     return root



# def build_tree(cave, graph):
#     if cave == Cave('end'):
#         return []
#     if cave == Cave('start'):
#         return []
#     else if cave
#     current = start[-1]
#     for cave in caves.connections(current):
#         if cave.is_small and cave in start:
#             return start + [Cave('EOF')]
#         if cave == Cave('end'):
#             return start + [cave]
#         if cave != Cave('start'):
#             return start + build_tree(caves, start=[cave])

class Stack:

    def __init__(self):
        self.imp = deque()

    def push(self, item):
        self.imp.append(item)

    def pop(self):
        return self.imp.pop()

    @property
    def top(self):
        return self.imp[-1]

    def __len__(self):
        return len(self.imp)

count = 0

graph = {}



@attr.s(auto_attribs=True, repr=False)
class Node:
    value: Cave
    graph: dict
    parent: Cave = None
    childs: typing.List['Node'] = attr.Factory(list)
    paths: typing.List[str] = attr.Factory(list)

    def __attrs_post_init__(self):
        #log.debug(f'creating {self}')
        global count
        count += 1
        #log.debug(f'{count=}')
        if self.parent is not None:
            #log.debug(f'set {self} as child of {self.parent}')
            self.parent._add_child(self)

    # def __init__(self, value, graph, parent=None):
    #     self.value = value
    #     self.graph = graph
    #     self.parent = parent
    #     if parent is not None:
    #         self.parent._add_child(self)
    #     self.childs = []

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

    def walk(self, accumulator):
        #log.debug(f'visit {self}')
        #log.debug(f'walk {self.value.name}')
        for child in self.graph[self.value]:
            if child.is_end:
                child_node = Node(child, self.graph, parent=self)
                log.debug(f'child is end {child_node}')
                log.debug(f'{child_node.chain=}')
                accumulator.append(child_node.chain)
            else:
                is_root = child == Cave('start')
                is_small_and_repeated = child.is_small and child in self.path_to_parent
                if not child.is_start and not is_small_and_repeated:
                    child_node = Node(child, self.graph, parent=self)
                    child_node.walk(accumulator=accumulator)
        #log.debug(f'walked {self}')

    def _add_child(self, child):
        self.childs.append(child)

    @property
    def chain(self):
        return '-'.join([str(step) for step in reversed(self.path_to_parent)])

    def __repr__(self):
        chain = '-'.join([str(step) for step in reversed(self.path_to_parent)])
        return f'Node({self.value}, chain={chain} paths={self.paths}))'

    # def __eq__(self, other):
    #     if isinstance(other, Node):
    #         if self.value == other.value:
    #             return len(self.childs) == len(other.childs) and all(s == o for s,o in zip(self.childs, other.childs))
    #     return False


def build_tree(graph, start):
    root = Node(start, graph, parent=None)
    accumulator = []
    root.walk(accumulator=accumulator)
    log.debug(f'walked graph: {accumulator=}')
    return root



def parse_rough_map(lns):
    rows = list(ln for ln in lns if len(ln) >0)
    return Map(Conn(spec) for spec in rows)
