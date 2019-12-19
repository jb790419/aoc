import unittest
from unittest import skip
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
        for p in range(1, phase + 1):
            pl = []
            for it in range(1, len(inpl) + 1):
                current_phase = [initial_phase[i//it] for i in range(len(initial_phase)*it)]
                c = current_phase*(len(inpl)//len(initial_phase))
                d = c[1:]
                d.append(c[0])
                print(d)
                f = int(str(sum([x*y for x, y in zip(inpl, d)]))[-1])
                pl.append(f)
            inp.append(pl)
    return pl



    return None

class TestSignal(unittest.TestCase):
    def test_phase1(self):
        self.assertEqual(signal('12345678', phase=1), [4,8,2,2,6,1,5,8])
    def test_phase2(self):
        self.assertEqual(signal('12345678', phase=2), [3,4,0,4,0,4,3,8])
    def test_phase3(self):
        self.assertEqual(signal('12345678', phase=3), [0,3,4,1,5,5,1,8])
    def test_phase4(self):
        self.assertEqual(signal('12345678', phase=4), [0,1,0,2,9,4,9,8])

    @skip('')
    def test_large1(self):
        self.assertEqual(signal('80871224585914546619083218645595', phase=100), '24176176')

    @skip('')
    def test_large2(self):
        self.assertEqual(signal('19617804207202209144916044189917', phase=100), '73745418')

    @skip('')
    def test_large3(self):
        self.assertEqual(signal('69317163492948606335995924319873', phase=100), '52432133')


if __name__ == '__main__':

    input_data = '59750939545604170490448806904053996019334767199634549908834775721405739596861952646254979483184471162036292390420794027064363954885147560867913605882489622487048479055396272724159301464058399346811328233322326527416513041769256881220146486963575598109803656565965629866620042497176335792972212552985666620566167342140228123108131419565738662203188342087202064894410035696740418174710212851654722274533332525489527010152875822730659946962403568074408253218880547715921491803133272403027533886903982268040703808320401476923037465500423410637688454817997420944672193747192363987753459196311580461975618629750912028908140713295213305315022251918307904937'
    print(signal(input_data, phase=100))
