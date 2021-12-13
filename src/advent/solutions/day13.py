import copy
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

from ..solution import Solution


class Day13(Solution, day=13):
    def parse(self):
        grid = []
        folds = []
        parsing_grid = True
        with open(self.input_file, "rt") as infile:
            for line in infile:
                line = line.strip()
                if not line:
                    parsing_grid = False
                    continue
                if parsing_grid:
                    left, right = map(int, line.split(","))
                    grid.append((left, right))
                else:
                    _, _, instruction = line.split(" ")
                    axis, val = instruction.split("=")
                    val = int(val)
                    folds.append((axis, val))

        return {
            "grid": set(grid),
            "folds": folds,
        }

    def part1(self):
        # So the prompt gives an example where all the folds are exactly _halfway_
        # across the paper, so a 2d gride fold is very easy. However, in the actual
        # input, the paper has an even, not an odd, width, and so the fold number
        # cannot be the median. As such, we just do a literal reflection
        grid = copy.copy(self.data["grid"])
        folds = self.data["folds"]
        axis, val = folds[0]
        new_grid = set()

        if axis == "x":
            for x, y in grid:
                if x > val:
                    # 656 over 655 -> 654 = 655 - (656 - 655)
                    new_grid.add((val - (x - val), y))
                elif x == val:
                    # These seem to just get dropped in the examples
                    pass
                else:
                    # These stay put
                    new_grid.add((x, y))
        else:
            for x, y in grid:
                if y > val:
                    # 656 over 655 -> 654 = 655 - (656 - 655)
                    new_grid.add((x, val - (y - val)))
                elif x == val:
                    # These seem to just get dropped in the examples
                    pass
                else:
                    # These stay put
                    new_grid.add((x, y))
        grid = new_grid
        return len(grid)

    def part2(self):
        grid = copy.copy(self.data["grid"])
        folds = self.data["folds"]
        for axis, val in folds:
            new_grid = set()

            if axis == "x":
                for x, y in grid:
                    if x > val:
                        # 656 over 655 -> 654 = 655 - (656 - 655)
                        new_grid.add((val - (x - val), y))
                    elif x == val:
                        # These seem to just get dropped in the examples
                        pass
                    else:
                        # These stay put
                        new_grid.add((x, y))
            else:
                for x, y in grid:
                    if y > val:
                        # 656 over 655 -> 654 = 655 - (656 - 655)
                        new_grid.add((x, val - (y - val)))
                    elif y == val:
                        # These seem to just get dropped in the examples
                        pass
                    else:
                        # These stay put
                        new_grid.add((x, y))
            grid = new_grid

        max_x = max(x for x, _ in grid)
        max_y = max(y for _, y in grid)
        np_grid = np.zeros((max_x + 1, max_y + 1), dtype=bool)
        for x, y in grid:
            np_grid[x, y] = True

        return "\n" + "\n".join(
            "".join("#" if val else " " for val in row) for row in np_grid.T
        )
