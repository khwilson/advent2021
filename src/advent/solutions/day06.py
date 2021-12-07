import copy

from ..solution import Solution


class Day06(Solution, day=6):
    def parse(self):
        data = [0] * 9
        with open(self.input_file, "rt") as infile:
            for fish in infile.read().split(","):
                data[int(fish)] += 1
        return data

    def part1(self):
        data = copy.copy(self.data)
        for _ in range(80):
            to_create = data[0]
            data[:-1] = data[1:]
            data[-1] = to_create
            data[6] += to_create
        return sum(data)

    def part2(self):
        data = copy.copy(self.data)
        for _ in range(256):
            to_create = data[0]
            data[:-1] = data[1:]
            data[-1] = to_create
            data[6] += to_create
        return sum(data)
