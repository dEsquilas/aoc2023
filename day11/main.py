def day_11(filename, a_size_p2):

    space_map = load_map(filename)

    p1 = calculate(space_map, 2)
    p2 = calculate(space_map, a_size_p2)

    return p1, p2


def load_map(filename):
    with (open(filename)) as file:
        space_map = [list(line) for line in file.read().splitlines()]

    for row_id in range(len(space_map)):
        empty_row = True
        for col_id in range(len(space_map[row_id])):
            if space_map[row_id][col_id] == "#":
                empty_row = False
                break
        if empty_row:
            for col_id in range(len(space_map[row_id])):
                space_map[row_id][col_id] = "a"

    for col_id in range(len(space_map[0])):
        empty_col = True
        for row_id in range(len(space_map)):
            if space_map[row_id][col_id] == "#":
                empty_col = False
                break
        if empty_col:
            for row_id in range(len(space_map)):
                space_map[row_id][col_id] = "a"

    return space_map

def calculate(space_map, a_size):
    distances = {}
    nodes = []
    ans = 0
    for row_id in range(len(space_map)):
        for col_id in range(len(space_map[row_id])):
            if space_map[row_id][col_id] == "#":
                nodes.append((row_id, col_id))

    for cur_node in nodes:
        for other_node in nodes:
            if cur_node == other_node:
                continue

            t1 = cur_node[0] - other_node[0]
            t2 = cur_node[1] - other_node[1]

            d = abs(t1) + abs(t2)

            a_count = 0

            min_0 = min(cur_node[0], other_node[0])
            max_0 = max(cur_node[0], other_node[0])
            min_1 = min(cur_node[1], other_node[1])
            max_1 = max(cur_node[1], other_node[1])

            for i in range(min_0, max_0):
                if space_map[i][cur_node[1]] == "a":
                    a_count += 1
            for i in range(min_1, max_1):
                if space_map[cur_node[0]][i] == "a":
                    a_count += 1

            if (cur_node, other_node) not in distances and (other_node, cur_node) not in distances:
                distances[(cur_node, other_node)] = d + a_count * (a_size - 1)

    for k,v in distances.items():
        ans += v

    return ans

def test_day_11():
    assert day_11("test.txt", 10) == (374, 1030)
    assert day_11("test.txt", 100) == (374, 8410)

test_day_11()
p1, p2 = day_11("input.txt", 1000000)
print("Part 1: ", p1)
print("Part 2: ", p2)
