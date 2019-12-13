import unittest
import itertools

class Intcode:

    def __init__(self, intc, phase = None):
        self.pos = 0
        self.intc = {i:intc[i] for i in range(len(intc))}
        self.input = None
        self.phase = phase
        self.count_inputs = 0
        self.base = 0 # base for relative position mode
        self.outputlist = []
        self.output_number = 0
        self.max_outputs = None
        self.robot = None

    def talk_to_robot(self):
        if self.robot is None:
            pass
        else:
            self.input = self.robot.interpret(self.outputlist[-(self.max_outputs):])

    def parval(self, idx, return_value = True):
        '''
        21101 instruction code
           01 opcode
          1   mode of first parameter
         1    mode of second parameter
        2     mode of third parameter 
        '''
        mode = f'{self.intc[self.pos]:05}'[-(idx + 2)]
        modes = {
                '0': self.intc[self.pos + idx], # positional mode
                '1': self.pos + idx, # immediate mode
                '2': self.base + self.intc[self.pos + idx] # relative mode
                }
        address = modes.get(mode)
        if return_value:
            try:
                return self.intc[address]
            except KeyError:
                return 0
        else:
            return address

    def add(self):
        value = self.parval(1) + self.parval(2)
        address = self.parval(3, False)
        self.intc[address] = value
        self.pos += 4

    def multiply(self):
        value = self.parval(1) * self.parval(2)
        address = self.parval(3, False)
        self.intc[address] = value
        self.pos += 4

    def take_input(self):
        address = self.parval(1, False)
        if self.count_inputs == 0:
            value = self.phase
        else:
            value = self.input

        if value is None:
            value = self.robot.provide_input()

        self.count_inputs += 1
        self.intc[address] = value
        self.pos += 2

    def produce_output(self):
        self.output = self.parval(1)
        self.outputlist.append(self.output)
        self.output_number +=1
        self.pos += 2
        if self.max_outputs is not None and self.output_number == self.max_outputs:
            self.output_number = 0
            self.talk_to_robot()
        try:
            self.nextamp.input = self.output
            self.nextamp.process()
        except AttributeError:
            pass

    def jump_if_true(self):
        self.pos = self.parval(2) if self.parval(1) != 0 else self.pos + 3

    def jump_if_false(self):
        self.pos = self.parval(2) if self.parval(1) == 0 else self.pos + 3

    def less_than(self):
        value = 1 if self.parval(1) < self.parval(2) else 0
        address = self.parval(3, False)
        self.intc[address] = value
        self.pos += 4

    def equals(self):
        value = 1 if self.parval(1) == self.parval(2) else 0
        address = self.parval(3, False)
        self.intc[address] = value
        self.pos += 4

    def offset_base(self):
        self.base = self.base + self.parval(1)
        self.pos += 2

    def process(self):
        instructions = {
                1: self.add,
                2: self.multiply,
                3: self.take_input,
                4: self.produce_output,
                5: self.jump_if_true,
                6: self.jump_if_false,
                7: self.less_than,
                8: self.equals,
                9: self.offset_base,
                }
        opcode = int(str(f'{self.intc[self.pos]:05}')[-2:])
        while opcode < 99:
            processor = instructions.get(opcode)
            processor()
            opcode = int(str(f'{self.intc[self.pos]:05}')[-2:])
        return self.intc

def serial(amp):
    for i in range(len(amp)):
        if i < len(amp) - 1:
            amp[i].nextamp = amp[i+1]

def feedback(amp):
    for i in range(len(amp)):
        if i == len(amp) - 1:
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
        self.assertListEqual(list(comp.intc.values()), [1,0,0,0,99])
        intc = comp.process()
        self.assertListEqual(list(intc.values()), [2,0,0,0,99])
        vstup = [1,1,1,4,99,5,6,0,99]
        comp = Intcode(vstup)
        self.assertListEqual(list(comp.process().values()), [30,1,1,4,2,5,6,0,99])

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

    def test_day9(self):
        vstup = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        comp = Intcode(vstup)
        comp.process()
        self.assertListEqual(comp.outputlist, vstup)

        vstup = [1102,34915192,34915192,7,4,7,99,0]
        comp = Intcode(vstup)
        comp.process()
        self.assertEqual(len(str(abs(comp.output))), 16)

        vstup = [104,1125899906842624,99]
        comp = Intcode(vstup)
        comp.process()
        self.assertEqual(comp.output, 1125899906842624)

        vstup = [109,2,99]
        comp = Intcode(vstup)
        comp.process()
        self.assertEqual(comp.base, 2)

        vstup = [109,2,204,-2,99]
        comp = Intcode(vstup)
        comp.process()
        self.assertEqual(comp.base, 2)
        self.assertEqual(comp.output, 109)

        vstup = [203, 0, 99]
        comp = Intcode(vstup, 12)
        comp.base = 1
        intc = comp.process()
        self.assertListEqual(list(intc.values()), [203, 12, 99])

