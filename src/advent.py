#!/usr/bin/env python

from advent2021.code import (
    DAYS,
    PARSER,
)

if __name__ == '__main__':
    import sys

    _, day = sys.argv
    print(f'{day=}')
    f = sys.stdin
    parsed = list(PARSER[day](f))
    answer = DAYS[day](parsed)
    print(f'Day {day} answer: {answer}')
