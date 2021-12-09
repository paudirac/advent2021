import pytest

import logging
log = logging.getLogger(__name__)

from advent2021.displays import (
    parse_entry,
    parse_entries,
    normalize_key,
    Decoder,
    EASY_ONES,
)

def mk_lines(s):
    for line in s.split('\n'):
        yield line

sample_data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

@pytest.mark.only
def test_parse_enty():
    entry = parse_entry("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    assert entry.patterns == [7, 'cdfbe', 'gcdfa', 'fbcad', 3, 'cefabd', 'cdfgeb', 4, 'cagedb', 2]
    assert entry.outputs == ["cdfeb", "fcadb", "cdfeb", "cdbaf"]
    log.debug(f'{entry=}')

def test_notes():
    lns = mk_lines(sample_data)
    entries = parse_entries(lns)
    assert len(entries) == 10

def test_key_normalizer():
    assert normalize_key('cg') == 'cg'
    assert normalize_key('gc') == 'cg'
    assert normalize_key('fdcagb') == 'abcdfg'
    assert normalize_key('cbg') == 'bcg'

def test_decoder_leaves_unknown_keys_untoucked():
    decoder = Decoder()
    assert decoder['patata'] == 'patata'

def test_decoder_normalizes_key_access():
    decoder = Decoder()
    decoder['cg'] = 1
    assert decoder['cg'] == 1
    assert decoder['gc'] == 1
    decoder['cefg'] = 4
    assert decoder['cefg'] == 4
    assert decoder['ecfg'] == 4
    assert decoder['cfeg'] == 4
    assert decoder['gcef'] == 4

def test_easy_digits():
    lns = mk_lines(sample_data)
    entries = parse_entries(lns)
    outputs = entries.outputs
    assert len(outputs) == 10
    all_outputs = entries.all_outputs
    assert len(all_outputs) == 40
    easy_ones = [out for out in all_outputs if out in EASY_ONES]
    assert len(easy_ones) == 26

@pytest.mark.only
def test_something():
    something = [
        ("acedgfb", 8),
        ("cdfbe", 5),
        ("gcdfa", 2),
        ("fbcad", 3),
        ("dab", 7),
        ("cefabd", 9),
        ("cdfgeb", 6),
        ("eafb", 4),
        ("cagedb", 0),
        ("ab", 1),
    ]
    easy = [(normalize_key(k), v) for k,v in something if v in EASY_ONES]
    something2 = [(normalize_key(k), v) for k,v in something if v not in EASY_ONES]
    log.debug(f'{easy=}')
    log.debug(f'{something2=}')
    assert False
