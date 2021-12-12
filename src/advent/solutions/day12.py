import string
from collections import defaultdict
from typing import Dict, List

from ..solution import Solution


def count_paths(data: Dict[str, List[str]], path: List[str]) -> int:
    cur_end = path[-1]
    retval = 0
    for next_step in data[cur_end]:
        if next_step == "end":
            retval += 1
        elif ((next_step[0] in string.ascii_lowercase) and (next_step not in path)) or (
            next_step[0] in string.ascii_uppercase
        ):
            # Don't visit lower cases multiple times
            path.append(next_step)
            retval += count_paths(data, path)
            path.pop()
    return retval


def count_paths_part2(
    data: Dict[str, List[str]], path: List[str], already_done_double: bool
) -> int:
    cur_end = path[-1]
    retval = 0
    for next_step in data[cur_end]:
        if next_step == "start":
            # Not allowed
            continue
        elif next_step == "end":
            retval += 1
        elif next_step[0] in string.ascii_uppercase:
            path.append(next_step)
            retval += count_paths_part2(data, path, already_done_double)
            path.pop()
        else:
            # We have a lowercase cave
            if next_step not in path:
                # No further checks
                path.append(next_step)
                retval += count_paths_part2(data, path, already_done_double)
                path.pop()

            else:
                if not already_done_double:
                    path.append(next_step)
                    retval += count_paths_part2(data, path, True)
                    path.pop()
                else:
                    # Only allowed to visit _one_ lowercase cave twice!
                    pass
    return retval


class Day12(Solution, day=12):
    def parse(self):
        data = defaultdict(list)
        with open(self.input_file, "rt") as infile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                left, right = line.split("-")
                data[left].append(right)
                data[right].append(left)
        return data

    def part1(self):
        # Let's just DFS through caves
        path = ["start"]
        return count_paths(self.data, path)

    def part2(self):
        path = ["start"]
        return count_paths_part2(self.data, path, False)
