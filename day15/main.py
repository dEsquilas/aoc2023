def day_15(filename):

    with (open(filename)) as file:
         orders = [x for x in file.read().split(",")]

    p1 = 0
    p2 = 0

    boxes = {x:[] for x in range(255)}
    boxes_count = {x:[] for x in range(255)}

    for order in orders:
        p1 += get_label(order)

    for order in orders:
        if "=" in order:
            aux = order.split("=")
            name = aux[0]
            label = get_label(name)
            distance = int(aux[1])

            if name not in boxes[label]:
                boxes[label].append(name)
                boxes_count[label].append((name, distance))
            else:
                for i in range(len(boxes_count[label])):
                    box = boxes_count[label][i]
                    if box[0] == name:
                        boxes_count[label][i] = (name, distance)
                        break
        if "-" in order:
            name = order.split("-")[0]
            label = get_label(name)
            if name in boxes[label]:
                pos = boxes[label].index(name)
                del boxes[label][pos]
                del boxes_count[label][pos]

    for (box_id, box) in boxes_count.items():
        for lens_id in range(len(box)):
            t = (box_id + 1) * (lens_id + 1) * box[lens_id][1]
            p2 += t

    return p1,p2

def get_label(order):
    t = 0
    for i in range(len(order)):
        t += ord(order[i])
        t *= 17
        t %= 256

    return t

def test_day_15():
    assert day_15("test.txt") == (1320, 145)

test_day_15()
p1, p2 = day_15("input.txt")
print("Part 1: ", p1)
print("Part 2: ", p2)
