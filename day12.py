import unittest
from itertools import combinations

class Moon:
    def __init__(self, name, pos = (0, 0, 0), vel = (0, 0, 0)):
        self.name = name
        self.inipos = pos
        self.inivel = vel
        self.pos = pos
        self.vel = vel
        self.stepnum = 0

    def step(self):
        self.pos = tuple([(pos + vel) for (pos, vel) in zip(self.pos, self.vel)])
        self.stepnum += 1

    @property
    def pot(self):
        return sum(map(abs, self.pos))

    @property
    def kin(self):
        return sum(map(abs, self.vel))

    @property
    def tot(self):
        return self.pot * self.kin

    @property
    def is_initial(self):
        return self.stepnum > 0 and self.vel == self.inivel and self.pos == self.inipos

class MS:
    def __init__(self, moons = []):
        self.moons = moons

    def apply_gravity(self):
        for (m1, m2) in combinations(self.moons, 2):
            for axis in [0, 1, 2]:
                if m1.pos[axis] > m2.pos[axis]:
                    vel = list(m1.vel)
                    vel[axis] -= 1
                    m1.vel = tuple(vel)
                    vel = list(m2.vel)
                    vel[axis] += 1
                    m2.vel = tuple(vel)
                elif m1.pos[axis] < m2.pos[axis]:
                    vel = list(m1.vel)
                    vel[axis] += 1
                    m1.vel = tuple(vel)
                    vel = list(m2.vel)
                    vel[axis] -= 1
                    m2.vel = tuple(vel)

    def apply_velocity(self):
        for m in self.moons:
            m.step()

    def step(self):
        self.apply_gravity()
        self.apply_velocity()

    @property
    def is_initial(self):
        return self.moons[0].is_initial and self.moons[1].is_initial and self.moons[2].is_initial and self.moons[3].is_initial

    def simulate(self, steps):
        while steps > 0:
            steps -= 1
            self.step()

    def sim(self):
        st = 0
        while self.is_initial != True:
            self.step()
            st += 1
            print(st)
        return st

    @property
    def energy(self):
        total = 0
        for m in self.moons:
            total = total + m.tot
        return total


class TestMS(unittest.TestCase):
    '''
    Motion Simulator TEST
    '''
    def test_part1_1(self):
        io = Moon('Io', (-1, 0, 2))
        europa = Moon('Europa', (2, -10, -7))
        ganymede = Moon('Ganymede', (4, -8, 8))
        callisto = Moon('Callisto', (3, 5, -1))
        ms = MS([io, europa, ganymede, callisto])
        ms.simulate(1)

        self.assertEqual(io.pos, (2, -1, 1))
        self.assertEqual(io.vel, (3, -1, -1))
        self.assertEqual(europa.pos, (3, -7, -4))
        self.assertEqual(europa.vel, (1, 3, 3))
        self.assertEqual(ganymede.pos, (1, -7, 5))
        self.assertEqual(ganymede.vel, (-3, 1, -3))
        self.assertEqual(callisto.pos, (2, 2, 0))
        self.assertEqual(callisto.vel, (-1, -3, 1))

    def test_part1_10(self):
        io = Moon('Io', (-1, 0, 2))
        europa = Moon('Europa', (2, -10, -7))
        ganymede = Moon('Ganymede', (4, -8, 8))
        callisto = Moon('Callisto', (3, 5, -1))
        ms = MS([io, europa, ganymede, callisto])
        ms.simulate(10)

        self.assertEqual(io.pos, (2, 1, -3))
        self.assertEqual(io.vel, (-3, -2, 1))
        self.assertEqual(europa.pos, (1, -8, 0))
        self.assertEqual(europa.vel, (-1, 1, 3))
        self.assertEqual(ganymede.pos, (3, -6, 1))
        self.assertEqual(ganymede.vel, (3, 2, -3))
        self.assertEqual(callisto.pos, (2, 0, 4))
        self.assertEqual(callisto.vel, (1, -1, -1))
        self.assertEqual(ms.energy, 179)

    def test_part2_1(self):
        io = Moon('Io', (-1, 0, 2))
        europa = Moon('Europa', (2, -10, -7))
        ganymede = Moon('Ganymede', (4, -8, 8))
        callisto = Moon('Callisto', (3, 5, -1))
        ms = MS([io, europa, ganymede, callisto])
        self.assertEqual(ms.sim(), 2772)



if __name__ == "__main__":
    io = Moon('Io', (8, 0, 8))
    europa = Moon('Europa', (0, -5, -10))
    ganymede = Moon('Ganymede', (16, 10, -5))
    callisto = Moon('Callisto', (19, -10, -7))
    ms = MS([io, europa, ganymede, callisto])
    #ms.simulate(1000)
    #print(ms.energy)
    ms.sim()
