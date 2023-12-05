class Map:
    def __init__(self, map):
        self.map_type = map[0]
        self.map_ranges = []
        for i in range(1, len(map)):
            self.map_ranges.append(MapRange(map[i]))

    def translate(self, value):
        for map_range in self.map_ranges:
            if map_range.source_range_start <= value <= map_range.source_range_end:
                return map_range.translate(value)

        return value

    def sub_ranges(self, current_ranges):

        generated_ranges = []
        ranges_for_check = current_ranges

        while len(ranges_for_check) > 0:
            cr = ranges_for_check.pop(0)
            range_found = False
            for map_range in self.map_ranges:
                if map_range.source_range_start <= cr[0] <= map_range.source_range_end and map_range.source_range_start <= cr[1] <= map_range.source_range_end:
                    generated_ranges.append((map_range.translate(cr[0]), map_range.translate(cr[1])))
                    range_found = True
                elif map_range.source_range_start <= cr[0] <= map_range.source_range_end and map_range.source_range_start < cr[1]:
                    generated_ranges.append((map_range.translate(cr[0]), map_range.translate(map_range.source_range_end)))
                    ranges_for_check.append((map_range.source_range_end + 1, cr[1]))
                    range_found = True
                elif cr[0] < map_range.source_range_start and map_range.source_range_start <= cr[1] <= map_range.source_range_end:
                    generated_ranges.append((map_range.translate(map_range.source_range_start), map_range.translate(cr[1])))
                    ranges_for_check.append((cr[0], map_range.source_range_start - 1))
                    range_found = True
            if not range_found:
                generated_ranges.append(cr)

        return generated_ranges

class MapRange:
    def __init__(self, line):
        aux = line.split(" ")
        self.destination_range_start = int(aux[0])
        self.source_range_start = int(aux[1])
        self.range_length = int(aux[2])
        self.source_range_end = self.source_range_start + self.range_length - 1


    def translate(self, value):
        return self.destination_range_start + (value - self.source_range_start)

def day_5(filename):

    file = [l.strip() for l in open(filename)]

    seeds = [int(x) for x in file[0].split(": ")[1].split(" ")]

    maps = []
    newMap = []

    for line in file[2:]:
        if line == "":
            maps.append(Map(newMap))
            newMap = []
        else:
            newMap.append(line)

    maps.append(Map(newMap))

    # part 1

    location = 0
    lowest_location_p1 = 999999999999999
    for seed in seeds:
        location = lowest_location_find(seed, maps)
        lowest_location_p1 = min(location, lowest_location_p1)

    seeds_pairs = []
    for i in range(len(seeds) // 2):
        seeds_pairs.append((seeds[i * 2], seeds[i * 2 + 1]))

    # part 2

    lowest_location_p2 = 999999999999999

    ranges = []
    all_ranges = []

    for (seed_init, seed_range) in seeds_pairs:
        ranges = [(seed_init, seed_init + seed_range - 1)]
        for map in maps:
            ranges = map.sub_ranges(ranges)
        all_ranges.extend(ranges)


    for (start, end) in all_ranges:
        lowest_location_p2 = min(lowest_location_p2, start)

    return lowest_location_p1, lowest_location_p2

def lowest_location_find(current_seed, maps):

    location = current_seed
    for map in maps:
        location = map.translate(location)

    return location

def test_day_5():
     assert day_5("test.txt") == (35, 46)

test_day_5()

p1, p2 = day_5("input.txt")

print("Part 1: ", p1)
print("Part 2: ", p2)