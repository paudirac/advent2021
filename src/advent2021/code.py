def zip_one(lst):
    return zip(lst, lst[1:])

def count_larger(lst):
    diffs = [b-a for a,b in zip_one(lst)]
    return sum(1 for a in diffs if a >0)

class Chunks:

    def __init__(self, lst, window):
        self.lst = list(lst)
        self.len = len(self.lst)
        self.window = window

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= self.len - self.window + 1:
            raise StopIteration

        ret = self.lst[self.i:self.i + self.window]
        self.i += 1
        return ret

def sliding_sum(sample, window=1):
    # for chunk in Chunks(sample, window):
    #     print(f'{chunk=} {sum(chunk)}')
    return [sum(chunk) for chunk in Chunks(sample, window=window)]

def int_lines(f):
    for line in f.readlines():
        yield int(line)

def as_list(g):
    return list(g)

DAYS = {
    '1.1': count_larger,
    '1.2': lambda l: count_larger(sliding_sum(l, window=3)),
}

PARSER = {
    '1.1': lambda f: as_list(int_lines(f)),
    '1.2': lambda f: as_list(int_lines(f)),
}

if __name__ == '__main__':
    import sys

    _, day = sys.argv
    print(f'{day=}')
    f = sys.stdin
    parsed = list(PARSER[day](f))
    answer = DAYS[day](parsed)
    print(f'Day {day} answer: {answer}')
