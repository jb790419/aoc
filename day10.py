import day10_input
import unittest

from math import atan2, degrees, pi

def part1(data):
    asts = data.splitlines()
    x_l = len(asts[0])
    y_l = len(asts)
    x_range = range(x_l)
    y_range = range(y_l)
    points = [(x, y) for y in y_range for x in x_range]
    r = []
    for (x, y) in points:
        #y = coord[0]
        #x = coord[1]
        if asts[y][x] == '#':
            lines = {}
            '''
            pro kazdy asteroid vezmu vsechny body site a zjistim uhel
            potom najdu v tomto uhlu nejblizsi asteroid
            jak reprezentovat uhel?
            trigonometric functions to the rescue!
            '''
            for (xx, yy) in points:
                if asts[yy][xx] == '#':
                    if x == xx and y == yy:
                        continue
                    uhel = degrees(atan2(x-xx, y-yy))
                    try:
                        nearest = lines[uhel]
                        if (abs(x - nearest[0]) + abs(y - nearest[1])) > (abs(x-xx) + abs(y-yy)):
                            lines[uhel] = (xx, yy)
                    except KeyError:
                        lines[uhel] = (xx, yy)
            r.append((x, y, len(lines.keys())))
    return sorted(r, key=lambda n: n[2], reverse = True)[0]

def part2(data, myx, myy):
    asts = data.splitlines()
    x_l = len(asts[0])
    y_l = len(asts)
    x_range = range(x_l)
    y_range = range(y_l)
    points = [(x, y) for y in y_range for x in x_range]
    lines = {}
    for (xx, yy) in points:
        if asts[yy][xx] == '#':
            if myx == xx and myy == yy:
                continue
            arc = atan2(myx-xx, myy-yy)
            arc = arc if arc > 0 else arc + 2*pi
            arc = degrees(arc)
            try:
                lines[arc].append((xx,yy))
            except KeyError:
                lines[arc] = []
                lines[arc].append((xx, yy))
    for arc, line in lines.items():
        lines[arc] = sorted(lines[arc], key=lambda n: abs(myx-n[0])+abs(myy-n[1]))


    r = []
    while len(lines.keys()) > 0:
        for arc in sorted(lines.keys(), reverse = True):
            r.append(lines[arc].pop(0))
            if len(lines[arc]) == 0:
                del(lines[arc])
    return r






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
    def test_part2_5(self):
        poradi = part2(day10_input.test5_data, 11, 13)
        self.assertEqual(poradi[0], (11,12))
        self.assertEqual(poradi[1], (12,1))
        self.assertEqual(poradi[2], (12,2))
        self.assertEqual(poradi[9], (12,8))
        self.assertEqual(poradi[19], (16,0))
        self.assertEqual(poradi[49], (16,9))
        self.assertEqual(poradi[99], (10,16))
        self.assertEqual(poradi[198], (9,6))
        self.assertEqual(poradi[199], (8,2))
        self.assertEqual(poradi[200], (10,9))
        self.assertEqual(poradi[298], (11,1))

if __name__ == '__main__':
    lookup = part1(day10_input.input_data)
    print(lookup)
    poradi = part2(day10_input.input_data, lookup[0], lookup[1])
    print(poradi[199][0]*100 + poradi[199][1])
