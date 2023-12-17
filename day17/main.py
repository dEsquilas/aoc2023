import heapq

def day_17(filename):

    with open(filename) as file:
        heat_map = [[int(digit) for digit in line.strip()] for line in file]

    p1 = dijkstra(heat_map)
    p2 = dijkstra(heat_map, True)


    return p1,p2

def dijkstra(heat_map, part2=False):


    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    opposite_directions = {
        (0, 1): (0, -1),
        (0, -1): (0, 1),
        (1, 0): (-1, 0),
        (-1, 0): (1, 0),
    }
    distance_to_everything = {}
    # (distance, (x, y), last_direction, steps_last_direction)
    initial_node = (0, (0, 0), (None, None), 0)

    nodes_to_explore = []
    heapq.heappush(nodes_to_explore, initial_node)

    while nodes_to_explore:

        current_node = heapq.heappop(nodes_to_explore)
        distance, position, last_direction, steps_from_last_direction = current_node
        x = position[0]
        y = position[1]

        if (position, last_direction, steps_from_last_direction) in distance_to_everything:
            continue

        distance_to_everything[(position, last_direction, steps_from_last_direction)] = distance

        for d in directions:
            new_direction = (d[0],d[1])
            new_x = x + d[0]
            new_y = y + d[1]
            new_distance = distance + heat_map[x][y]
            current_steps = steps_from_last_direction


            if new_x < 0 or new_y < 0 or new_x >= len(heat_map) or new_y >= len(heat_map[0]):
                continue

            if last_direction != (None, None) and new_direction == opposite_directions[last_direction]:
                continue

            if not part2:
                if new_direction == last_direction and current_steps >= 3:
                    continue

                if new_direction == last_direction and current_steps < 3:
                    current_steps += 1

                if new_direction != last_direction:
                    current_steps = 1

            if part2:

                if new_direction == last_direction and current_steps <= 10:
                    current_steps += 1

                elif new_direction != last_direction and 4 <= current_steps <= 10:
                    current_steps = 1

                elif last_direction == (None, None):
                    current_steps = 1

                else:
                    continue

            next_node = (new_distance, (new_x, new_y), new_direction, current_steps)
            heapq.heappush(nodes_to_explore, next_node)


    solv = 999999999999999999999999

    for k,v in distance_to_everything.items():
        position, last_direction, steps_from_last_direction = k
        if position == (len(heat_map)-1, len(heat_map[0])-1):
            solv = min(solv, v+1)

    return solv


def test_day_17():
    assert day_17("test.txt") == (102, 94)

test_day_17()
p1, p2 = day_17("input.txt")
print("Part 1: ", p1)
print("Part 2: ", p2)