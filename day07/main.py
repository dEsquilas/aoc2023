import copy
from functools import cmp_to_key

def day_7(filename):

    lines = [line.strip() for line in open(filename, "r")]
    initial_hands = [[x.split(" ")[0], int(x.split(" ")[1])] for x in lines]
    hands_p1 = copy.deepcopy(initial_hands)
    hands_p2 = copy.deepcopy(initial_hands)

    # Part 1

    for hand in hands_p1:
        hand.append(check_type(hand[0]))
    hands_p1 = sorted(hands_p1, key=cmp_to_key(cmp))
    p1 = 0
    for i in range(len(hands_p1)):
        p1 += hands_p1[i][1] * (i + 1)

    # Part 2

    for hand in hands_p2:
        hand.append(check_type2(hand[0]))
    hands_p2 = sorted(hands_p2, key=cmp_to_key(cmp2))

    p2 = 0
    for i in range(len(hands_p2)):
        p2 += hands_p2[i][1] * (i + 1)

    return p1, p2

def cmp(a, b):
    if a[2] > b[2]:
        return 1
    elif a[2] < b[2]:
        return -1

    for i in range(len(a[0])):
        if a[0][i] == b[0][i]:
            continue
        else:
            for j in ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]:
                if a[0][i] == j:
                    return 1
                if b[0][i] == j:
                    return -1
    return 0

def cmp2(a, b):
    if a[2] > b[2]:
        return 1
    elif a[2] < b[2]:
        return -1

    for i in range(len(a[0])):
        if a[0][i] == b[0][i]:
            continue
        else:
            for j in ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]:
                if a[0][i] == j:
                    return 1
                if b[0][i] == j:
                    return -1
    return 0



def count_ocurrences(hand):
    co = {}
    for i in range(len(hand)):
        co[hand[i]] = (hand.count(hand[i]))
    return co
def check_type(hand):
    pairs = 0

    count_ocurrence = count_ocurrences(hand)

    if len(count_ocurrence) == 1:
        return 6
    elif len(count_ocurrence) == 2:
        for k, item in count_ocurrence.items():
            if item == 4:
                return 5
        else:
            return 4
    elif len(count_ocurrence) == 3:
        for k,item in count_ocurrence.items():
            if item == 3:
                return 3
        else:
            return 2
    elif len(count_ocurrence) == 4:
        return 1
    elif len(count_ocurrence) == 5:
        return 0

    exit()

def check_type2(hand):
    if "J" not in hand:
        return check_type(hand)


    j_count = hand.count("J")
    new_hand = hand.replace("J", "")

    if j_count == 4 or j_count == 5: # 0 cards left
        return 6

    new_type = check_type(new_hand)
    new_ocurrences = count_ocurrences(new_hand)

    if j_count == 3: # 2 cards left
        if len(new_ocurrences) == 1:
            return 6
        elif len(new_ocurrences) == 2:
            return 5
    if j_count == 2: # 3 cards left
        if len(new_ocurrences) == 1:
            return 6
        elif len(new_ocurrences) == 2:
            return 5
        elif len(new_ocurrences) == 3:
            return 3
    if j_count == 1: # 4 cards left
        if len(new_ocurrences) == 1:
            return 6
        elif len(new_ocurrences) == 2:
            for k, item in new_ocurrences.items():
                if item == 3:
                    return 5
            return 4
        elif len(new_ocurrences) == 3:
            return 3
        elif len(new_ocurrences) == 4:
            return 1



def test_day_7():
     assert day_7("test.txt") == (6440, 5905)

test_day_7()
p1, p2 = day_7("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)