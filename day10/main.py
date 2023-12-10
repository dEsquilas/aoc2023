DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
PIPE_TYPES = ["F", "7", "J", "L", "-", "|", "S"]

def day_10(filename):
    with (open(filename)) as file:
        pipes_map = [list(line) for line in file.read().splitlines()]

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

    pipes_map.insert(0, ["." for _ in range(len(pipes_map[0]))])
    for row_index in range(len(pipes_map)):
        pipes_map[row_index].insert(0, ".")
        pipes_map[row_index].append(".")
    pipes_map.append(["." for _ in range(len(pipes_map[0]))])

    # find surrounding values from Start

    starter_cell = (-1, -1)

    for row_index in range(len(pipes_map)):
        for col_index in range(len(pipes_map[row_index])):
            if pipes_map[row_index][col_index] == "S":
                starter_cell = (row_index, col_index)
                break
        if starter_cell != (-1, -1):
            break

    current_cell = starter_cell
    from_d = ""

    for d in DIRECTIONS:
        if 0 <= starter_cell[0] + d[0] < len(pipes_map) and 0 <= starter_cell[1] + d[1] < len(pipes_map[0]) and  pipes_map[starter_cell[0] + d[0]][starter_cell[1] + d[1]] != ".":
            next_cell = (starter_cell[0] + d[0], starter_cell[1] + d[1])
            from_d = from_direction(starter_cell, next_cell)
            current_cell = next_cell
            if from_d in pipes[pipes_map[current_cell[0]][current_cell[1]]]:
                break
    steps = 1

    used_tiles = [["*" for x in range(len(pipes_map[y]))] for y in range(len(pipes_map))]
    used_tiles[current_cell[0]][current_cell[1]] = "U"

    # PART 1

    while True:

        current_pipe = pipes[pipes_map[current_cell[0]][current_cell[1]]]
        to_apply = current_pipe[from_d]
        next_cell = (current_cell[0] + to_apply[0], current_cell[1] + to_apply[1])
        from_d = from_direction(current_cell, next_cell)
        current_cell = next_cell

        steps += 1

        used_tiles[current_cell[0]][current_cell[1]] = "U"

        if pipes_map[current_cell[0]][current_cell[1]] == "S":
            break

    used_tiles[starter_cell[0]][starter_cell[1]] = "U"

    for row_index in range(len(pipes_map)):
        for col_index in range(len(pipes_map[row_index])):
            if used_tiles[row_index][col_index] == "*" and pipes_map[row_index][col_index] in PIPE_TYPES:
                used_tiles[row_index][col_index] = "N"

    # tiled used are marked with U
    # non used tiles are marked with N
    # free spaces are marked with *

    # create a map using the real pipes for flood it

    extended_map = extend_map(pipes_map)

    # use the flood system. You can flood all floor until you take a limit or a used pipe
    # if the pipe is not used, count as flooded

    flood(extended_map)

    tiles_not_reach_exterior = 0

    for row_index in range(len(pipes_map)):
        for col_index in range(len(pipes_map[row_index])):
            # translate center for growed map
            # every center part of the pipe is always 1
            t_col = col_index * 3 + 1
            t_row = row_index * 3 + 1
            if extended_map[t_row][t_col] == 1 and pipes_map[row_index][col_index] in PIPE_TYPES and used_tiles[row_index][col_index] == "N": # it's a pipe and it's not used
                # can the pipe reach the exterior?
                # the pipe can reach the exterior if any part of the full tile
                # is flooded (2)
                can_reach_exterior = False
                for c in range(t_col -1, t_col + 1):
                    for r in range(t_row -1, t_row + 1):
                        if extended_map[r][c] == 2:
                            can_reach_exterior = True
                            break
                if not can_reach_exterior:
                    tiles_not_reach_exterior += 1
            if used_tiles[row_index][col_index] == "*" and pipes_map[row_index][col_index] == ".":
                if extended_map[t_row][t_col] not in (1, 2): # it's a free space and is not flooded
                    tiles_not_reach_exterior += 1

    return steps//2, tiles_not_reach_exterior

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

def flood(current_map):
    start = (0, 0)
    next_cells = [start]
    while len(next_cells) > 0:
        current_cell = next_cells.pop(0)
        for d in DIRECTIONS:
            if 0 <= current_cell[0] + d[0] < len(current_map) and 0 <= current_cell[1] + d[1] < len(current_map[0]): # it's on limits
                if current_map[current_cell[0] + d[0]][current_cell[1] + d[1]] == 0:
                    current_map[current_cell[0] + d[0]][current_cell[1] + d[1]] = 2
                    next_cells.append((current_cell[0] + d[0], current_cell[1] + d[1]))
                if current_map[current_cell[0] + d[0]][current_cell[1] + d[1]] in ("N", "*"):
                    current_map[current_cell[0] + d[0]][current_cell[1] + d[1]] = "."
                    next_cells.append((current_cell[0] + d[0], current_cell[1] + d[1]))

def extend_map(current_map):
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

    extended_map =  [[] for _ in range(len(current_map) * 3)]
    current_extended_map_row_index = 0

    # Generate a map using 0 as free space
    # and 1 as pipe

    for row_index in range(len(current_map)):
        for col_index in range(len(current_map[row_index])):
            current_tile = current_map[row_index][col_index]
            subtile = tiles[current_tile]
            for subtile_row_id in range(len(subtile)):
                extended_map[subtile_row_id + current_extended_map_row_index].extend(subtile[subtile_row_id])
        current_extended_map_row_index += 3

    return extended_map

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
