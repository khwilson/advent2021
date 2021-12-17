import itertools as its
import re
from collections import defaultdict

from ..solution import Solution


def run_sims(x1, x2, y1, y2):
    # Making assumption y1 and y2 are both negative
    max_vy = abs(y1) + 1
    t_to_vy_in_range = defaultdict(list)
    for vy in range(-max_vy, max_vy + 1):
        cur_vy = vy
        t = 0
        y = 0
        while y >= y1:
            if y <= y2:
                t_to_vy_in_range[t].append(vy)
            t += 1  # Has to be integer so t must be even
            y += cur_vy
            cur_vy -= 1

    # Making assumption x1 and x2 are both positive
    max_t = max(t_to_vy_in_range)
    max_vx = x2 + 1
    t_to_vx_in_range = defaultdict(list)
    vx = 1
    for vx in range(max_vx + 1):
        cur_vx = vx
        t = 0
        x = 0
        while t <= max_t:
            if x1 <= x <= x2:
                t_to_vx_in_range[t].append(vx)
            t += 1
            x += cur_vx
            cur_vx = max(cur_vx - 1, 0)

    return t_to_vx_in_range, t_to_vy_in_range


class Day17(Solution, day=17):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return tuple(map(int, re.findall(r"(-?\d+)", infile.read())))

    def part1(self):
        x1, x2, y1, y2 = self.data
        t_to_vx_in_range, t_to_vy_in_range = run_sims(x1, x2, y1, y2)
        shared_ts = set(t_to_vy_in_range) & set(t_to_vx_in_range)
        correct_vy = max(max(t_to_vy_in_range[t]) for t in shared_ts)
        return (correct_vy * (correct_vy + 1)) // 2

    def part2(self):
        x1, x2, y1, y2 = self.data
        t_to_vx_in_range, t_to_vy_in_range = run_sims(x1, x2, y1, y2)
        shared_ts = set(t_to_vy_in_range) & set(t_to_vx_in_range)

        return len(
            {
                (vx, vy)
                for t in shared_ts
                for vx, vy in its.product(t_to_vx_in_range[t], t_to_vy_in_range[t])
            }
        )
