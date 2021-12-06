import logging
log = logging.getLogger(__name__)

class Game:

    def __init__(self, draws):
        self.draws = draws

def _draws(line):
    return [int(num) for num in line.split(',')]

def new_game(lines):
    lines = list(lines)
    assert len(lines) > 0, "Not enough data!"
    draws = _draws(lines[0])
    return Game(draws=draws)
