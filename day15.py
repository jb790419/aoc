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
        self.x = 0
        self.y = 0
        self.new_x = 0
        self.new_y = 0
        self.strings = {
                0: '#',
                1: '.',
                2: 'O',
                3: ' '
                }

        self.comp.process()

    def showmap(self):
        lines = []
        try:
            xs = [x for (x,y), val in self.map.items()]
            ys = [y for (x,y), val in self.map.items()]
            for y in range(min(ys), max(ys)+1):
                line = str()
                for x in range(min(xs), max(xs)+1):
                    if x == 0 and y == 0:
                        line += 'S'
                    if x == self.x and y == self.y:
                        line += 'X'
                    else:
                        line += self.strings.get(self.map[(x, y)])
                lines.append(line)
            return '\n'.join(lines)
        except ValueError:
            pass


    def interpret(self, outputs):
        '''
        0 wall did not change position,
        1 has moved in direction
        2 has moved in direction
        3 land of unknown
            new position is the location of the oxygen system
        '''
        self.sc = outputs[0]
        # zanes do mapy souradnice a 012
        self.map[(self.new_x, self.new_y)] = self.sc
        if self.sc in (1, 2):
            # hnuli jsme se v input smeru
            self.x = self.new_x
            self.y = self.new_y

    def where(self):
        '''
        navrhuje na zaklade aktualni pozice a okolnich bodu,
        jakym smerem se dat

        0. potrebuji vedet, co je okolo aktualni pozice
        1. pokud je tam neprozkoumany prostor, dat se do nej
        2. pokud je volny prostor, dat se do volneho prostoru
        '''
        north = self.map[(self.x, self.y+1)]
        south = self.map[(self.x, self.y-1)]
        west = self.map[(self.x+1, self.y)]
        east = self.map[(self.x-1, self.y)]

        dirs = {
                1: north,
                2: south,
                3: west,
                4: east
                }

        back = {1:2, 2:1, 3:4, 4:3} 

        prefer = random.randint(1,4)
        while dirs.get(prefer) not in (1,3):
            prefer = random.randint(1,4)
        return prefer

    def provide_input(self):
        '''
        1 north
        2 south
        3 west
        4 east
        '''
        print(self.showmap())
        self.input = self.where()
        print(f'moving {self.input}')

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
