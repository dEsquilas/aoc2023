import pytest

def day_2(filename):
    lines = [l.strip() for l in open(filename)]
    id_sum = 0
    min_power = 0

    for line in lines:
        g = Game(line)
        if g.check_possible():
            id_sum += int(g.id)
        min_power += g.check_minimum_power()

    return id_sum, min_power


class Game:
    def __init__(self, line):

        tmp = line.split(": ")

        self.max = {
            "red": 12,
            "green": 13,
            "blue": 14,
        }
        self.id = tmp[0][5:]
        self.sets = []

        for set in tmp[1].split("; "):

            newSet = {}

            for cubes in set.split(", "):
                color = cubes.split(" ")[1]
                number = cubes.split(" ")[0]
                newSet[color] = int(number)

            self.sets.append(newSet)


    def check_possible(self):
        for set in self.sets:
            for color, value in set.items():
                if value > self.max[color]:
                    return False
        return True

    def check_minimum_power(self):
        colors = ["red", "green", "blue"]
        minimum = {
            "red": 1,
            "green": 1,
            "blue": 1,
        }

        for color in colors:
            for set in self.sets:
                if color in set and minimum[color] < set[color]:
                    minimum[color] = set[color]

        min_val = 1
        for color, value in minimum.items():
            min_val *= value

        return min_val

def test_day_2():
     assert day_2("test.txt") == (8, 2286)


test_day_2()
p1, p2 = day_2("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
