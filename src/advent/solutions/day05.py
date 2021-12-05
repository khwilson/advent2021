import re
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

from ..solution import Solution

PARSER = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


class Day05(Solution, day=5):
    def parse(self):
        horiz_lines = []
        vert_lines = []
        diag_lines = []
        with open(self.input_file, "rt") as infile:
            for line in infile:
                if line := line.strip():
                    left_x, left_y, right_x, right_y = map(int, PARSER.findall(line)[0])
                    if left_x == right_x:
                        horiz_lines.append([left_x, left_y, right_x, right_y])
                    elif left_y == right_y:
                        vert_lines.append([left_x, left_y, right_x, right_y])
                    else:
                        assert abs(left_x - right_x) == abs(left_y - right_y)
                        diag_lines.append([left_x, left_y, right_x, right_y])

        horiz_lines = np.array(horiz_lines)
        vert_lines = np.array(vert_lines)
        diag_lines = np.array(diag_lines)

        max_x = max(
            data[:, i].max()
            for data in (horiz_lines, vert_lines, diag_lines)
            for i in [0, 2]
        )
        max_y = max(
            data[:, i].max()
            for data in (horiz_lines, vert_lines, diag_lines)
            for i in [1, 3]
        )

        return {
            "horiz_lines": horiz_lines,
            "vert_lines": vert_lines,
            "diag_lines": diag_lines,
            "max_x": max_x,
            "max_y": max_y,
        }

    def part1(self):
        mask = np.zeros(
            (self.data["max_x"] + 1, self.data["max_y"] + 1), dtype=np.int64
        )

        for row in self.data["horiz_lines"]:
            mask[row[0], np.arange(min(row[1], row[3]), max(row[1], row[3]) + 1)] += 1

        for row in self.data["vert_lines"]:
            mask[np.arange(min(row[0], row[2]), max(row[0], row[2]) + 1), row[1]] += 1

        return (mask > 1).sum()

    def part2(self):
        mask = np.zeros(
            (self.data["max_x"] + 1, self.data["max_y"] + 1), dtype=np.int64
        )

        for row in self.data["horiz_lines"]:
            mask[row[0], np.arange(min(row[1], row[3]), max(row[1], row[3]) + 1)] += 1

        for row in self.data["vert_lines"]:
            mask[np.arange(min(row[0], row[2]), max(row[0], row[2]) + 1), row[1]] += 1

        for row in self.data["diag_lines"]:
            x_order = 1 if row[0] < row[2] else -1
            y_order = 1 if row[1] < row[3] else -1

            mask[
                np.arange(row[0], row[2] + x_order, x_order),
                np.arange(row[1], row[3] + y_order, y_order),
            ] += 1

        return (mask > 1).sum()
