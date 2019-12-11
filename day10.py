import day10_input
import unittest

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
            print(x,y, asts[y][x])
            '''
            pro kazdy asteroid vezmu vsechny body site a zjistim uhel
            potom najdu v tomto uhlu nejblizsi asteroid
            jak reprezentovat uhel?
            rozdil mezi x a rozdil mezi y
            podil
            '''
            for (xx, yy) in points:
                if asts[yy][xx] == '#':
                #if x != xx and y !=yy:
                #uhel.append((x-xx, y-yy))
                    if y!=yy and x!=xx:
                        uhel = f'{x-xx}:{y-yy}'
                        try:
                            nearest = lines[uhel]
                            if (abs(x - nearest[0]) + abs(y - nearest[1])) > (abs(x -xx) + abs(y-yy)):
                                lines[uhel] = (xx, yy)
                        except KeyError:
                            lines[uhel] = (xx, yy)
                    #  + vyresit situaci na ose y=yy x=xx a je to!
            print(lines)

def part1x(data):
    asts = data.splitlines()
    x_l = len(asts[0])
    y_l = len(asts)
    r = []
    for y in range(y_l):
        for x in range(x_l):
            print(x,y, asts[y][x])
            if asts[y][x] == '#':
                visibles = 0
                # primy smer sever
                for yy in range(y - 1, -1, -1):
                    if asts[yy][x] == '#':
                        visibles += 1
                        break
                # primy smer jih
                for yy in range(y + 1, y_l):
                    if asts[yy][x] == '#':
                        visibles += 1
                        break
                # primy smer zapad
                for n in range(x + 1, x_l):
                    if asts[y][n] == '#':
                        visibles += 1
                        break
                # primy smer vychod
                for n in range(x - 1, -1, -1):
                    if asts[y][n] == '#':
                        visibles += 1
                        break
                # I. kvadrant
                '''
                ctyri kvadranty
                ... resp osm oktantu, jak vychazi najevo
                I. x v rozmezi x+1 -> x_l step +1
                   y v rozmezi 0 az y-1
                '''
                if y > 0:
                    for n in range(x + 1, x_l):
                        # jak daleko je n od x - to je step dalsi iterace
                        #print(n, x, x_l)
                        #print(list(range(n, x_l, n-x)))

                        line = [(xx, yy) for xx in range(n, x_l, n-x) for yy in range(y-1, -1, -1)]
                        print(x, y, n,line)


                    
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
