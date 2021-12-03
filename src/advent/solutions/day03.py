from collections import Counter, defaultdict

import numpy as np
import pandas as pd

from ..solution import Solution


class Day03(Solution, day=3):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return np.array([[int(x) for x in line.strip()] for line in infile if line.strip()])

    def part1(self):
        totals = self.data.sum(axis=0)
        γ = totals > (self.data.shape[0] / 2)
        ε = ~γ
        γ = int("".join(map(str, γ.astype(int))), 2)
        ε = int("".join(map(str, ε.astype(int))), 2)
        return γ * ε


    def part2(self):
        data = self.data.copy()
        for col in range(self.data.shape[1]):
            msb = 1 if data[:, col].sum() >= (data.shape[0] / 2) else 0
            data = data[data[:, col] == msb, :]
            if data.shape[0] == 1:
                break

        assert data.shape[0] == 1
        oxy = int("".join(map(str, data.flatten().astype(int))), 2)

        data = self.data.copy()
        for col in range(self.data.shape[1]):
            msb = 1 if data[:, col].sum() >= (data.shape[0] / 2) else 0
            lsb = 1 - msb
            data = data[data[:, col] == lsb, :]
            if data.shape[0] == 1:
                break

        assert data.shape[0] == 1
        co2 = int("".join(map(str, data.flatten().astype(int))), 2)

        return oxy * co2