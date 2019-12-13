from intcode import Intcode
import input_day13

class Arcade:
    def __init__(self, intc):
        self.comp = Intcode(intc, 0)
        self.comp.max_outputs = 3
        self.comp.robot = self
        self.blocks = []
        self.map = {}
        self.score = 0

        self.comp.process()

    def interpret(self, outputs):
        x, y, tileid = outputs
        if x == -1 and y == 0:
            self.score = tileid
        else:
            if tileid == 2:
                self.blocks.append((x, y, tileid))
            #build map
            self.map[(x,y)] = tileid
        # position of joystick 0 neutral, -1 left, 1 right
        print(self.map)
        return None


if __name__ == "__main__":

    #arc = Arcade(input_day13.data)
    #print(f'part1: {len(arc.blocks)}')

    input_day13.data[0] = 2
    arc = Arcade(input_day13.data)
    print(arc.map)
    print(arc.score)
