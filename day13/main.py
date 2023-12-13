def day_13(filename):

    with (open(filename)) as file:
         maps = file.read().split("\n\n")

    p1 = 0
    p2 = 0

    # check horizontal

    for m in maps:
        current_map = m.split("\n")
        mirror_count_h_p1 = check_map_p1(current_map)
        mirror_count_v_p1 = 0

        mirror_count_h_p2 = check_map_p2(current_map)
        mirror_count_v_p2 = 0

        if mirror_count_h_p1 == 0 or mirror_count_h_p2 == 0:
            reversed_map = reverse_map(current_map)

        if mirror_count_h_p1 == 0:
            mirror_count_v_p1 = check_map_p1(reversed_map)

        if mirror_count_h_p2 == 0:
            mirror_count_v_p2 = check_map_p2(reversed_map)

        p1 += mirror_count_h_p1 * 100 + mirror_count_v_p1
        p2 += mirror_count_h_p2 * 100 + mirror_count_v_p2

    return p1,p2

def reverse_map(current_map):
    new_map = []
    for i in range(len(current_map[0])):
        new_row = []
        for j in range(len(current_map)):
            new_row.append(current_map[j][i])
        new_map.append(new_row)
    return new_map

def check_map_p1(current_map):

    count = 0

    for i in range(1, len(current_map)):
        if current_map[i] == current_map[i-1]:
            # check mirror
            mirror_found = True
            for mirror_index in range(0, i - 1):
                fail_count = 0
                left_index = i - mirror_index - 2
                right_index = i + mirror_index + 1
                if right_index < len(current_map):
                    if current_map[left_index] != current_map[right_index]:
                        mirror_found = False
                        break

            if mirror_found:
                count += i
                break

    return count


def check_map_p2(current_map):

    for i in range(1, len(current_map)):

        fails_on = -1
        diff = sum(1 for a, b in zip(current_map[i], current_map[i - 1]) if a != b)
        if diff > 1:
            continue

        if diff == 1:
            fails_on = i

        current_pivot_l = i - 1
        current_pivot_r = i

        mirror_found = True
        for j in range(0, i):

            next_pivot_l = current_pivot_l - j
            next_pivot_r = current_pivot_r + j

            if next_pivot_l < 0 or next_pivot_r >= len(current_map):
                break

            diff = sum(1 for a, b in zip(current_map[next_pivot_l], current_map[next_pivot_r]) if a != b)
            if diff > 1:
                mirror_found = False
                break

            if diff == 1 and (fails_on != -1 and fails_on != next_pivot_r):
                mirror_found = False
                break
            if diff == 1 and fails_on == -1:
                fails_on = next_pivot_r

        if mirror_found and fails_on != -1:
            return i

    return 0



def test_day_13():
    assert day_13("test.txt") == (405, 400)

test_day_13()
p1, p2 = day_13("input.txt")
print("Part 1: ", p1)
print("Part 2: ", p2)
