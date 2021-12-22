import itertools as its
import re
from collections import Counter
from functools import lru_cache

from ..solution import Solution

die_rolls = Counter(
    die1 + die2 + die3
    for die1, die2, die3 in its.product(range(1, 4), range(1, 4), range(1, 4))
)


@lru_cache(maxsize=None)
def play_game_from(player1_pos, player1_score, player2_pos, player2_score, player_turn):
    total1, total2 = 0, 0
    for die_roll, count in die_rolls.items():
        if player_turn == 1:
            new_player1_pos = ((player1_pos + die_roll - 1) % 10) + 1
            new_player1_score = player1_score + new_player1_pos
            if new_player1_score >= 21:
                total1 += count
                continue

            left, right = play_game_from(
                new_player1_pos, new_player1_score, player2_pos, player2_score, 2
            )
            total1 += left * count
            total2 += right * count
        else:
            new_player2_pos = ((player2_pos + die_roll - 1) % 10) + 1
            new_player2_score = player2_score + new_player2_pos
            if new_player2_score >= 21:
                total2 += count
                continue

            left, right = play_game_from(
                player1_pos, player1_score, new_player2_pos, new_player2_score, 1
            )
            total1 += left * count
            total2 += right * count

    return total1, total2


class Day21(Solution, day=21):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return [int(x) for x in re.findall(r"(\d+)", infile.read())][1::2]

    def part1(self):
        player1_score = 0
        player2_score = 0
        player1_pos, player2_pos = self.data
        die = 1
        num_rolls = 0
        while True:
            inc = 0
            for _ in range(3):
                inc += die
                die += 1
                die = ((die - 1) % 100) + 1
                num_rolls += 1

            player1_pos = ((player1_pos + inc - 1) % 10) + 1
            player1_score += player1_pos

            if player1_score >= 1000:
                return player2_score * num_rolls

            inc = 0
            for _ in range(3):
                inc += die
                die += 1
                die = ((die - 1) % 100) + 1
                num_rolls += 1
            player2_pos = ((player2_pos + inc - 1) % 10) + 1
            player2_score += player2_pos

            if player2_score >= 1000:
                return player1_score * num_rolls

    def part2(self):
        return max(*play_game_from(self.data[0], 0, self.data[1], 0, 1))
