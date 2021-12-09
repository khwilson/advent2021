from collections import Counter, defaultdict, deque

import numpy as np
import pandas as pd

from ..solution import Solution
from ..utils import around


class Day09(Solution, day=9):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return np.array(
                [[int(c) for c in sline] for line in infile if (sline := line.strip())],
                dtype=int,
            )

    def part1(self):
        # Add a border of 10s
        data = np.ones((self.data.shape[0] + 2, self.data.shape[1] + 2), dtype=int) * 10
        data[1:-1, 1:-1] = self.data

        # Mask points to low points
        mask = (
            (self.data < data[2:, 1:-1])
            & (self.data < data[1:-1, 2:])
            & (self.data < data[:-2, 1:-1])
            & (self.data < data[1:-1, :-2])
        )

        return ((self.data + 1) * mask).sum()

    def part2(self):
        data = np.ones((self.data.shape[0] + 2, self.data.shape[1] + 2), dtype=int) * 10
        data[1:-1, 1:-1] = self.data

        # Mask points to low points
        mask = (
            (self.data < data[2:, 1:-1])
            & (self.data < data[1:-1, 2:])
            & (self.data < data[:-2, 1:-1])
            & (self.data < data[1:-1, :-2])
        )

        xs, ys = np.where(mask)

        bfs_land = np.zeros_like(self.data, dtype=int)
        queue = deque(
            [(x, y, basin_id) for basin_id, (x, y) in enumerate(zip(xs, ys), 1)]
        )
        seen = set()
        while queue:
            (x, y, basin_id) = queue.popleft()
            for new_x, new_y in around(x, y, self.data.shape):
                if (new_x, new_y) in seen or self.data[new_x, new_y] == 9:
                    continue
                bfs_land[new_x, new_y] = basin_id
                queue.append((new_x, new_y, basin_id))
                seen.add((new_x, new_y))

        counts = np.bincount(bfs_land.flatten())[1:]
        counts.sort()
        return np.prod(counts[-3:])
