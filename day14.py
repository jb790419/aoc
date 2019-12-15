import unittest
import input_day14

def parse(input_string):
    parsed = []
    for (inputs, output) in [[line.split(' => ')[0].split(', '), line.split(' => ')[1]] for line in input_string.splitlines()]:
        react = {}
        qty, subst = output.split(' ')
        react[(int(qty), subst)] = [(int(item.split(' ')[0]), item.split(' ')[1]) for item in inputs]
        parsed.append(react)
    return parsed

def ore_for(qty, subst, parsed):
    stack = []
    stack.append((qty, subst))
    final_subst = {}
    while stack:
        (qty, subst) = stack.pop(0)
        print(qty, subst)
        for r in parsed:
            for ((outqty, outsubst), inputs) in r.items():
                if outsubst == subst:
                    '''porovnat qty 7A vs outqty 10A'''
                    podil, zbytek = divmod(qty, outqty)
                    if zbytek > 0: podil += 1
                    for inqty, insubst in inputs:
                        '''pokud subst je ore, ...'''
                        if insubst == 'ORE':
                            '''spocitat kolik ore a pricist k celku'''
                            try:
                                final_subst[subst] += qty 
                            except KeyError:
                                final_subst[subst] = qty
                        else:
                            stack.append((inqty*podil, insubst))
                    continue
    print(final_subst)
    orecount = 0
    for subst, qty in final_subst.items():
        for r in parsed:
            for ((outqty, outsubst), inputs) in r.items():
                if outsubst == subst:
                    podil, zbytek = divmod(qty, outqty)
                    if zbytek > 0: podil += 1
                    inqty, insubst = inputs[0]
                    orecount += podil * inqty
                    #print(f'na vyrobu {qty} {subst} potrebujeme {podil*inqty} {insubst}')
                    continue
    return orecount




def part1(input_string):
    parsed = parse(input_string)
    return ore_for(1, 'FUEL', parsed)

class TestReactions(unittest.TestCase):

    def test_parse(self):
        '''
        jak by mela vypadat jedna veta?
        [{(1, FUEL):[(7, A), (1, B)]},...]
        '''
        parsed = [{(2, 'A'): [(9, 'ORE')]},
                {(3, 'B'): [(8, 'ORE')]},
                {(5, 'C'): [(7, 'ORE')]},
                {(1, 'AB'): [(3, 'A'), (4, 'B')]},
                {(1, 'BC'): [(5, 'B'),(7, 'C')]},
                {(1, 'CA'): [(4, 'C'), (1, 'A')]},
                {(1, 'FUEL'): [(2, 'AB'), (3, 'BC'), (4, 'CA')]}]

        self.assertEqual(parse(input_day14.test2), parsed)
        
    def test_part1_1(self):
        self.assertEqual(part1(input_day14.test1), 31)

    def test_part1_2(self):
        self.assertEqual(part1(input_day14.test2), 165)

    def test_part1_3(self):
        self.assertEqual(part1(input_day14.test3), 13312)

    def test_part1_4(self):
        self.assertEqual(part1(input_day14.test4), 180697)

    def test_part1_5(self):
        self.assertEqual(part1(input_day14.test5), 2210736)
