from __future__ import annotations

import itertools as its
from dataclasses import dataclass
from math import ceil, floor
from typing import Optional, Union

from ..solution import Solution


@dataclass
class Number:
    left: Union[Number, int]
    right: Union[Number, int]
    parent: Optional[Number]

    @classmethod
    def parse(cls, contents: Union[str, list]) -> Number:
        if isinstance(contents, str):
            contents = eval(contents)

        left = (
            contents[0] if isinstance(contents[0], int) else Number.parse(contents[0])
        )
        right = (
            contents[1] if isinstance(contents[1], int) else Number.parse(contents[1])
        )
        number = Number(left, right, None)
        if isinstance(left, Number):
            left.parent = number
        if isinstance(right, Number):
            right.parent = number
        return number

    def copy(self) -> Number:
        left = self.left if isinstance(self.left, int) else self.left.copy()
        right = self.right if isinstance(self.right, int) else self.right.copy()
        retval = Number(left, right, None)
        if isinstance(left, Number):
            left.parent = retval

        if isinstance(right, Number):
            right.parent = retval
        return retval

    def add(self, other: Number) -> Number:
        left = self.copy()
        right = other.copy()

        if left.parent is not None or right.parent is not None:
            raise ValueError("Can't add two non-roots")

        retval = Number(left, right, None)
        left.parent = retval
        right.parent = retval
        retval.reduce()
        return retval

    def magnitude(self) -> int:
        total = 0
        total += 3 * (
            self.left if isinstance(self.left, int) else self.left.magnitude()
        )
        total += 2 * (
            self.right if isinstance(self.right, int) else self.right.magnitude()
        )
        return total

    def add_to_left_neighbor(self, amount: int) -> None:
        next_up = self.parent
        this_up = self
        while this_up is next_up.left:
            this_up = next_up
            next_up = next_up.parent
            if next_up is None:
                return

        this_down = next_up
        next_down = next_up.left
        if isinstance(next_down, int):
            this_down.left += amount
            return

        while isinstance(next_down, Number):
            this_down = next_down
            next_down = this_down.right

        this_down.right += amount

    def add_to_right_neighbor(self, amount: int) -> None:
        """
        The nearest right neighbor is found by:
          * Go up the tree until the branch is the _left_ branch
          * Step down _once_ to the _right_
          * Then step down the _left_ trees until you find an integer
        """
        next_up = self.parent
        this_up = self
        while this_up is next_up.right:
            this_up = next_up
            next_up = next_up.parent
            if next_up is None:
                return

        this_down = next_up
        next_down = next_up.right
        if isinstance(next_down, int):
            this_down.right += amount
            return

        while isinstance(next_down, Number):
            this_down = next_down
            next_down = this_down.left

        this_down.left += amount

    def explode(self):
        if isinstance(self.left, Number) or isinstance(self.right, Number):
            raise ValueError("Can't explode non-terminal node")

        self.add_to_left_neighbor(self.left)
        self.add_to_right_neighbor(self.right)

        # Collapse parent into single node
        parent = self.parent
        if parent is None:
            raise ValueError("Can't explode root")

        if self is parent.left:
            parent.left = 0
        else:
            parent.right = 0

    def split_left(self):
        if not isinstance(self.left, int):
            raise ValueError("Can't split leaf")
        self.left = Number(int(floor(self.left / 2)), int(ceil(self.left / 2)), self)

    def split_right(self):
        if not isinstance(self.right, int):
            raise ValueError("Can't split leaf")
        self.right = Number(int(floor(self.right / 2)), int(ceil(self.right / 2)), self)

    def reduce(self) -> None:
        while True:
            while _explode(self, 0):
                pass

            if _split(self):
                continue

            break

    def pretty(self) -> str:
        output = ["["]
        if isinstance(self.left, int):
            output.append(str(self.left))
        else:
            output.append(self.left.pretty())

        output.append(",")

        if isinstance(self.right, int):
            output.append(str(self.right))
        else:
            output.append(self.right.pretty())
        output.append("]")
        return "".join(output)


def _explode(number: Number, depth: int) -> bool:
    if depth == 3:
        if isinstance(number.left, Number):
            number.left.explode()
            return True

        if isinstance(number.right, Number):
            number.right.explode()
            return True

    if isinstance(number.left, Number):
        if _explode(number.left, depth + 1):
            return True

    if isinstance(number.right, Number):
        if _explode(number.right, depth + 1):
            return True

    return False


def _split(number: Number) -> bool:
    if isinstance(number.left, int):
        if number.left >= 10:
            number.split_left()
            return True
    else:
        if _split(number.left):
            return True

    if isinstance(number.right, int):
        if number.right >= 10:
            number.split_right()
            return True
    else:
        if _split(number.right):
            return True

    return False


class Day18(Solution, day=18):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return [Number.parse(sline) for line in infile if (sline := line.strip())]

    def part1(self):
        val = self.data[0]
        for new_val in self.data[1:]:
            val = val.add(new_val)

        return val.magnitude()

    def part2(self):
        return max(
            left.add(right).magnitude()
            for left, right in its.product(self.data, self.data)
        )
