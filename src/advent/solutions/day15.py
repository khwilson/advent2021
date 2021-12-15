import networkx as nx
import numpy as np

from ..solution import Solution
from ..utils import around


def min_cost(board):
    """
    Implement the answer using networkx library. The previous implementation utilized
    the non-priority queue version of Djikstra, which is V^2 in size, which is rather
    large. networkx does the priority-queue version which is E + V log V, which is
    _much_ smaller.
    """
    g = nx.DiGraph()
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            g.add_node((x, y))

    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            for xx, yy in around(x, y, board.shape):
                g.add_edge((x, y), (xx, yy), cost=board[xx, yy])

    path = nx.shortest_path(
        g, source=(0, 0), target=(board.shape[0] - 1, board.shape[1] - 1), weight="cost"
    )
    return sum(board[x, y] for x, y in path) - board[0, 0]


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
