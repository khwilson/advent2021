from collections import Counter, defaultdict, deque

import numpy as np
import pandas as pd

from ..solution import Solution
from ..utils import around

def min_cost(board):
    """
    Implement as dynamic programming: The minimum cost path from a point is its
    cost plus the minimum cost of a path from any neighbor.

    Problem is that the two-dimensional nature of the problem makes it difficult to
    think about the ordering. But if you grow from the bottom-right, it works out,
    as long as you break whenever the cost of the path seen is higher than the one
    already there
    """
    cost = np.ones_like(board, dtype=float) * float('inf')
    init_cost = board[board.shape[0] - 1, board.shape[1] - 1]
    cost[board.shape[0] - 1, board.shape[1] - 1] = init_cost
    queue = deque([(board.shape[0] - 1, board.shape[1] - 1, init_cost)])
    while queue:
        x, y, this_cost = queue.popleft()
        for next_x, next_y in around(x, y, board.shape):
            next_cost = this_cost + board[next_x, next_y]
            if next_cost < cost[next_x, next_y]:
                cost[next_x, next_y] = next_cost
                queue.append((next_x, next_y, next_cost))
    return int(cost[0, 0] - board[0, 0])


class Day15(Solution, day=15):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return np.array([[int(c) for c in sline] for line in infile if (sline := line.strip())])

    def part1(self):
        return min_cost(self.data)

    def part2(self):
        data = np.hstack([self.data, self.data + 1, self.data + 2, self.data + 3, self.data + 4])
        data = np.vstack([data, data + 1, data + 2, data + 3, data + 4])

        highs = data // 10
        data = data * (1 - highs) + highs * (((data - 1) % 9) + 1)
        return min_cost(data)
