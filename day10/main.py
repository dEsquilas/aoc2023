def day_10(filename):
    map = [[x for x in list(line)] for line in open(filename).read().splitlines()]

    # (row_index, col_index)
    # from_<directon>

    pipes = {
        ".": {},
        "|": {
            "up": (1, 0),
            "down": (-1, 0),
        },
        "-": {
            "left": (0, 1),
            "right": (0, -1),
        },
        "L": {
            "up": (0, 1),
            "right": (-1, 0),
        },
        "J": {
            "up": (0, -1),
            "left": (-1, 0),
        },
        "7": {
            "down": (0, -1),
            "left": (1, 0),
        },
        "F": {
            "down": (0, 1),
            "right": (1, 0),
        }
    }


    # grow map

    map.insert(0, ["." for _ in range(len(map[0]))])
    for row_index in range(len(map)):
        map[row_index].insert(0, ".")
        map[row_index].append(".")
    map.append(["." for _ in range(len(map[0]))])

    # find sorrounding values

    for row_index in range(len(map)):
        for col_index in range(len(map[row_index])):
            if map[row_index][col_index] == "S":
                S = (row_index, col_index)
                break

    dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    current_cell = S

    for d in dir:
        if 0 <= S[0] + d[0] < len(map) and 0 <= S[1] + d[1] < len(map[0]) and  map[S[0] + d[0]][S[1] + d[1]] != ".":
            next_cell = (S[0] + d[0], S[1] + d[1])
            from_d = from_direction(S, next_cell)
            current_cell = next_cell
            if from_d in pipes[map[current_cell[0]][current_cell[1]]]:
                break




    growed_map = grow_map(map)
    steps = 1

    used_tiles = [["*" for x in range(len(map[y]))] for y in range(len(map))]
    used_tiles[current_cell[0]][current_cell[1]] = "U"

    # PART 1

    while True:

        current_pipe = pipes[map[current_cell[0]][current_cell[1]]]
        to_apply = current_pipe[from_d]
        next_cell = (current_cell[0] + to_apply[0], current_cell[1] + to_apply[1])
        from_d = from_direction(current_cell, next_cell)
        current_cell = next_cell

        steps += 1

        used_tiles[current_cell[0]][current_cell[1]] = "U"

        if map[current_cell[0]][current_cell[1]] == "S":
            break

    used_tiles[S[0]][S[1]] = "U"
    print(S)

    print_map(used_tiles, True)

    print("\n\n\n\n")
    ops = ["F", "7", "J", "L", "-", "|", "S"]
    for row_index in range(len(map)):
        for col_index in range(len(map[row_index])):
            if used_tiles[row_index][col_index] == "*" and map[row_index][col_index] in ops:
                used_tiles[row_index][col_index] = "N"

    print("\n\n\n\n")
    pre_flood(used_tiles)
    print_map(used_tiles, True)

    # PART 2

    # print_map(growed_map, True)
    # print("\n\n\n\n")
    # flood(growed_map)
    # print_map(growed_map, True)

    #print_map(growed_map, True)

    print("\n\n\n\n")
    flood(growed_map)

    #print_map(growed_map, True)

    count = 0

    on1 = []
    on2 = []
    on3 = []

    for row_index in range(len(map)):
        for col_index in range(len(map[row_index])):
            #translate center
            t_col = col_index * 3 + 1
            t_row = row_index * 3 + 1
            if growed_map[t_row][t_col] == 1 and map[row_index][col_index] in ops and used_tiles[row_index][col_index] == "N": # es una tuberia y no esta usada
                # la tuberia puede llegar al exterior?
                can_reach_exterior = False
                for c in range(t_col -1, t_col + 1):
                    for r in range(t_row -1, t_row + 1):
                        if growed_map[r][c] == 2:
                            can_reach_exterior = True
                            break
                if not can_reach_exterior:
                    on2.append((row_index, col_index))
                    count += 1
            if used_tiles[row_index][col_index] == "*" and map[row_index][col_index] == ".":
                if growed_map[t_row][t_col] not in (1, 2): # es un trozo de "tierra" y no se ha inhundado
                    count += 1
                    on3.append((row_index, col_index))

    print_map(growed_map, True)

    print(on1)
    print(on2)
    print(on3)
    print(len(on1), len(on2), len(on3))

    return steps//2, count


def from_direction(current_cell, next_cell):
    from_direction_int = (next_cell[0] - current_cell[0], next_cell[1] - current_cell[1])
    if from_direction_int == (0, 1):
        return "left"
    elif from_direction_int == (0, -1):
        return "right"
    elif from_direction_int == (1, 0):
        return "up"
    elif from_direction_int == (-1, 0):
        return "down"

def print_map(map, v=False):

    for row_index in range(len(map)):
        for col_index in range(len(map[row_index])):
            c = map[row_index][col_index]
            if not v:
                print(f" {c:3} ", end="")
            else:
                if(c == 0):
                    print("·", end="")
                else:
                    print(c, end="")
                # if col_index % 3 == 2:
                #     print(" ", end="")
        print()
        # if row_index % 3 == 2:
        #     print()

def pre_flood(map):
    start = (0, 0)
    next_cells = [start]
    dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    while len(next_cells) > 0:
        current_cell = next_cells.pop(0)
        for d in dir:
            if 0 <= current_cell[0] + d[0] < len(map) and 0 <= current_cell[1] + d[1] < len(map[0]):  # it's on limits
                if map[current_cell[0] + d[0]][current_cell[1] + d[1]] in ("N", "*"):
                    map[current_cell[0] + d[0]][current_cell[1] + d[1]] = "."
                    next_cells.append((current_cell[0] + d[0], current_cell[1] + d[1]))
def flood(map):
    start = (0, 0)
    next_cells = [start]
    dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    while len(next_cells) > 0:
        current_cell = next_cells.pop(0)
        for d in dir:
            if 0 <= current_cell[0] + d[0] < len(map) and 0 <= current_cell[1] + d[1] < len(map[0]): # it's on limits
                if map[current_cell[0] + d[0]][current_cell[1] + d[1]] == 0:
                    map[current_cell[0] + d[0]][current_cell[1] + d[1]] = 2
                    next_cells.append((current_cell[0] + d[0], current_cell[1] + d[1]))


def grow_map(map):
    tiles = {
        "|": [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ],
        "-": [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ],
        "L": [
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ],
        "J": [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 0],
        ],
        "7": [
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
        ],
        "F": [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 0],
        ],
        "." : [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        "S": [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]
    }

    growed_map =  [[] for _ in range(len(map) * 3)]
    current_growed_map_row_index = 0
    for row_index in range(len(map)):
        for col_index in range(len(map[row_index])):
            current_tile = map[row_index][col_index]

            subtile = tiles[current_tile]

            for subtile_row_id in range(len(subtile)):
                growed_map[subtile_row_id + current_growed_map_row_index].extend(subtile[subtile_row_id])

        current_growed_map_row_index += 3


    return growed_map


def test_day_10():
    assert day_10("test.txt")[0] == 8
    assert day_10("test2.txt")[1] == 8
    assert day_10("test3.txt")[1] == 10
    assert day_10("test4.txt")[1] == 4
    assert day_10("test5.txt")[1] == 4

test_day_10()
p1, p2 = day_10("input.txt")
print("Part 1: ", p1)
print("Part 2: ", p2)
