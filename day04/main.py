import pytest

def day_4(filename):

    cards = [l.strip() for l in open(filename)]

    p1 = 0
    p2 = 0
    scratchcards = {i: 1 for i in range(1, len(cards) + 1)}
    additional_cards = []

    for card in cards:
        card_id = int(card.split(": ")[0].split(" ")[-1])
        card = card.split(": ")[1]

        winner_numbers = set(card.split(" | ")[0].split(" "))
        my_numbers = set(card.split(" | ")[1].split(" "))
        winner_numbers.discard("")
        my_numbers.discard("")
        ocurrences = len(my_numbers.intersection(winner_numbers))
        if ocurrences != 0:
            p1 += 2**(len(my_numbers.intersection(winner_numbers)) -1)
            for i in range(card_id + 1, card_id + 1 + ocurrences):
                scratchcards[i] += scratchcards[card_id]
    for count in scratchcards.values():
        p2 += count

    return p1, p2


def test_day_4():
     assert day_4("test.txt") == (13, 30)


test_day_4()
p1, p2 = day_4("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)