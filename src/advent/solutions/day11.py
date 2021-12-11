import itertools as its
from collections import deque

import numpy as np

from ..solution import Solution
from ..utils import saround


class Day11(Solution, day=11):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return np.array(
                [
                    [int(char) for char in sline]
                    for line in infile
                    if (sline := line.strip())
                ],
                dtype=int,
            )

    def part1(self):
        data = self.data.copy()
        num_flashes = 0
        for _ in range(100):
            data += 1
            xs, ys = np.where(data == 10)
            queue = deque(zip(xs, ys))
            num_flashes += len(queue)
            while queue:
                x, y = queue.popleft()
                for cx, cy in saround(x, y, data.shape):
                    data[cx, cy] += 1
                    if data[cx, cy] == 10:
                        num_flashes += 1
                        queue.append((cx, cy))
            data *= (data < 10).astype(int)
        return num_flashes

    def part2(self):
        data = self.data.copy()
        for num_round in its.count():
            data += 1
            xs, ys = np.where(data == 10)
            queue = deque(zip(xs, ys))
            while queue:
                x, y = queue.popleft()
                for cx, cy in saround(x, y, data.shape):
                    data[cx, cy] += 1
                    if data[cx, cy] == 10:
                        queue.append((cx, cy))
            data *= (data < 10).astype(int)
            if (data == 0).all():
                return num_round + 1
