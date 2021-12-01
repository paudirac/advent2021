from advent2021.code import count_larger

def test_count_larger():
    sample = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263,
    ]
    assert count_larger(sample) == 7
