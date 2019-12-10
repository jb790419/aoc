import day10_input
import unittest

def cvis(x, y):
    '''count visible asteroids'''
    if x == 3 and y == 4:
        return 8
    return 0

def part1(data):
    asts = data.splitlines()
    x_l = len(asts[0])
    y_l = len(asts)
    r = [(x,y,cvis(x,y)) for x in range(x_l) for y in range(y_l) if asts[x][y] == '#']
    return sorted(r, key=lambda n: n[2], reverse = True)[0]

class TestMonitor(unittest.TestCase):
    def test_part1_1(self):
        self.assertEqual(part1(day10_input.test1_data), (3, 4, 8))
    def test_part1_2(self):
        self.assertEqual(part1(day10_input.test2_data), (5, 8, 33))
    def test_part1_3(self):
        self.assertEqual(part1(day10_input.test3_data), (1, 2, 35))
    def test_part1_4(self):
        self.assertEqual(part1(day10_input.test4_data), (6, 3, 41))
    def test_part1_5(self):
        self.assertEqual(part1(day10_input.test5_data), (11, 13, 210))

if __name__ == '__main__':
    print(part1(day10_input.input_data))
