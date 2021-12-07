import logging

log = logging.getLogger(__name__)

from dataclasses import dataclass

def _clean_specs(lns):
    import re
    _IS_BLANK = re.compile(r'\s+$')

    def is_blank(line):
        return _IS_BLANK.match(line) or len(line) == 0

    return list(ln for ln in lns if not is_blank(ln))

@dataclass(frozen=True)
class LineDef:
    x0: int
    y0: int
    x1: int
    y1: int

    @property
    def is_horizontal(self):
        return self.y0 == self.y1

    @property
    def is_vertical(self):
        return self.x0 == self.x1

def _parse_line_def(spec):
    log.debug(f'{spec=}')
    left, right = spec.split('->')
    x0,y0 = left.strip().split(',')
    x1, y1 = right.strip().split(',')
    return LineDef(int(x0), int(y0), int(x1), int(y1))

def parse_line_defs(lns):
    specs = _clean_specs(lns)
    return [_parse_line_def(spec) for spec in specs]
