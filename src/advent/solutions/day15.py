import heapq

import numpy as np

from ..solution import Solution
from ..utils import around


def min_cost(board):
    """
    Implement the answer using an actual priority queue with the built in heap
    implementation
    """
    last_x = board.shape[0] - 1
    last_y = board.shape[1] - 1

    heap = [(board[last_x, last_y], last_x, last_y)]

    # This allows us to drop paths that would be longer than ones we've already explored
    min_cost = np.ones_like(board, dtype=np.float64) * float("inf")

    # Keep track of minimum length explored path here
    heapq.heapify(heap)
    while heap:
        this_cost, this_x, this_y = heapq.heappop(heap)
        for next_x, next_y in around(this_x, this_y, board.shape):
            next_cost = this_cost + board[next_x, next_y]

            # We've found the end of the path! This is necessarily the shortest path
            # as all other prospective paths are longer!
            if (next_x, next_y) == (0, 0):
                return next_cost - board[0, 0]

            # If we've already found a shorter path, don't explore this one
            if next_cost < min_cost[next_x, next_y]:
                heapq.heappush(heap, (next_cost, next_x, next_y))
                min_cost[next_x, next_y] = next_cost


class Day15(Solution, day=15):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return np.array(
                [[int(c) for c in sline] for line in infile if (sline := line.strip())]
            )

    def part1(self):
        return min_cost(self.data)

    def part2(self):
        data = np.hstack(
            [self.data, self.data + 1, self.data + 2, self.data + 3, self.data + 4]
        )
        data = np.vstack([data, data + 1, data + 2, data + 3, data + 4])

        highs = data // 10
        data = data * (1 - highs) + highs * (((data - 1) % 9) + 1)
        return min_cost(data)
