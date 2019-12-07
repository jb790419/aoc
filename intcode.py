import unittest
import itertools
import copy

class Intcode:

    intc = []

    def __init__(self, intc, phase = None, inp = None):
        self.pos = 0
        self.intc = copy.copy(intc)
        self.input = inp
        self.phase = phase
        self.count_inputs = 0

    def immd(self, instr, index):
        '''test for immediate or positional parameter'''
        try:
            return str(instr)[index] == '1'
        except IndexError:
            return False

    def parval(self, idx):
        if idx == 1:
            idx_for_imm_test = -3
        elif idx == 2:
            idx_for_imm_test = -4

        return self.intc[self.pos + idx] if self.immd(self.intc[self.pos], idx_for_imm_test) else self.intc[self.intc[self.pos + idx]] 

    def process(self, pos = 0):

        self.pos = pos

        try:
            instr = int(str(self.intc[pos])[-2:])
        except IndexError:
            instr = self.intc[pos]

        if instr == 99:
            return self.intc
        elif instr == 1:
            self.intc[self.intc[pos + 3]] = self.parval(1) + self.parval(2)
            self.pos = pos + 4
        elif instr == 2:
            self.intc[self.intc[pos + 3]] = self.parval(1) * self.parval(2)
            self.pos = pos + 4
        elif instr == 3:
            self.intc[self.intc[pos + 1]] = self.phase if self.count_inputs == 0 else self.input
            self.count_inputs = self.count_inputs + 1
            self.pos = pos + 2
        elif instr == 4:
            self.output = self.parval(1) 
            self.pos = pos + 2
            try:
                self.nextamp.input = self.output
                self.nextamp.process(self.nextamp.pos)
            except AttributeError:
                pass
        elif instr == 5:
            if self.parval(1) != 0:
                self.pos = self.parval(2)
            else:
                self.pos = pos + 3

        elif instr == 6:
            if self.parval(1) == 0:
                self.pos = self.parval(2)
            else:
                self.pos = pos + 3
        elif instr == 7:
            if self.parval(1) < self.parval(2):
                self.intc[self.intc[pos + 3]] = 1
            else:
                self.intc[self.intc[pos + 3]] = 0
            self.pos = pos + 4
        elif instr == 8:
            if self.parval(1) == self.parval(2):
                self.intc[self.intc[pos + 3]] = 1
            else:
                self.intc[self.intc[pos + 3]] = 0
            self.pos = pos + 4
        else:
            raise KeyError(f'unknown instruction {instr}')

        return self.process(self.pos)

def serial(amp):
    for i in range(5):
        if i != 4:
            amp[i].nextamp = amp[i+1]

def feedback(amp):
    for i in range(5):
        if i == 4:
            amp[i].nextamp = amp[0]
        else:
            amp[i].nextamp = amp[i+1]


def amps(vstup, phases, connection = serial):
    amp = []

    for i in range(5):
        amp.append(Intcode(vstup, phases[i]))

    connection(amp)

    amp[0].input = 0
    amp[0].process()
    return amp[4].output

def signal_max(vstup):
    signals = []
    for phases in itertools.permutations([0,1,2,3,4]):
        signals.append(amps(vstup, phases, connection = serial))
    return max(signals)

def signal_max_feedback_loop(vstup):
    signals = []
    for phases in itertools.permutations([5,6,7,8,9]):
        signals.append(amps(vstup, phases, connection = feedback))
    return max(signals)

class TestIntcode(unittest.TestCase):
    def test_feedback_loop(self):
        vstup = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
        phases = (9,8,7,6,5)
        result = 139629729
        self.assertEqual(amps(vstup, phases, connection = feedback), result)

        vstup = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
        phases = (9,7,8,5,6)
        result = 18216
        self.assertEqual(amps(vstup, phases, connection = feedback), result)


    def test_amps(self):
        vstup = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
        phases = (4,3,2,1,0)
        result = 43210
        self.assertEqual(amps(vstup, phases), result)

        vstup = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
        phases = (0,1,2,3,4)
        result = 54321
        self.assertEqual(amps(vstup, phases), result)
        vstup = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
        phases = (1,0,4,3,2)
        result = 65210
        self.assertEqual(amps(vstup, phases), result)

    def test_input_output(self):
        vstup = [1,0,0,0,99]
        comp = Intcode(vstup)
        self.assertListEqual(comp.intc, [1,0,0,0,99])
        intc = comp.process()
        self.assertListEqual(intc, [2,0,0,0,99])
        vstup = [1,1,1,4,99,5,6,0,99]
        comp = Intcode(vstup)
        self.assertListEqual(comp.process(), [30,1,1,4,2,5,6,0,99])

    def test_3(self):
        vstup = [3,0,4,0,99]
        comp = Intcode(vstup, 3)
        comp.process()
        self.assertEqual(comp.output, 3)

    def test_op(self):
        vstup = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
        comp = Intcode(vstup, 0)
        comp.process()
        self.assertEqual(comp.output, 0)

        comp = Intcode(vstup, 15)
        comp.process()
        self.assertEqual(comp.output, 1)

    def test_big(self):
        vstup = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        comp = Intcode(vstup, 7)
        comp.process()
        self.assertEqual(comp.output, 999)

        comp = Intcode(vstup, 8)
        comp.process()
        self.assertEqual(comp.output, 1000)

        comp = Intcode(vstup, 9)
        comp.process()
        self.assertEqual(comp.output, 1001)



if __name__ == '__main__':
    vstup = [3,8,1001,8,10,8,105,1,0,0,21,34,59,68,85,102,183,264,345,426,99999,3,9,101,3,9,9,102,3,9,9,4,9,99,3,9,1002,9,4,9,1001,9,2,9,1002,9,2,9,101,5,9,9,102,5,9,9,4,9,99,3,9,1001,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,2,9,1001,9,5,9,4,9,99,3,9,1002,9,3,9,1001,9,5,9,102,3,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99]
    print(signal_max(vstup))
    print(signal_max_feedback_loop(vstup))
