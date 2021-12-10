from collections import Counter, defaultdict
from typing import Optional

import numpy as np
import pandas as pd

from ..solution import Solution

PAIR = {
    "(": ")",
    "{": "}",
    "[": "]",
    "<": ">",
}

for key, val in list(PAIR.items()):
    PAIR[val] = key

POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

OPOINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def find_illegal_char(line: str) -> Optional[str]:
    chars = []
    for char in line:
        match char:
            case "(" | "[" | "<" | "{":
                chars.append(char)
            case ")" | "]" | ">" | "}":
                if not chars:
                    return char, None
                elif chars[-1] == PAIR[char]:
                    chars.pop()
                else:
                    return char, None
    return None, chars


class Day10(Solution, day=10):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return [sline for line in infile if (sline := line.strip())]

    def part1(self):
        total = 0
        for line in self.data:
            char, _ = find_illegal_char(line)
            if char:
                total += POINTS[char]
        return total

    def part2(self):
        totals = []
        for line in self.data:
            _, chars = find_illegal_char(line)
            if chars:
                this_total = 0
                for char in reversed(chars):
                    this_total *= 5
                    this_total += OPOINTS[PAIR[char]]
                totals.append(this_total)
        totals.sort()
        return totals[len(totals) // 2]
