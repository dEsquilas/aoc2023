import pytest

def day_3(filename):

    matrix = [l.strip() for l in open(filename)]
    square = [(-1, -1),(0, -1),(1, -1),(-1, 0),(1, 0),(-1, 1),(0, 1),(1, 1)]

    total_p1 = 0
    total_p2 = 0
    gear_values = {}

    for y in range(len(matrix)):
        current_number = ""
        current_number_is_valid = False
        current_gear = []
        for x in range(len(matrix[y])):
            if matrix[y][x].isdigit():
                current_number += matrix[y][x]
                for dx, dy in square:
                    if 0 <= x + dx < len(matrix[y]) and 0 <= y + dy < len(matrix):
                        if not matrix[y + dy][x + dx].isdigit() and matrix[y + dy][x + dx] != ".":
                            current_number_is_valid = True
                    if 0 <= x + dx < len(matrix[y]) and 0 <= y + dy < len(matrix) and  matrix[y + dy][x + dx] == "*":
                        if not (y + dy, x + dx) in current_gear:
                            current_gear.append((y + dy, x + dx))
            else:
                if current_number_is_valid and len(current_number) > 0:
                    total_p1 += int(current_number)
                if current_number != "":
                    for gear in current_gear:
                        if not gear in gear_values:
                            gear_values[gear] = []
                        gear_values[gear].append(int(current_number))

                current_gear = []
                current_number = ""
                current_number_is_valid = False

        if current_number_is_valid and len(current_number) > 0:
            total_p1 += int(current_number)
        if current_number != "":
            for gear in current_gear:
                if not gear in gear_values:
                    gear_values[gear] = []
                gear_values[gear].append(int(current_number))
        current_gear = []
        current_number = ""
        current_number_is_valid = False

    for gear, values in gear_values.items():
        if len(values) == 2:
            total_p2 += values[0] * values[1]


    return total_p1, total_p2


def test_day_3():
     assert day_3("test.txt") == (4361, 467835)


test_day_3()
p1, p2 = day_3("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
