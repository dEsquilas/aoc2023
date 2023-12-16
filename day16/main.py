def day_16(filename):

    with (open(filename)) as file:
         layout = [list(x) for x in file.read().splitlines()]

    # (row, col)
    # each beam has a tuple with the current position and the direction it is going
    start_beam_p1 = ((0, 0), (0, 1), [])

    p1 = illuminate(layout, start_beam_p1)
    p2 = 0

    # first col

    for col_id in range(len(layout[0])):
        direction = (1, 0)
        position = (0, col_id)
        divisors_visited = []
        start_beam_p2 = (position, direction, divisors_visited)
        p2 = max(p2, illuminate(layout, start_beam_p2))

    # for first row

    for row_id in range(len(layout)):
        direction = (0, 1)
        position = (row_id, 0)
        divisors_visited = []
        start_beam_p2 = (position, direction, divisors_visited)
        p2 = max(p2, illuminate(layout, start_beam_p2))

    # for last row

    for row_id in range(len(layout)):
        direction = (-1, 0)
        position = (row_id, len(layout[0]) - 1)
        divisors_visited = []
        start_beam_p2 = (position, direction, divisors_visited)
        p2 = max(p2, illuminate(layout, start_beam_p2))

    # for last col

    for col_id in range(len(layout[0])):
        direction = (0, -1)
        position = (len(layout) - 1, col_id)
        divisors_visited = []
        start_beam_p2 = (position, direction, divisors_visited)
        p2 = max(p2, illuminate(layout, start_beam_p2))

    return p1,p2


def illuminate(layout, start_beam):

    illuminated = 0
    light_layout = [["." for x in range(len(layout[0]))] for y in range(len(layout))]

    beams = [start_beam]

    while beams:

        beam = beams.pop(0)

        position = beam[0]
        direction = beam[1]
        divisors_visited = beam[2]

        if position[0] >= len(layout) or position[1] >= len(layout[0]) or position[0] < 0 or position[1] < 0:
            continue

        light_layout[position[0]][position[1]] = "#"

        if layout[position[0]][position[1]] == ".":
            next_position = (position[0] + direction[0], position[1] + direction[1])
            next_direction = direction
            next_beam = (next_position, next_direction, divisors_visited)
            beams.append(next_beam)

        if layout[position[0]][position[1]] == "|":

            if direction == (1, 0) or direction == (-1, 0): # nothing occours
                next_position = (position[0] + direction[0], position[1] + direction[1])
                next_direction = direction
                next_beam = (next_position, next_direction, divisors_visited)
                beams.append(next_beam)
            else: # if it's perpendicular, generates 2 new beams

                if position in divisors_visited:
                    continue

                divisors_visited.append(position)

                next_direction_beam1 = (1, 0)
                next_direction_beam2 = (-1, 0)

                next_position_beam1 = (position[0] + next_direction_beam1[0], position[1] + next_direction_beam1[1])
                next_position_beam2 = (position[0] + next_direction_beam2[0], position[1] + next_direction_beam2[1])

                next_beam1 = (next_position_beam1, next_direction_beam1, divisors_visited)
                next_beam2 = (next_position_beam2, next_direction_beam2, divisors_visited)

                beams.append(next_beam1)
                beams.append(next_beam2)

        if layout[position[0]][position[1]] == "-":

            if direction == (0, 1) or direction == (0, -1):
                next_position = (position[0] + direction[0], position[1] + direction[1])
                next_direction = direction
                next_beam = (next_position, next_direction, divisors_visited)
                beams.append(next_beam)
            else:

                if position in divisors_visited:
                    continue

                divisors_visited.append(position)

                next_direction_beam1 = (0, 1)
                next_direction_beam2 = (0, -1)

                next_position_beam1 = (position[0] + next_direction_beam1[0], position[1] + next_direction_beam1[1])
                next_position_beam2 = (position[0] + next_direction_beam2[0], position[1] + next_direction_beam2[1])

                next_beam1 = (next_position_beam1, next_direction_beam1, divisors_visited)
                next_beam2 = (next_position_beam2, next_direction_beam2, divisors_visited)

                beams.append(next_beam1)
                beams.append(next_beam2)

        if layout[position[0]][position[1]] == "/":

            if direction == (1, 0):
                next_direction = (0, -1)
            if direction == (-1, 0):
                next_direction = (0, 1)
            if direction == (0, 1):
                next_direction = (-1, 0)
            if direction == (0, -1):
                next_direction = (1, 0)

            next_position = (position[0] + next_direction[0], position[1] + next_direction[1])
            next_beam = (next_position, next_direction, divisors_visited)

            beams.append(next_beam)

        if layout[position[0]][position[1]] == "\\":

            if direction == (1, 0):
                next_direction = (0, 1)
            if direction == (-1, 0):
                next_direction = (0, -1)
            if direction == (0, 1):
                next_direction = (1, 0)
            if direction == (0, -1):
                next_direction = (-1, 0)

            next_position = (position[0] + next_direction[0], position[1] + next_direction[1])
            next_beam = (next_position, next_direction, divisors_visited)

            beams.append(next_beam)


    for row_id in range(len(light_layout)):
        for col_id in range(len(light_layout[0])):
            if light_layout[row_id][col_id] == "#":
                illuminated += 1

    return illuminated

def test_day_16():
    assert day_16("test.txt") == (46, 51)

test_day_16()
p1, p2 = day_16("input.txt")
print("Part 1: ", p1)
print("Part 2: ", p2)