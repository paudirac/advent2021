import pytest

import logging
log = logging.getLogger(__name__)

from advent2021.caves import (
    parse_rough_map,
    Cave,
    Conn,
    build_paths,
    count_paths,
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
    paths = build_paths(graph, start=S)
    expected_paths = set([
        'start-a-end',
        'start-b-end',
    ])

    assert paths == expected_paths

def test_not_so_simple_graph():
    S = Start('start')
    a = Cave('a')
    b = Cave('b')
    E = End('end')
    graph = {
        S: [a, b],
        a: [S, E,b],
        b: [S, E, a],
        E: [a, b],
    }
    paths = build_paths(graph, start=S)
    expected_paths = set([
        'start-a-end',
        'start-a-b-end',
        'start-b-end',
        'start-b-a-end',
    ])
    assert paths == expected_paths

def test_not_so_simple_graph_with_repetitions():
    S = Start('start')
    A = Cave('A')
    b = Cave('b')
    E = End('end')
    graph = {
        S: [A, b],
        A: [S, E, b],
        b: [S, E, A],
        E: [A, b],
    }
    paths = build_paths(graph, start=S)
    log.debug(f'{paths=}')
    expected_paths = set([
        'start-A-b-A-end',
        'start-A-b-end',
        'start-A-end',
        'start-b-A-end',
        'start-b-end',
    ])
    log.debug(f'{paths=}')
    assert paths == expected_paths

def test_paths_on_sample():
    lns = mk_lines(sample_data)
    caves = parse_rough_map(lns)
    graph = caves.graph
    paths = build_paths(graph, Start('start'))
    normalized_paths = set([path.replace('-', ',') for path in paths])
    expected_paths = set([
        'start,A,b,A,c,A,end',
        'start,A,b,A,end',
        'start,A,b,end',
        'start,A,c,A,b,A,end',
        'start,A,c,A,b,end',
        'start,A,c,A,end',
        'start,A,end',
        'start,b,A,c,A,end',
        'start,b,A,end',
        'start,b,end',
    ])
    assert normalized_paths == expected_paths

sample_data_2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

def test_paths_on_sample_2():
    lns = mk_lines(sample_data_2)
    caves = parse_rough_map(lns)
    graph = caves.graph
    paths = build_paths(graph, Start('start'))
    normalized_paths = set([path.replace('-', ',') for path in paths])
    expected_paths = set([
        'start,HN,dc,HN,end',
        'start,HN,dc,HN,kj,HN,end',
        'start,HN,dc,end',
        'start,HN,dc,kj,HN,end',
        'start,HN,end',
        'start,HN,kj,HN,dc,HN,end',
        'start,HN,kj,HN,dc,end',
        'start,HN,kj,HN,end',
        'start,HN,kj,dc,HN,end',
        'start,HN,kj,dc,end',
        'start,dc,HN,end',
        'start,dc,HN,kj,HN,end',
        'start,dc,end',
        'start,dc,kj,HN,end',
        'start,kj,HN,dc,HN,end',
        'start,kj,HN,dc,end',
        'start,kj,HN,end',
        'start,kj,dc,HN,end',
        'start,kj,dc,end',
    ])
    assert normalized_paths == expected_paths

sample_data_3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

def test_paths_on_larger_sample():
    lns = mk_lines(sample_data_3)
    caves = parse_rough_map(lns)
    graph = caves.graph
    paths = build_paths(graph, Start('start'))
    assert len(paths) == 226
    assert count_paths(graph, Start('start')) == 226
    #assert count_paths(graph, Start('start'), allowed_times_max=2) == 3509
