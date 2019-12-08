import unittest

def parse(data, wide, tall):
    '''parse data to layers by wide and tall'''
    data.rstrip('\n')
    intlist = list(map(int, list(data)))
    trojice = [tuple(intlist[i:i+wide]) for i in range(0, len(intlist), wide)]
    layers = [trojice[i:i+tall] for i in range(0, len(trojice), tall)]
    return layers

def parse_to_string(data, wide, tall):
    data.rstrip('\n')
    layers = [data[i:i+wide*tall] for i in range(0, len(data), wide*tall)]
    return layers

def part1_str(data, wide, tall):
    layers = parse_to_string(data, wide, tall)
    layer = sorted(layers, key=lambda layer: layer.count('0'))[0]
    return layer.count('1') * layer.count('2')

def part2_str(data, wide, tall):
    layers = parse_to_string(data, wide, tall)
    image = [str() for _ in range(tall)]
    for i in range(wide * tall):
        coord = divmod(i, wide)
        for layer in layers:
            if layer[i] != '2':
                image[coord[0]] += ' ' if layer[i] == '0' else '0'
                break
    return '\n'.join(image)

def less0(data, wide, tall):
    '''find layer that contains fewest 0 digits'''
    layers = parse(data, wide, tall)
    zerocount = []
    for i in range(len(layers)):
        zerocount.append(0) 
        for ntice in layers[i]:
            zerocount[i] = zerocount[i] + ntice.count(0)
    layer_index = zerocount.index(min(zerocount))
    return layers[layer_index]

def part1(data, wide, tall):
    '''
    count on chosen layer
    what is the number of 1 digits multiplied by number of 2 digits?
    count 1's
    count 2's
    pocet jednicek vynasobeny poctem dvojek
    '''
    layer = less0(data, wide, tall)
    number1 = 0
    number2 = 0
    for ntice in layer:
        number1 = number1 + ntice.count(1)
        number2 = number2 + ntice.count(2)
    return number1*number2

def part2(data, wide, tall):
    ''' result of decoding is is string wide x tall 01'''
    layers = parse(data, wide, tall)
    image = []
    for t in range(tall):
        line = str()
        for w in range(wide):
            '''
            mame cislo radku (t)
            mame cislo sloupce (w)
            potrebujeme zjistit 0 nebo 1
            musime projit vsechny vrstvy
            '''
            color = 2
            for layer in layers:
                if layer[t][w] != 2:
                    color = layer[t][w]
                    break
            line += ' ' if color == 0 else '0'
        image.append(line)
    return '\n'.join(image)

class TestLayers(unittest.TestCase):
    def test_parse(self):
        layer = parse('123456789012', 3, 2)
        self.assertListEqual(layer, [[(1,2,3), (4,5,6)], [(7,8,9), (0,1,2)]])
    def test_parse_to_string(self):
        layers = parse_to_string('123456789012', 3, 2)
        self.assertListEqual(layers, ['123456', '789012'])
    def test_zerocount(self):
        zerocount = less0('123456789012', 3, 2)
        self.assertListEqual(zerocount, [(1,2,3), (4,5,6)])
    def test_part1(self):
        res = part1('123456789012', 3, 2)
        self.assertEqual(res, 1*1)

    def test_decoding(self):
        self.assertEqual(part2('0222112222120000', 2, 2), " 0\n0 ")

if __name__ == '__main__':
    data = open('input8.txt', 'r').read().splitlines()
    print(part1(data[0], 25, 6))
    print(part1_str(data[0], 25, 6))
    print(part2(data[0], 25, 6))
    print(part2_str(data[0], 25, 6))
