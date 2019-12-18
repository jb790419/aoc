from intcode import Intcode
import input_day15
from collections import defaultdict
import random

def unknown():
    return 3

class Droid:
    def __init__(self, intc):
        self.comp = Intcode(intc)
        self.comp.max_outputs = 1
        self.comp.robot = self
        # {(x, y): sc, ...}
        self.map = defaultdict(unknown)
        self.map[(0,0)] = 1
        self.x = 0
        self.y = 0
        self.sc = 0
        self.input = 1
        self.path = [1]
        self.new_x = 0
        self.new_y = 0
        self.stepcount = 0
        self.at_start = 0
        self.strings = {
                0: '#',
                1: '.',
                2: 'O',
                3: ' ',
                4: 'v'
                }

        self.comp.process()

    def showmap(self):
        lines = []
        try:
            xs = [x for (x,y), val in self.map.items()]
            ys = [y for (x,y), val in self.map.items()]
            for y in range(min(ys), max(ys) + 1):
                line = str()
                for x in range(min(xs), max(xs)+1):
                    if x == 0 and y == 0:
                        line += 'S'
                    elif x == self.x and y == self.y:
                        line += 'X'
                    else:
                        line += self.strings.get(self.map[(x, y)])
                lines.append(line)
            return '\n'.join(lines)
        except ValueError:
            pass

    @property
    def last(self):
        if self.sc == 0:
            #naposledy jsme sli posledni element path
            return self.path[-1]
        else:
            #naposledy jsem sli self.input
            return self.input

    @property
    def left(self):
        if self.last == 1: return 3
        if self.last == 2: return 4
        if self.last == 3: return 2
        if self.last == 4: return 1

    @property
    def right(self):
        if self.last == 1: return 4 
        if self.last == 2: return 3
        if self.last == 3: return 1
        if self.last == 4: return 2

    @property
    def head(self):
        return self.last

    @property
    def back(self):
        if self.last == 1: return 2 
        if self.last == 2: return 1
        if self.last == 3: return 4
        if self.last == 4: return 3

    def interpret(self, outputs):
        '''
        0 wall did not change position,
        1 has moved in direction
        2 has moved in direction
            new position is the location of the oxygen system
        3 land of unknown
        '''
        # na pozici self.input je self.sc... co dal? left-hand rule wall follower
        self.sc = outputs[0]
        # zanes do mapy souradnice a status code
        self.map[(self.new_x, self.new_y)] = self.sc
        if self.sc in (1, 2):
            # hnuli jsme se v input smeru
            self.x = self.new_x
            self.y = self.new_y
            self.path.append(self.input)
        if self.x == 0 and self.y == 0:
            self.at_start += 1

    def where(self):
        '''
        navrhuje na zaklade aktualni pozice a okolnich bodu,
        jakym smerem se dat
        wall follower left-hand rule
        jdu dopredu (n) pokud to jde a kontroluju zed na levo
        pokud na levo neni zed, jdu na levo
        '''
        if self.at_start > 2: return None

        dirs = {
                1: self.map[(self.x, self.y+1)],
                2: self.map[(self.x, self.y-1)],
                3: self.map[(self.x+1, self.y)],
                4: self.map[(self.x-1, self.y)]
                }

        back = {1:2, 2:1, 3:4, 4:3}

        print(f'last {self.last}')

        if dirs.get(self.left) == 3:
            return self.left
        if dirs.get(self.left) == 0 and dirs.get(self.head) == 0 and dirs.get(self.right) == 0:
            return self.back
        if dirs.get(self.left) == 0 and dirs.get(self.head) == 0:
            return self.right
        if dirs.get(self.left) == 0:
            return self.head

        if dirs.get(self.left) == 1:
            return self.left

    def provide_input(self):
        '''
        1 north
        2 south
        3 west
        4 east
        '''
        #print(self.map)
        print(self.showmap())
        self.input = self.where()
        #print(f'moving {self.input}')

        if self.input == 1: # north
            self.new_y = self.y + 1
            self.new_x = self.x
        elif self.input == 2: # south
            self.new_y = self.y - 1
            self.new_x = self.x
        elif self.input == 3: # west
            self.new_x = self.x + 1
            self.new_y = self.y
        elif self.input == 4: # east
            self.new_x = self.x - 1
            self.new_y = self.y
        return self.input


if __name__ == '__main__':
    droid = Droid(input_day15.input_data)
    print(droid.stepcount)
