import time

def read_input(filename):
    lines = [line.strip() for line in open(filename, "r")]

    order = [0 if lines[0][x] == 'L' else 1 for x in range(len(lines[0]))]
    instructions = {line.split(' = ')[0]: tuple(line.split(' = ')[1].strip('()').split(', ')) for line in lines[2:]}

    return order, instructions

def day_8_p1(filename):

    order, instructions = read_input(filename)

    current_pointer = 0
    current_node = 'AAA'
    steps = 0

    while True:
        current_node = instructions[current_node][order[current_pointer]]
        steps += 1
        if current_node == 'ZZZ':
            break
        current_pointer += 1
        if current_pointer == len(order):
            current_pointer = 0

    return steps

def distance_to_first_z(instructions, order, start):

    steps = 0
    current_node = start
    current_pointer = 0

    while True:
        current_node = instructions[current_node][order[current_pointer]]
        steps += 1
        if current_node[2] == 'Z':
            break
        current_pointer += 1
        if current_pointer == len(order):
            current_pointer = 0

    return steps

def day_8_p2(filename):

    order, instructions = read_input(filename)
    starts_nodes = []

    for key, node in instructions.items():
        if key[2] == 'A':
            starts_nodes.append(key)

    # for node in current_nodes:
    max_distance = 0

    all_max_distances = []
    for node in starts_nodes:
        dtfz = distance_to_first_z(instructions, order, node)
        all_max_distances.append(dtfz)
        max_distance = max(dtfz, max_distance)

    cycle = 1
    steps = 0

    while True:
        steps = cycle * max_distance
        allowed = True
        for distance in all_max_distances:
            if steps % distance != 0:
                allowed = False
                break
        if allowed:
            break
        cycle += 1


    return steps


def test_day_8():
    assert day_8_p1("test.txt") == 2
    assert day_8_p1("test2.txt") == 6
    assert day_8_p2("test3.txt") == 6


test_day_8()
p1 = day_8_p1("input.txt")
start_time = time.perf_counter()
p2 = day_8_p2("input.txt")
end_time = time.perf_counter()

print("Part 1: ", p1)
print("Part 2: ", p2)
print(f"Execution time: {(end_time - start_time) :.3f} seconds")