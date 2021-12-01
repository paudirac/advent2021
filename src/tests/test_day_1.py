from advent2021.code import (
    count_larger,
    sliding_sum,
)

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

def test_sum_three_window():
    sample = [
        199, #  A
        200, #  A B
        208, #  A B C
        210, #    B C D
        200, #  E   C D
        207, #  E F   D
        240, #  E F G
        269, #    F G H
        260, #      G H
        263, #        H
    ]
    sample_sliding_sum = [
        607,
        618,
        618,
        617,
        647,
        716,
        769,
        792,
    ]
    assert sliding_sum(sample, window=3) == sample_sliding_sum

def test_count_larger_sliding():
    sample = [
        199, #  A
        200, #  A B
        208, #  A B C
        210, #    B C D
        200, #  E   C D
        207, #  E F   D
        240, #  E F G
        269, #    F G H
        260, #      G H
        263, #        H
    ]
    assert count_larger(sliding_sum(sample, window=3)) == 5
