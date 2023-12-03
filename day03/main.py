import pytest

def day_3(filename):
    matrix = [l.strip() for l in open(filename)]

    square = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1)
    ]

    total_p1 = 0

    for y in range(len(matrix)):
        current_number = ""
        current_number_is_valid = False
        for x in range(len(matrix[y])):
            if matrix[y][x].isdigit():
                current_number += matrix[y][x]
                for dx, dy in square:
                    if 0 <= x + dx < len(matrix[y]) and 0 <= y + dy < len(matrix):
                        if not matrix[y + dy][x + dx].isdigit() and matrix[y + dy][x + dx] != ".":
                            current_number_is_valid = True
            else:
                if current_number_is_valid and len(current_number) > 0:
                    total_p1 += int(current_number)
                current_number = ""
                current_number_is_valid = False
        if current_number_is_valid and len(current_number) > 0:
            total_p1 += int(current_number)
        current_number = ""
        current_number_is_valid = False

    total_p2 = 1
    asterix_values = {}

    for y in range(len(matrix)):
        current_number = ""
        current_number_is_valid = False
        current_asterix = []
        for x in range(len(matrix[y])):
            if matrix[y][x].isdigit():
                current_number += matrix[y][x]
                for dx, dy in square:
                    if 0 <= x + dx < len(matrix[y]) and 0 <= y + dy < len(matrix) and  matrix[y + dy][x + dx] == "*":
                        asterix_x = x + dx
                        asterix_y = y + dy
                        if not (asterix_x, asterix_y) in current_asterix:
                            current_asterix.append((asterix_x, asterix_y))

            else:
                if current_number != "":
                    for asterix in current_asterix:
                        if not asterix in asterix_values:
                            asterix_values[asterix] = []
                        asterix_values[asterix].append(int(current_number))
                    current_number = ""
                    current_asterix = []
        if current_number != "":
            for asterix in current_asterix:
                if not asterix in asterix_values:
                    asterix_values[asterix] = []
                asterix_values[asterix].append(int(current_number))
        current_number = ""
        current_asterix = []

    total_p2 = 0

    for asterix, values in asterix_values.items():
        if len(values) == 2:
            total_p2 += values[0] * values[1]


    return total_p1, total_p2


def test_day_3():
     assert day_3("test.txt") == (4361, 467835)


test_day_3()
p1, p2 = day_3("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
