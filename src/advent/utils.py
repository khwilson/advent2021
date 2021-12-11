from __future__ import annotations

from typing import Tuple


class Coord:
    """
    Represent an x/y coordiate as a pair of ints. Also allow for
    adding and multiplying them pointwise.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __mul__(self, other: int) -> Coord:
        return Coord(self.x * other, self.y * other)

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def rotate_cw(self) -> Coord:
        return Coord(-self.y, self.x)

    def rotate_ccw(self) -> Coord:
        return Coord(self.y, -self.x)


NORTH = Coord(0, 1)
SOUTH = Coord(0, -1)
EAST = Coord(1, 0)
WEST = Coord(-1, 0)


def around(x: int, y: int, shape: Tuple[int, int]):
    if x + 1 < shape[0]:
        yield x + 1, y
    if x - 1 >= 0:
        yield x - 1, y

    if y + 1 < shape[1]:
        yield x, y + 1

    if y - 1 >= 0:
        yield x, y - 1


def saround(x: int, y: int, shape: Tuple[int, int]):
    yield from around(x, y, shape)

    if x + 1 < shape[0] and y + 1 < shape[1]:
        yield x + 1, y + 1
    if x + 1 < shape[0] and y - 1 >= 0:
        yield x + 1, y - 1
    if x - 1 >= 0 and y + 1 < shape[1]:
        yield x - 1, y + 1
    if x - 1 >= 0 and y - 1 >= 0:
        yield x - 1, y - 1
