"""
Day 1 of Advent of Code
"""
import numpy as np

from ..solution import Solution


class Day01(Solution, day=1):
    """
    Solution to day 1
    """

    def parse(self):
        """Parse the input file"""
        with open(self.input_file, mode="rt", encoding="utf8") as infile:
            return np.array(list(map(int, infile.read().strip().split())))

    def part1(self) -> int:
        """How many times do consecutive numbers increase?"""
        return (self.data[1:] > self.data[:-1]).sum()

    def part2(self) -> int:
        """How many times do rolling sums of 3 increase?"""
        return (self.data[3:] > self.data[:-3]).sum()
