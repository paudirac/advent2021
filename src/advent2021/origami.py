class Paper:
    pass

class Instructions:
    pass



from collections import namedtuple

class Coordinate(namedtuple('CoordinateBase', 'x y')):

    @classmethod
    def from_string(cls, string):
        x, y = string.split(',')
        return cls(int(x), int(y))

    @classmethod
    def is_coordinate(cls, ln):
        try:
            a,b = ln.split(',')
        except:
            return False
        return True

class FoldInstruction(namedtuple('FoldInstructionBase', 'coord value')):

    @classmethod
    def from_string(cls, string):
        _, code = string.split('fold along')
        coord, value = code.strip().split('=')
        return cls(coord, int(value))

    @classmethod
    def is_instruction(cls, ln):
        try:
            _, code = ln.split('fold along')
        except:
            return False
        return True

def parse_paper_instructions(lns):
    lns = list(lns)
    coords = list(Coordinate.from_string(ln) for ln in lns if Coordinate.is_coordinate(ln))
    instructions = list(FoldInstruction.from_string(ln) for ln in lns if FoldInstruction.is_instruction(ln))
    return coords, instructions
