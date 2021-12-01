def zip_one(lst):
    return zip(lst, lst[1:])

def count_larger(lst):
    lst = list(lst)
    diffs = [b-a for a,b in zip_one(lst)]
    return sum(1 for a in diffs if a >0)

def parser(f):
    for line in f.readlines():
        yield int(line)

DAYS = {
    '1': count_larger,
}

PARSER = {
    '1': parser,
}

if __name__ == '__main__':
    import sys

    _, day = sys.argv
    print(f'{day=}')
    f = sys.stdin
    parsed = PARSER[day](f)
    answer = DAYS[day](parsed)
    print(f'Day {day} answer: {answer}')
