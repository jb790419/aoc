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
        tiles = {
                0: ' ',
                1: '#',
                2: 'M',
                3: '-',
                4: 'O'
                }
        if x == -1 and y == 0:
            self.score = tileid
        else:
            if tileid == 2:
                self.blocks.append((x, y, tileid))
            #build map
            self.map[(x,y)] = tiles.get(tileid)
        #print(self.showmap())

    def provide_input(self):
        # position of joystick 0 neutral, -1 left, 1 right
        print(self.showmap())
        # based on x of tileid 4 and x of tileid 3
        # if x of tileid 4 < x tileid 3, move left (-1)
        # if x of tileid 4 > x tileid 3, move right (1)
        ball_x, ball_y = next(((x,y) for (x,y), tile in self.map.items() if tile == 'O'), None)
        paddle_x, paddle_y = next(((x,y) for (x,y), tile in self.map.items() if tile == '-'), None)
        if ball_x > paddle_x:
            return 1
        elif ball_x < paddle_x:
            return -1

        #return int(input('paddle move (-1 left; 0 no move; 1 right: '))

    def showmap(self):
        # 39x24
        lines = [str() for _ in range(25)]
        for (x,y), value in sorted(self.map.items()):
            lines[y] += str(value)
        return '\n'.join(lines)

if __name__ == "__main__":

    #arc = Arcade(input_day13.data)
    #print(f'part1: {len(arc.blocks)}')

    input_day13.data[0] = 2
    arc = Arcade(input_day13.data)
    print(sorted(arc.map))
    print(arc.score)
