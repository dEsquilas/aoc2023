def day_6(filename):

    file = [l.strip().split() for l in open(filename)]
    times = [int(x) for x in file[0][1:]]
    distances = [int(x) for x in file[1][1:]]

    p1 = 1

    for race in range(len(times)):
        cur_time = times[race]
        cur_distance = distances[race]
        min_hold_time, max_hold_time = calculate_min_max(cur_time, cur_distance)
        p1 *= (max_hold_time - min_hold_time + 1)

    time_p2 = int(''.join(map(str, times)))
    distance_p2 = int(''.join(map(str, distances)))

    min_p2, max_p2 = calculate_min_max(time_p2, distance_p2)

    return p1, max_p2 - min_p2 + 1

def calculate_min_max(cur_time, cur_distance):
    # count by bottom
    enought = False
    min_hold_time = 0
    max_hold_time = 0
    for x in range(1, cur_time - 1):
        hold = x
        speed = hold
        elapse_time = cur_time - hold
        distance_traveled = speed * elapse_time
        if distance_traveled > cur_distance:
            enought = True
            min_hold_time = hold
            break

    for x in reversed(range(1, cur_time - 1)):
        hold = x
        speed = hold
        elapse_time = cur_time - hold
        distance_traveled = speed * elapse_time
        if distance_traveled > cur_distance:
            enought = True
            max_hold_time = hold
            break

    return min_hold_time, max_hold_time

def test_day_6():
     assert day_6("test.txt") == (288, 71503)

test_day_6()
p1, p2 = day_6("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)