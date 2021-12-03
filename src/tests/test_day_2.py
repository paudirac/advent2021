from advent2021.submarine import (
    tokenize,
    new_submarine,
    Position,
    AimPosition,
    forward,
    down,
    up,
)

def mk_sample(s):
    for line in s.split('\n'):
        yield line

def test_parse():
    """This is overkill, I know. But fun, right?"""
    sample = mk_sample("""
forward 5
down 5
forward 8
up 3
down 8
forward 2
    """)
    print(f'{sample=}')
    tokens = list(tokenize(sample))
    print(f'{tokens=}')
    assert list(tokens) == [forward(5), down(5), forward(8), up(3), down(8), forward(2)]


def test_position():
    sample = mk_sample("""
forward 5
down 5
forward 8
up 3
down 8
forward 2
    """)
    submarine = new_submarine(Position(x=0, y=0))
    assert submarine.position == Position(x=0, y=0)
    commands = tokenize(sample)
    for cmd in commands:
        submarine.process(cmd)
    assert submarine.position == (15, 10)

def test_product_x_y():
    sample = mk_sample("""
forward 5
down 5
forward 8
up 3
down 8
forward 2
    """)
    submarine = new_submarine(Position(x=0, y=0))
    commands = tokenize(sample)
    for cmd in commands:
        submarine.process(cmd)
    assert submarine.position.x * submarine.position.y == 150

def test_with_aim():
    sample = mk_sample("""
forward 5
down 5
forward 8
up 3
down 8
forward 2
    """)
    submarine = new_submarine(AimPosition(x=0, y=0, aim=0))
    commands = tokenize(sample)
    for cmd in commands:
        submarine.process(cmd)
    assert submarine.position.x * submarine.position.y == 900
