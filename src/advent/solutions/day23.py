from collections import Counter, defaultdict
from dataclasses import dataclass
import math
from functools import lru_cache
from typing import Tuple

import numpy as np
import pandas as pd

from ..solution import Solution

Hole = Tuple[int, int]

@dataclass(frozen=True, eq=True)
class BoardState:
    left: int
    right: int
    hall: Tuple[int, int, int, int, int]
    holes: Tuple[Hole, Hole, Hole, Hole]


DONE_STATE = BoardState(
    left=0,
    right=0,
    hall=(0, 0, 0, 0, 0),
    holes=(
        (1, 1),
        (10, 10),
        (100, 100),
        (1000, 1000),
    )
)

def parse_elt(elt):
    match elt:
        case ".":
            return 0
        case "A":
            return 1
        case "B":
            return 10
        case "C":
            return 100
        case "D":
            return 1000
        case _:
            raise ValueError("Oops")

def create_new_hole(state: BoardState, ball: int):
    hole_num = int(math.log10(ball))
    hole = state.holes[hole_num]
    if not all(bb in [0, ball] for bb in hole):
        # Must empty the hole before we can put new things in it
        return None, None, None
    if hole[1] == 0:
        dist = 1
        new_hole = (0, ball)
    else:
        dist = 0
        new_hole = (ball, ball)

    new_holes = tuple(h if j != hole_num else new_hole for j, h in enumerate(state.holes))
    return new_holes, dist, hole_num

@lru_cache(maxsize=None)
def play_game_from(state: BoardState):
    if state == DONE_STATE:
        return 0

    cost = float('inf')

    # Try to move from holes to hallway
    for i, hole in enumerate(state.holes):
        if hole[0] == 0 and hole[1] == 0:
            # No balls to move. Skip
            continue

        if hole[0] == 10 ** i and hole[1] == 10 ** i:
            # We're already golden. Nothing to do.
            continue

        if hole[0] > 0:
            # No matter its value, this has to move because at least one of the elements
            # in the hole is not correct b/c prevous if statement
            dist = 0
            new_hole = (0, hole[1])
            ball = hole[0]
        elif hole[1] != 10 ** i:
            # In this case, we've got to get the bottom ball free
            dist = 1
            new_hole = (0, 0)
            ball = hole[1]
        else:
            # This is the case that the bottom guy in the hole is correct and so
            # it is only costly to move it
            continue

        new_holes = tuple(h if j != i else new_hole for j, h in enumerate(state.holes))
        new_dist = dist
        for j in range(i, -1, -1):
            new_dist += 2
            if state.hall[j] == 0:
                new_hall = tuple(b if jj != j else ball for jj, b in enumerate(state.hall))
                new_state = BoardState(left=state.left, right=state.right, hall=new_hall, holes=new_holes)
                cost = min(cost, new_dist * ball + play_game_from(new_state))
            else:
                break
        else:
            # Run only if we got to the end of the hallway
            new_dist += 1
            if state.left == 0:
                new_state = BoardState(left=ball, right=state.right, hall=state.hall, holes=new_holes)
                cost = min(cost, new_dist * ball + play_game_from(new_state))

        new_dist = dist
        for j in range(i + 1, len(state.hall)):
            new_dist += 2
            if state.hall[j] == 0:
                new_hall = tuple(b if jj != j else ball for jj, b in enumerate(state.hall))
                new_state = BoardState(left=state.left, right=state.right, hall=new_hall, holes=new_holes)
                cost = min(cost, new_dist * ball + play_game_from(new_state))
            else:
                break
        else:
            # Run only if we got to the end of the hallway
            new_dist += 1
            if state.right == 0:
                new_state = BoardState(left=state.left, right=ball, hall=state.hall, holes=new_holes)
                cost = min(cost, new_dist * ball + play_game_from(new_state))

    # Now we try to move balls from hallway to holes
    for i, b in enumerate(state.hall):
        if b == 0:
            # Nothing here to move
            continue

        new_hall = tuple(bb if j != i else 0 for j, bb in enumerate(state.hall))
        new_holes, dist, hole_num = create_new_hole(state, b)
        if not new_holes:
            continue

        if i <= hole_num:
            # We're approaching from the left
            if all(bb == 0 for bb in state.hall[i + 1: hole_num + 1]):
                # We can deposit the ball
                new_dist = dist + 2 * (hole_num - i) + 2
                new_state = BoardState(left=state.left, right=state.right, hall=new_hall, holes=new_holes)
                cost = min(cost, new_dist * b + play_game_from(new_state))
        else:
            # We're approaching from the right
            if all(bb == 0 for bb in state.hall[hole_num + 1:i]):
                # We can deposit the ball
                new_dist = dist + 2 * (i - hole_num - 1) + 2
                new_state = BoardState(left=state.left, right=state.right, hall=new_hall, holes=new_holes)
                cost = min(cost, new_dist * b + play_game_from(new_state))

    # Now try to move the ball from the left-most spot
    if state.left != 0:
        new_holes, dist, hole_num = create_new_hole(state, state.left)
        if new_holes and all(bb == 0 for bb in state.hall[:hole_num + 1]):
            # We can deposit it
            new_state = BoardState(left=0, right=state.right, hall=state.hall, holes=new_holes)
            new_dist = (
                1  # From left to hall[0]
                + 2 * hole_num  # Across the hall
                + 2  # Into the top slot of the hole
                + dist  # Into the bottom slot of the hole if necessary
            )
            cost = min(cost, new_dist * state.left + play_game_from(new_state))

    # Now try to move the ball from the right-most spot
    if state.right != 0:
        new_holes, dist, hole_num = create_new_hole(state, state.right)
        if new_holes and all(bb == 0 for bb in state.hall[hole_num + 1:]):
            # We can deposit it
            new_state = BoardState(left=state.left, right=0, hall=state.hall, holes=new_holes)
            new_dist = (
                1  # From right to hall[-1]
                + 2 * (len(state.hall) - hole_num - 2)  # Across the hall
                + 2  # Into the top slot of the hole
                + dist  # Into the bottom slot of the hole if necessary
            )
            cost = min(cost, new_dist * state.right + play_game_from(new_state))

    return cost


class Day23(Solution, day=23):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            data = infile.readlines()
            return BoardState(
                left=parse_elt(data[1][1]),
                hall=(parse_elt(data[1][2]),
                parse_elt(data[1][4]),
                parse_elt(data[1][6]),
                parse_elt(data[1][8]),
                parse_elt(data[1][10]),
                ),
                right=parse_elt(data[1][11]),
                holes=(
                    (parse_elt(data[2][3]), parse_elt(data[3][3])),
                    (parse_elt(data[2][5]), parse_elt(data[3][5])),
                 (parse_elt(data[2][7]),parse_elt(data[3][7])),
                (parse_elt(data[2][9]),parse_elt(data[3][9]))
            )
            )

    def part1(self):
        return play_game_from(self.data)

    def part2(self):
        pass
