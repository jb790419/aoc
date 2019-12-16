import unittest
from collections import defaultdict
from math import ceil
import input_day14

def parse(data):
    def parse_chem(s):
        units, name = s.split(' ')
        return int(units), name

    reactions = {}
    for reaction in data.split('\n'):
        input, output = reaction.split(' => ')
        inputs = []
        for chem in input.split(', '):
            inputs.append(parse_chem(chem))
        out_units, out_chem = parse_chem(output)
        reactions[out_chem] = (out_units, inputs)
    return reactions

def minimum_ore(reactions, chem='FUEL', units=1, waste=None):
    if waste is None:
        waste = defaultdict(int)

    if chem == 'ORE':
        return units

    # Re-use waste chemicals.
    reuse = min(units, waste[chem])
    units -= reuse
    waste[chem] -= reuse

    # Work out how many reactions we need to perform.
    produced, inputs = reactions[chem]
    n = ceil(units / produced)

    # Determine the minimum ore required to produce each input.
    ore = 0
    for required, input in inputs:
        ore += minimum_ore(reactions, input, n * required, waste)

    # Store waste so it can be re-used
    waste[chem] += n * produced - units

    return ore

def maximum_fuel(reactions):
    target = 1000000000000
    lower = None
    upper = 1

    # Find upper bound.
    while minimum_ore(reactions, units=upper) < target:
        lower = upper
        upper *= 2

    # Binary search to find maximum fuel produced.
    while lower + 1 < upper:
        mid = (lower + upper) // 2
        ore = minimum_ore(reactions, units=mid)
        if ore > target:
            upper = mid
        elif ore < target:
            lower = mid

    return lower


class TestReactions(unittest.TestCase):

    def test_part1_1(self):
        self.assertEqual(minimum_ore(parse(input_day14.test1)), 31)

    def test_part1_2(self):
        self.assertEqual(minimum_ore(parse(input_day14.test2)), 165)

    def test_part1_3(self):
        self.assertEqual(minimum_ore(parse(input_day14.test3)), 13312)

    def test_part1_4(self):
        self.assertEqual(minimum_ore(parse(input_day14.test4)), 180697)

    def test_part1_5(self):
        self.assertEqual(minimum_ore(parse(input_day14.test5)), 2210736)

if __name__ == '__main__':
    print(minimum_ore(parse(input_day14.input_data)))
    print(maximum_fuel(parse(input_day14.input_data)))
