from ..solution import Solution
from ..utils import EAST, NORTH, SOUTH, Coord


class Day02(Solution, day=2):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return infile.readlines()

    def part1(self):
        ship = Coord(0, 0)
        for line in self.data:
            match line.strip().split():
                case ["forward", dist]:
                    ship += EAST * int(dist)
                case ["up", dist]:
                    ship += NORTH * int(dist)
                case ["down", dist]:
                    ship += SOUTH * int(dist)
                case _:
                    raise ValueError(f"Bad line: {line}")

        # "depth" is interpreted by reversing the y-coordinates
        return -ship.x * ship.y

    def part2(self):
        ship = Coord(0, 0)
        aim = 0
        for line in self.data:
            match line.strip().split():
                case ["forward", dist]:
                    ship += EAST * int(dist)
                    ship += SOUTH * aim * int(dist)
                case ["up", dist]:
                    aim += int(dist)
                case ["down", dist]:
                    aim -= int(dist)
                case _:
                    raise ValueError(f"Bad line: {line}")

        # With this modification, we're actually getting signs correct
        return ship.x * ship.y
