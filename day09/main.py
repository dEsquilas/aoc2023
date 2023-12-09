def day_9(filename):
    lines = open(filename).read().splitlines()

    p1 = 0
    p2 = 0

    for line in lines:
        numbers = [int(x) for x in line.split(" ")]

        all_numbers = [numbers]
        while not all_zeros(numbers):
            numbers = generate_below(numbers)
            all_numbers.append(numbers)

        p1, p2 = map(sum, zip((p1, p2), calculate_next(all_numbers)))

    return p1, p2

def calculate_next(all_numbers):

    all_numbers.reverse()
    all_numbers[0].append(0)

    for i in range(0, len(all_numbers) - 1):
        #p1
        p1_current = all_numbers[i][-1]
        p1_previous = all_numbers[i+1][-1]
        all_numbers[i+1].append(p1_current + p1_previous)
        #p2
        p2_current = all_numbers[i][0]
        p2_previous = all_numbers[i + 1][0]
        all_numbers[i+1].insert(0, p2_previous - p2_current)

    return all_numbers[-1][-1], all_numbers[-1][0]


def all_zeros(numbers):
    for number in numbers:
        if number != 0:
            return False

    return True

def generate_below(line):

    added = []

    for i in range(1, len(line)):
        added.append(line[i] - line[i-1])

    return added

def test_day_9():
    assert day_9("test.txt") == (114, 2)

test_day_9()
p1, p2 = day_9("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
