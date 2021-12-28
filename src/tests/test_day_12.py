import pytest

import logging
log = logging.getLogger(__name__)

from advent2021.caves import (
    parse_rough_map,
    Cave,
    Conn,
    build_tree,
    Node,
    Start,
    End,
)

def mk_lines(s):
    for line in s.split('\n'):
        yield line

sample_data = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

def test_caves():
    lns = mk_lines(sample_data)
    caves = parse_rough_map(lns)
    assert len(caves.conns) == 7
    assert len(caves.caves) == 6
    assert Cave('start') in caves
    assert Cave('A') in caves
    assert Cave('b') in caves
    assert Cave('c') in caves
    assert Cave('d') in caves
    assert Cave('end') in caves

def test_conns():
    conn = Conn('a-b')
    assert conn.ends == { Cave('a'), Cave('b') }

def test_connections():
    lns = mk_lines(sample_data)
    caves = parse_rough_map(lns)
    assert caves.connections(Cave('start')) == { Cave('A'), Cave('b') }
    assert caves.connections(Cave('A')) == { Cave('start'), Cave('b'), Cave('c'), Cave('end') }
    assert caves.connections(Cave('b')) == { Cave('start'), Cave('A'), Cave('d'), Cave('end') }
    assert caves.connections(Cave('c')) == { Cave('A') }
    assert caves.connections(Cave('d')) == { Cave('b') }

def xtest_start_end():
    lns = mk_lines(sample_data)
    caves = parse_rough_map(lns)
    assert caves.get('start') == Cave('start')
    assert caves.get('end') == Cave('end')
    tree = build_tree(caves, start=Cave('end'))
    log.debug(f'{tree=}')
    assert False
    # build cave tree
    # discard paths that do not end to the end
    # create paths

def xtest_conns_dict():
    lns = mk_lines(sample_data)
    caves = parse_rough_map(lns)
    graph = caves.graph
    import pprint
    tree = build_tree(graph)
    import pprint
    log.debug(f'{tree=}')
    #log.debug(f'{pprint.pformat(tree)}')
    assert len(tree) == 2
    assert False

def test_simple_graph():
    S = Start('start')
    a = Cave('a')
    b = Cave('b')
    E = End('end')
    graph = {
        S: [a, b],
        a: [E],
        b: [E],
        E: [a, b],
    }
    tree = build_tree(graph, start=S)
    log.debug(f'{tree=}')

    root = Node(S, graph, parent=None)
    node_root_a = Node(a, graph, parent=root)
    node_root_b = Node(b, graph, parent=root)
    node_root_a_end = Node(E, graph, parent=node_root_a)
    node_root_b_end = Node(E, graph, parent=node_root_b)
    expected = root
    assert tree == expected

@pytest.mark.only
def test_not_so_simple_graph():
    S = Start('start')
    a = Cave('a')
    b = Cave('b')
    E = End('end')
    graph = {
        S: [a, b],
        a: [E,b],
        b: [E, a],
        E: [a, b],
    }
    tree = build_tree(graph, start=S)

    # root = Node(S, graph, parent=None)
    # root_a = Node(a, graph, parent=root)
    # root_b = Node(b, graph, parent=root)
    # root_a_end = Node(E, graph, parent=root_a)
    # root_b_end = Node(E, graph, parent=root_b)
    # root_a_b = Node(b, graph, parent=root_a)
    # root_a_b_end = Node(E, graph, parent=root_a_b)
    # root_b_a = Node(a, graph, parent=root_b)
    # root_b_a_end = Node(E, graph, parent=root_b_a)
    #log.debug(f'expected: {expected}')
    log.debug(f'{tree=}')
    #expected = root
    #assert tree == expected
    assert False


def xtest_not_so_simple_graph():
    S = Cave('start')
    A = Cave('A')
    b = Cave('b')
    E = Cave('end')
    graph = {
        S: [A, b],
        A: [E, b],
        b: [E, A],
        E: [A, b],
    }
    X = Cave('∅')
    tree = build_tree(graph, start=S)
    log.debug(f'{tree=}')
    expected = [
        S,
        [A, [E], [b, [E], [A, [E], [b, X]]]], [b, X]]
    assert tree == expected

def xtest_graph():
    S = Cave('start')
    A = Cave('A')
    b = Cave('b')
    c = Cave('c')
    E = Cave('end')
    graph = {
        S: [A, b],
        A: [S, b],
        b: [A, c],
        c: [b, E],
        E: [b, c],
    }

    root = build_tree(graph, start=S)
    log.debug(f'{root=}')
    assert False
