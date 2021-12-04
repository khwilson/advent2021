from collections import Counter, defaultdict

import numpy as np
import pandas as pd

from ..solution import Solution


class Day04(Solution, day=4):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            called_values = [int(x) for x in next(infile).strip().split(",")]

            # Skip the empty line
            next(infile)

            boards = []
            for line in infile:
                line = line.strip()
                if line:
                    boards.append([int(x) for x in line.split()])

            assert len(boards) % 5 == 0
            return {"called_values": called_values, "boards": np.array(boards)}

    def part1(self):
        mask = np.zeros_like(self.data["boards"], dtype=bool)
        for val in self.data["called_values"]:
            mask |= self.data["boards"] == val

            winning_board = None

            # Check for winner in rows
            row_winners = np.where(mask.all(axis=1))[0]
            if len(row_winners) > 0:
                # Do whatever
                winning_board = row_winners[0] // 5

            # Check for winner in columns
            col_cumsums = np.vstack([np.zeros(5), mask.cumsum(axis=0)[4::5]])
            col_counts = col_cumsums[1:, :] - col_cumsums[:-1, :]
            col_winners = np.where(col_counts == 5)[0]
            if len(col_winners) > 0:
                winning_board = col_winners[0]

            if winning_board is None:
                continue

            board = self.data["boards"][winning_board * 5 : (winning_board + 1) * 5, :]
            board_mask = mask[winning_board * 5 : (winning_board + 1) * 5, :]
            unmarked_total = (board * ~board_mask).sum()
            return unmarked_total * val

    def part2(self):
        mask = np.zeros_like(self.data["boards"], dtype=bool)
        all_winning_boards = set()
        for val in self.data["called_values"]:
            mask |= self.data["boards"] == val

            winning_boards = []

            # Check for winner in rows
            row_winners = np.where(mask.all(axis=1))[0]
            if len(row_winners) > 0:
                # Do whatever
                winning_boards.extend(row_winners // 5)

            # Check for winner in columns
            col_cumsums = np.vstack([np.zeros(5), mask.cumsum(axis=0)[4::5]])
            col_counts = col_cumsums[1:, :] - col_cumsums[:-1, :]
            col_winners = np.where(col_counts == 5)[0]
            if len(col_winners) > 0:
                winning_boards.extend(col_winners)

            winning_boards = set(winning_boards)
            if (
                len(winning_boards | all_winning_boards)
                < self.data["boards"].shape[0] // 5
            ):
                # We're not at the last winning board, so just continue
                all_winning_boards |= winning_boards
                continue

            # import ipdb; ipdb.set_trace()
            this_round_winners = winning_boards - all_winning_boards
            winning_board = list(this_round_winners)[0]

            board = self.data["boards"][winning_board * 5 : (winning_board + 1) * 5, :]
            board_mask = mask[winning_board * 5 : (winning_board + 1) * 5, :]
            unmarked_total = (board * ~board_mask).sum()
            return unmarked_total * val
