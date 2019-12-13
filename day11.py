import unittest
from intcode import Intcode

class Hull:
    def __init__(self, intc, initial = 0):
        self.computer = Intcode(intc, initial)
        self.computer.max_outputs = 2
        self.computer.robot = self
        self.x = 0
        self.y = 0
        self.dir = 'up' # down right left
        self.map = {} # dvojice (x, y): barva pocatek je v 0, 0
        self.computer.process()

    def interpret(self, outputs):
        color, direction = outputs
        self.paint(color)
        self.turn_and_move(direction)
        return self.getcolor()

    def paint(self, color):
        
        self.map[(self.x, self.y)] = color

    def turn_and_move(self, direction):
        '''
        direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.
        '''
        if self.dir == 'up':
            self.dir = 'left' if direction == 0 else 'right'
        elif self.dir == 'down':
            self.dir = 'right' if direction == 0 else 'left'
        elif self.dir == 'left':
            self.dir = 'down' if direction == 0 else 'up'
        elif self.dir == 'right':
            self.dir = 'up' if direction == 0 else 'down'

        if self.dir == 'up':
            self.y -=1
        elif self.dir == 'down':
            self.y +=1
        elif self.dir == 'right':
            self.x +=1
        elif self.dir == 'left':
            self.x -=1

    def getcolor(self):
        try:
            return self.map[(self.x, self.y)]
        except KeyError:
            return 0

    def showmap(self):
        l = [str() for _ in range(6)]
        for k, v in sorted(self.map.items()):
            x, y = k
            l[y] += '.' if v == 0 else '#'

        return '\n'.join(l)





if __name__ == '__main__':
    input_data = [3,8,1005,8,318,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,29,1,107,12,10,2,1003,8,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,59,1,108,18,10,2,6,7,10,2,1006,3,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,93,1,1102,11,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,118,2,1102,10,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,145,1006,0,17,1006,0,67,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,173,2,1109,4,10,1006,0,20,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,201,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,224,1006,0,6,1,1008,17,10,2,101,5,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,256,2,1107,7,10,1,2,4,10,2,2,12,10,1006,0,82,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,294,2,1107,2,10,101,1,9,9,1007,9,988,10,1005,10,15,99,109,640,104,0,104,1,21102,1,837548352256,1,21102,335,1,0,1105,1,439,21102,1,47677543180,1,21102,346,1,0,1106,0,439,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,235190374592,1,21101,393,0,0,1105,1,439,21102,3451060455,1,1,21102,404,1,0,1105,1,439,3,10,104,0,104,0,3,10,104,0,104,0,21102,837896909668,1,1,21102,1,427,0,1105,1,439,21102,1,709580555020,1,21102,438,1,0,1105,1,439,99,109,2,21201,-1,0,1,21102,1,40,2,21102,1,470,3,21102,460,1,0,1106,0,503,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,465,466,481,4,0,1001,465,1,465,108,4,465,10,1006,10,497,1101,0,0,465,109,-2,2105,1,0,0,109,4,1201,-1,0,502,1207,-3,0,10,1006,10,520,21101,0,0,-3,21202,-3,1,1,22101,0,-2,2,21101,1,0,3,21101,0,539,0,1106,0,544,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,567,2207,-4,-2,10,1006,10,567,21202,-4,1,-4,1105,1,635,22101,0,-4,1,21201,-3,-1,2,21202,-2,2,3,21101,0,586,0,1105,1,544,22102,1,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,605,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,627,21202,-1,1,1,21101,627,0,0,105,1,502,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]
    robot = Hull(input_data)
    #print(robot.computer.count_inputs)
    #print(robot.computer.outputlist)
    #print(robot.map)
    print(len(robot.map.keys()))

    robot = Hull(input_data, initial = 1)
    print(robot.showmap())