if __name__ == '__main__':
    vstup = [3,8,1001,8,10,8,105,1,0,0,21,34,59,68,85,102,183,264,345,426,99999,3,9,101,3,9,9,102,3,9,9,4,9,99,3,9,1002,9,4,9,1001,9,2,9,1002,9,2,9,101,5,9,9,102,5,9,9,4,9,99,3,9,1001,9,4,9,4,9,99,3,9,101,3,9,9,1002,9,2,9,1001,9,5,9,4,9,99,3,9,1002,9,3,9,1001,9,5,9,102,3,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99]
    print(f'day7 part1: {signal_max(vstup)}')
    print(f'day7 part2: {signal_max_feedback_loop(vstup)}')
    vstup = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,0,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,396,1029,1101,0,356,1023,1101,401,0,1028,1101,24,0,1008,1101,33,0,1019,1101,35,0,1010,1102,359,1,1022,1102,32,1,1001,1101,37,0,1004,1101,0,31,1009,1101,0,30,1003,1101,28,0,1002,1102,1,36,1014,1102,20,1,1012,1101,21,0,1000,1101,0,22,1015,1102,23,1,1013,1102,1,1,1021,1102,1,39,1007,1102,26,1,1017,1101,0,38,1016,1101,0,437,1024,1102,432,1,1025,1101,0,421,1026,1101,0,29,1005,1101,27,0,1011,1102,1,0,1020,1101,0,25,1018,1101,0,414,1027,1102,34,1,1006,109,6,2108,33,-3,63,1005,63,201,1001,64,1,64,1105,1,203,4,187,1002,64,2,64,109,14,21108,40,40,-6,1005,1014,221,4,209,1105,1,225,1001,64,1,64,1002,64,2,64,109,-21,2102,1,3,63,1008,63,28,63,1005,63,251,4,231,1001,64,1,64,1106,0,251,1002,64,2,64,109,12,2101,0,-3,63,1008,63,21,63,1005,63,275,1001,64,1,64,1105,1,277,4,257,1002,64,2,64,109,-10,1207,1,27,63,1005,63,293,1105,1,299,4,283,1001,64,1,64,1002,64,2,64,109,9,21108,41,42,3,1005,1013,315,1105,1,321,4,305,1001,64,1,64,1002,64,2,64,109,-12,1202,6,1,63,1008,63,37,63,1005,63,347,4,327,1001,64,1,64,1105,1,347,1002,64,2,64,109,29,2105,1,-4,1105,1,365,4,353,1001,64,1,64,1002,64,2,64,109,-17,2108,32,-9,63,1005,63,387,4,371,1001,64,1,64,1105,1,387,1002,64,2,64,109,17,2106,0,1,4,393,1105,1,405,1001,64,1,64,1002,64,2,64,109,1,2106,0,-1,1001,64,1,64,1106,0,423,4,411,1002,64,2,64,109,-13,2105,1,9,4,429,1106,0,441,1001,64,1,64,1002,64,2,64,109,3,21107,42,41,-1,1005,1017,461,1001,64,1,64,1106,0,463,4,447,1002,64,2,64,109,-4,21107,43,44,1,1005,1015,481,4,469,1106,0,485,1001,64,1,64,1002,64,2,64,109,-6,21101,44,0,6,1008,1014,47,63,1005,63,505,1106,0,511,4,491,1001,64,1,64,1002,64,2,64,109,-6,1208,-1,32,63,1005,63,529,4,517,1105,1,533,1001,64,1,64,1002,64,2,64,109,11,1205,7,545,1106,0,551,4,539,1001,64,1,64,1002,64,2,64,109,11,21102,45,1,-7,1008,1017,48,63,1005,63,575,1001,64,1,64,1106,0,577,4,557,1002,64,2,64,109,-8,1206,5,593,1001,64,1,64,1105,1,595,4,583,1002,64,2,64,109,7,1206,-3,609,4,601,1106,0,613,1001,64,1,64,1002,64,2,64,109,-10,2101,0,-6,63,1008,63,39,63,1005,63,635,4,619,1106,0,639,1001,64,1,64,1002,64,2,64,109,-9,1208,0,39,63,1005,63,655,1106,0,661,4,645,1001,64,1,64,1002,64,2,64,109,4,2107,25,0,63,1005,63,681,1001,64,1,64,1105,1,683,4,667,1002,64,2,64,109,-5,2107,31,-2,63,1005,63,701,4,689,1106,0,705,1001,64,1,64,1002,64,2,64,109,19,1205,-1,719,4,711,1105,1,723,1001,64,1,64,1002,64,2,64,109,-17,1201,3,0,63,1008,63,24,63,1005,63,745,4,729,1106,0,749,1001,64,1,64,1002,64,2,64,109,13,21102,46,1,-3,1008,1015,46,63,1005,63,771,4,755,1105,1,775,1001,64,1,64,1002,64,2,64,109,-13,1207,4,32,63,1005,63,793,4,781,1106,0,797,1001,64,1,64,1002,64,2,64,109,7,2102,1,-9,63,1008,63,27,63,1005,63,821,1001,64,1,64,1105,1,823,4,803,1002,64,2,64,109,-18,1201,8,0,63,1008,63,25,63,1005,63,847,1001,64,1,64,1106,0,849,4,829,1002,64,2,64,109,23,21101,47,0,2,1008,1019,47,63,1005,63,871,4,855,1106,0,875,1001,64,1,64,1002,64,2,64,109,-22,1202,5,1,63,1008,63,19,63,1005,63,899,1001,64,1,64,1106,0,901,4,881,4,64,99,21102,27,1,1,21102,1,915,0,1105,1,922,21201,1,25165,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,942,1,0,1105,1,922,22102,1,1,-1,21201,-2,-3,1,21101,0,957,0,1105,1,922,22201,1,-1,-2,1106,0,968,21201,-2,0,-2,109,-3,2105,1,0]
    comp = Intcode(vstup, 1)
    comp.process()
    print(f'day9 part1: {comp.outputlist}')

    comp = Intcode(vstup, 2)
    comp.process()
    print(f'day9 part2: {comp.output}')
