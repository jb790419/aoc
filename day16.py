import unittest
from unittest import skip
import math
'''
--- Day 16: Flawed Frequency Transmission ---
You're 3/4ths of the way through the gas giants. Not only do roundtrip signals
to Earth take five hours, but the signal quality is quite bad as well. You can
clean up the signal with the Flawed Frequency Transmission algorithm, or FFT.

As input, FFT takes a list of numbers. In the signal you received (your puzzle
input), each number is a single digit: data like 15243 represents the sequence
1, 5, 2, 4, 3.

FFT operates in repeated phases. In each phase, a new list is constructed with
the same length as the input list. This new list is also used as the input for
the next phase.

Each element in the new list is built by multiplying every value in the input
list by a value in a repeating pattern and then adding up the results. So, if
the input list were 9, 8, 7, 6, 5 and the pattern for a given element were 1,
2, 3, the result would be 9*1 + 8*2 + 7*3 + 6*1 + 5*2 (with each input element
on the left and each value in the repeating pattern on the right of each
multiplication). Then, only the ones digit is kept: 38 becomes 8, -17 becomes
7, and so on.

While each element in the output array uses all of the same input array
elements, the actual repeating pattern to use depends on which output element
is being calculated. The base pattern is 0, 1, 0, -1. Then, repeat each value
in the pattern a number of times equal to the position in the output list being
considered. Repeat once for the first element, twice for the second element,
three times for the third element, and so on. So, if the third element of the
output list is being calculated, repeating the values would produce: 0, 0, 0,
1, 1, 1, 0, 0, 0, -1, -1, -1.

When applying the pattern, skip the very first value exactly once. (In other
words, offset the whole pattern left by one.) So, for the second element of the
output list, the actual pattern used would be: 0, 1, 1, 0, 0, -1, -1, 0, 0, 1,
1, 0, 0, -1, -1, ....

After using this process to calculate each element of the output list, the
phase is complete, and the output list of this phase is used as the new input
list for the next phase, if any.  '''

def signal(instr, phase=0):
    initial_phase = [0,1,0,-1]
    final = list(map(int, instr))
    inp = []
    inp.append(final)
    pn = 1 
    while pn <= phase:
        pn += 1
        inpl = inp.pop(0)
        pl = []
        for it in range(1, len(inpl) + 1):
            current_phase = [initial_phase[i//it] for i in range(len(initial_phase)*it)]
            #c = current_phase*(len(inpl)//len(initial_phase))
            c = current_phase*(math.ceil(len(inpl)/4))
            d = c[1:]
            #d.append(c[0])
            #print(d[0:len(inpl)])
            f = int(str(sum([x*y for x, y in zip(inpl, d)]))[-1])
            pl.append(f)
        inp.append(pl)
    return pl

def first8(instr, phase = 0):

    return signal(instr, phase = phase)[:8]

def tenkilo(s):
    from itertools import cycle, accumulate
    offset = int(s[:7])
    digits = [int(i) for i in s]
    # If `rep` is `digits` repeated 10K times, construct: 
    #     arr = [rep[-1], rep[-2], ..., rep[offset]]
    l = 10000 * len(digits) - offset
    i = cycle(reversed(digits))
    arr = [next(i) for _ in range(l)]
    # Repeatedly take the partial sums mod 10
    for _ in range(100):
        arr = [n % 10 for n in accumulate(arr)]
    return "".join(str(i) for i in arr[-1:-9:-1])


class TestSignal(unittest.TestCase):
    def test_phase1(self):
        self.assertEqual(first8('12345678', phase=1), [4,8,2,2,6,1,5,8])
    def test_phase2(self):
        self.assertEqual(first8('12345678', phase=2), [3,4,0,4,0,4,3,8])
    def test_phase3(self):
        self.assertEqual(first8('12345678', phase=3), [0,3,4,1,5,5,1,8])
    def test_phase4(self):
        self.assertEqual(first8('12345678', phase=4), [0,1,0,2,9,4,9,8])

    def test_large1(self):
        self.assertEqual(first8('80871224585914546619083218645595', phase=100), [2,4,1,7,6,1,7,6])

    def test_large2(self):
        self.assertEqual(first8('19617804207202209144916044189917', phase=100), [7,3,7,4,5,4,1,8])

    def test_large3(self):
        self.assertEqual(first8('69317163492948606335995924319873', phase=100), [5,2,4,3,2,1,3,3])

    def test_part2(self):
        self.assertEqual(tenkilo('03036732577212944063491565474664'), '84462026')
        self.assertEqual(tenkilo('02935109699940807407585447034323'), '78725270')
        self.assertEqual(tenkilo('03081770884921959731165446850517'), '53553731')



if __name__ == '__main__':

    input_data = '59750939545604170490448806904053996019334767199634549908834775721405739596861952646254979483184471162036292390420794027064363954885147560867913605882489622487048479055396272724159301464058399346811328233322326527416513041769256881220146486963575598109803656565965629866620042497176335792972212552985666620566167342140228123108131419565738662203188342087202064894410035696740418174710212851654722274533332525489527010152875822730659946962403568074408253218880547715921491803133272403027533886903982268040703808320401476923037465500423410637688454817997420944672193747192363987753459196311580461975618629750912028908140713295213305315022251918307904937'
    #print(signal(input_data, phase=100))
    print(tenkilo(input_data))
