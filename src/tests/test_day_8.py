import logging
log = logging.getLogger(__name__)

from advent2021.displays import (
    parse_entry,
    parse_entries,
    is_1,
    is_4,
    is_7,
    is_8,
    is_easy,
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

def test_parse_enty():
    entry = parse_entry("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    assert entry.patterns == "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab"
    assert entry.outputs == ["cdfeb", "fcadb", "cdfeb", "cdbaf"]

def test_notes():
    lns = mk_lines(sample_data)
    entries = parse_entries(lns)
    assert len(entries) == 10

def test_are_easy():
    # Assuming entries do not contain repeated values in any singnal or output values
    assert is_1("ab")
    assert is_4("abcd")
    assert is_7("abc")
    assert is_8("abcdefg")

def test_easy_digits():
    lns = mk_lines(sample_data)
    entries = parse_entries(lns)
    outputs = entries.outputs
    assert len(outputs) == 10
    all_outputs = entries.all_outputs
    assert len(all_outputs) == 40
    easy_ones = [out for out in all_outputs if is_easy(out)]
    assert len(easy_ones) == 26
