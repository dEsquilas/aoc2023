import pytest

def day_1_p1(filename):
    lines = [l.strip() for l in open(filename)]

    total = 0

    for line in lines:
        current_number = find_first_number(line) * 10 + find_first_number(line[::-1])
        total += current_number

    return total

def day_1_p2(filename):
    lines = [l.strip() for l in open(filename)]

    total = 0


    for line in lines:

        current_number_1 = find_number(line, 1)
        current_number_2 = find_number(line, -1)

        total += current_number_1 * 10 + current_number_2

    return total

def find_number(string, d):

    current_substr = ""
    current_number = -1

    numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

    if d == -1:
        string = string[::-1]

    for letter in string:
        if d == 1:
            current_substr += letter
        else:
            current_substr = letter + current_substr
        if letter.isdigit():
            current_number = int(letter)
            break
        else:
            for key, value in numbers.items():
                if key in current_substr:
                    current_number = value
                    break
        if current_number != -1:
            break

    return current_number

def find_first_number(string):
    for i in range(len(string)):
        if string[i].isdigit():
            return int(string[i])

def test_day_1_p1():
     assert day_1_p1("test.txt") == 142

def test_day_1_p2():
    assert day_1_p2("test2.txt") == 281


test_day_1_p1()
test_day_1_p2()

p1 = day_1_p1("input.txt")
p2 = day_1_p2("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)
