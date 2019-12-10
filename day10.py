import day10_input
import unittest

def part1(data):
    asts = data.splitlines()
    x_l = len(asts[0])
    y_l = len(asts)
    r = []
    for x in range(x_l):
        for y in range(y_l):
            if asts[x][y] == '#':
                visibles = 0
                # primy smer sever
                for n in range(y - 1, -1, -1):
                    if asts[x][n] == '#':
                        visibles += 1
                        break
                # primy smer jih
                for n in range(y + 1, y_l):
                    if asts[x][n] == '#':
                        visibles += 1
                        break
                # primy smer zapad
                for n in range(x + 1, x_l):
                    if asts[n][y] == '#':
                        visibles += 1
                        break
                # primy smer vychod
                for n in range(x - 1, -1, -1):
                    if asts[n][y] == '#':
                        visibles += 1
                        break
                # I. kvadrant
                '''
                ctyri kvadranty
                I. x v rozmezi x+1 -> x_l step +1
                   y v rozmezi 0 az y-1
                '''
                #for n in range(x + 1, x_l):
                #    for yy in range(y-1, -1, -1):
                #        for xx in range(x+1, x_l, n - x + 1):
                #            if asts[xx][yy] == '#':
                #                visibles += 1
                #                break
                '''
                II. x v rozmezi x-1 -> 0 step -1
                    y v rozmezi 0 az y-1
                '''
                #for n in range(x-1, -1, -1):
                #    for yy in range(y-1, -1, -1):
                #        for xx in range(x-1, -1, 
                '''
                III. x v rozmezi x-1 -> 0 step -1
                     y v rozmezi y+1 -> y_l+1
                IV. x v rozmezi x+1 -> x_l+1 step +1
                    y v rozmezi y+1 -> y_l+1
                pro kazdy asteroid prohledat tyto ctyri kvadranty
                a pricist asteroidy v primem smeru
                '''
                r.append((x, y, visibles))

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
