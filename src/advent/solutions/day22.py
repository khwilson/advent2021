import itertools as its
import re
from collections import defaultdict
from typing import List, Tuple

from shapely.geometry import box

from ..solution import Solution


def compute_area(shapes: List[Tuple[str, int, int, int, int, int, int]]) -> int:
    if not shapes:
        return 0

    first_on = 0
    while first_on < len(shapes) and shapes[first_on][0] != "on":
        first_on += 1

    if first_on == len(shapes):
        return 0

    _, x1, x2, y1, y2, _, _ = shapes[first_on]

    poly = box(x1, y1, x2, y2)
    for instr, x1, x2, y1, y2, _, _ in shapes[first_on + 1 :]:
        new_poly = box(x1, y1, x2, y2)
        if instr == "on":
            poly |= new_poly
        else:
            poly -= new_poly

    return int(poly.area)


class Day22(Solution, day=22):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return [
                (sline.split()[0], *map(int, re.findall(r"(-?\d+)", sline)))
                for line in infile
                if (sline := line.strip())
            ]

    def part1(self):
        outcome = defaultdict(bool)
        for instr, x1, x2, y1, y2, z1, z2 in self.data:
            x1 = max(x1, -50)
            x2 = min(x2, 50)
            y1 = max(y1, -50)
            y2 = min(y2, 50)
            z1 = max(z1, -50)
            z2 = min(z2, 50)

            for x, y, z in its.product(
                range(x1, x2 + 1), range(y1, y2 + 1), range(z1, z2 + 1)
            ):
                outcome[(x, y, z)] = instr == "on"
        return sum(outcome.values())

    def part2(self):
        # First, fix the coordinates to represent not the box but the bounds
        data = [
            (line[0], line[1], line[2] + 1, line[3], line[4] + 1, line[5], line[6] + 1)
            for line in self.data
        ]

        sorted_zs = sorted({z for line in data for z in line[5:]})

        total_area = 0
        for low_z, high_z in its.pairwise(sorted_zs):
            # Filter the shapes for ones that have zs in this range
            these_shapes = []
            for shape in data:
                _, _, _, _, _, z1, z2 = shape
                if z2 <= low_z:
                    continue
                if z1 < high_z:  # And implicity z2 > low_z
                    these_shapes.append(shape)
            total_area += (high_z - low_z) * compute_area(these_shapes)

        return total_area
