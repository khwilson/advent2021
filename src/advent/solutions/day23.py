import math
from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple

from ..solution import Solution

Hole = Tuple[int, int] | Tuple[int, int, int, int]


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
    ),
)

DONE_STATE_PART2 = BoardState(
    left=0,
    right=0,
    hall=(0, 0, 0, 0, 0),
    holes=(
        (1, 1, 1, 1),
        (10, 10, 10, 10),
        (100, 100, 100, 100),
        (1000, 1000, 1000, 1000),
    ),
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
    if len(hole) == 2:
        if hole[1] == 0:
            dist = 1
            new_hole = (0, ball)
        else:
            dist = 0
            new_hole = (ball, ball)
    else:
        if hole[3] == 0:
            dist = 3
            new_hole = (0, 0, 0, ball)
        elif hole[2] == 0:
            dist = 2
            new_hole = (0, 0, ball, ball)
        elif hole[1] == 0:
            dist = 1
            new_hole = (0, ball, ball, ball)
        else:
            dist = 0
            new_hole = (ball, ball, ball, ball)

    new_holes = tuple(
        h if j != hole_num else new_hole for j, h in enumerate(state.holes)
    )
    return new_holes, dist, hole_num


@lru_cache(maxsize=None)
def play_game_from(state: BoardState):
    if state == DONE_STATE or state == DONE_STATE_PART2:
        return 0

    cost = float("inf")

    # Try to move from holes to hallway
    for i, hole in enumerate(state.holes):
        if all(bb == 0 for bb in hole):
            # No balls to move. Skip
            continue

        if all(bb == 10 ** i for bb in hole):
            # We're already golden. Nothing to do.
            continue

        for j, ball in enumerate(hole):
            if ball > 0 and any(bb != 10 ** i for bb in hole[j:]):
                dist = j
                new_hole = tuple([0] * j + [0] + list(hole[j + 1 :]))
                break
        else:
            continue

        new_holes = tuple(h if j != i else new_hole for j, h in enumerate(state.holes))
        new_dist = dist
        for j in range(i, -1, -1):
            new_dist += 2
            if state.hall[j] == 0:
                new_hall = tuple(
                    b if jj != j else ball for jj, b in enumerate(state.hall)
                )
                new_state = BoardState(
                    left=state.left, right=state.right, hall=new_hall, holes=new_holes
                )
                cost = min(cost, new_dist * ball + play_game_from(new_state))
            else:
                break
        else:
            # Run only if we got to the end of the hallway
            new_dist += 1
            if state.left == 0:
                new_state = BoardState(
                    left=ball, right=state.right, hall=state.hall, holes=new_holes
                )
                cost = min(cost, new_dist * ball + play_game_from(new_state))

        new_dist = dist
        for j in range(i + 1, len(state.hall)):
            new_dist += 2
            if state.hall[j] == 0:
                new_hall = tuple(
                    b if jj != j else ball for jj, b in enumerate(state.hall)
                )
                new_state = BoardState(
                    left=state.left, right=state.right, hall=new_hall, holes=new_holes
                )
                cost = min(cost, new_dist * ball + play_game_from(new_state))
            else:
                break
        else:
            # Run only if we got to the end of the hallway
            new_dist += 1
            if state.right == 0:
                new_state = BoardState(
                    left=state.left, right=ball, hall=state.hall, holes=new_holes
                )
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
            if all(bb == 0 for bb in state.hall[i + 1 : hole_num + 1]):
                # We can deposit the ball
                new_dist = dist + 2 * (hole_num - i) + 2
                new_state = BoardState(
                    left=state.left, right=state.right, hall=new_hall, holes=new_holes
                )
                cost = min(cost, new_dist * b + play_game_from(new_state))
        else:
            # We're approaching from the right
            if all(bb == 0 for bb in state.hall[hole_num + 1 : i]):
                # We can deposit the ball
                new_dist = dist + 2 * (i - hole_num - 1) + 2
                new_state = BoardState(
                    left=state.left, right=state.right, hall=new_hall, holes=new_holes
                )
                cost = min(cost, new_dist * b + play_game_from(new_state))

    # Now try to move the ball from the left-most spot
    if state.left != 0:
        new_holes, dist, hole_num = create_new_hole(state, state.left)
        if new_holes and all(bb == 0 for bb in state.hall[: hole_num + 1]):
            # We can deposit it
            new_state = BoardState(
                left=0, right=state.right, hall=state.hall, holes=new_holes
            )
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
        if new_holes and all(bb == 0 for bb in state.hall[hole_num + 1 :]):
            # We can deposit it
            new_state = BoardState(
                left=state.left, right=0, hall=state.hall, holes=new_holes
            )
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
                hall=(
                    parse_elt(data[1][2]),
                    parse_elt(data[1][4]),
                    parse_elt(data[1][6]),
                    parse_elt(data[1][8]),
                    parse_elt(data[1][10]),
                ),
                right=parse_elt(data[1][11]),
                holes=(
                    (parse_elt(data[2][3]), parse_elt(data[3][3])),
                    (parse_elt(data[2][5]), parse_elt(data[3][5])),
                    (parse_elt(data[2][7]), parse_elt(data[3][7])),
                    (parse_elt(data[2][9]), parse_elt(data[3][9])),
                ),
            )

    def part1(self):
        return play_game_from(self.data)

    def part2(self):
        data = BoardState(
            left=self.data.left,
            right=self.data.right,
            hall=self.data.hall,
            holes=(
                (self.data.holes[0][0], 1000, 1000, self.data.holes[0][1]),
                (self.data.holes[1][0], 100, 10, self.data.holes[1][1]),
                (self.data.holes[2][0], 10, 1, self.data.holes[2][1]),
                (self.data.holes[3][0], 1, 100, self.data.holes[3][1]),
            ),
        )
        return play_game_from(data)
