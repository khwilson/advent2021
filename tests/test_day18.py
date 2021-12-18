from pathlib import Path

from advent.solutions import day18


def test_magnitude():
    number = day18.Number.parse([1, 2])
    assert number.magnitude() == 7
    number = day18.Number.parse([1, [2, 3]])
    assert number.magnitude() == 3 * 1 + 2 * (3 * 2 + 2 * 3)


def test_add():
    left = day18.Number.parse([1, 2])
    right = day18.Number.parse([3, 4])
    new = left.add(right)
    assert new.left.left == 1
    assert new.left.right == 2
    assert new.right.left == 3
    assert new.right.right == 4


def test_explode():
    number = day18.Number.parse([[1, 2], [3, 4]])
    number.left.explode()
    should_be = day18.Number.parse([0, [5, 4]])
    assert number.pretty() == should_be.pretty()


def test_split_left():
    number = day18.Number.parse([[1, 2], [3, 4]])
    number.right.split_left()
    should_be = day18.Number.parse([[1, 2], [[1, 2], 4]])
    assert number.pretty() == should_be.pretty()


def test_split_right():
    number = day18.Number.parse([[1, 2], [3, 5]])
    number.right.split_right()
    should_be = day18.Number.parse([[1, 2], [3, [2, 3]]])
    assert number.pretty() == should_be.pretty()


def test__split():
    number = day18.Number.parse([[11, 2], [3, 5]])
    assert day18._split(number)
    should_be = day18.Number.parse([[[5, 6], 2], [3, 5]])
    assert number.pretty() == should_be.pretty()

    number = day18.Number.parse([[9, 2], [3, 5]])
    assert not day18._split(number)
    should_be = day18.Number.parse([[9, 2], [3, 5]])
    assert number.pretty() == should_be.pretty()

    number = day18.Number.parse([[11, 2], [13, 5]])
    assert day18._split(number)
    should_be = day18.Number.parse([[[5, 6], 2], [13, 5]])
    assert number.pretty() == should_be.pretty()

    assert day18._split(number)
    should_be = day18.Number.parse([[[5, 6], 2], [[6, 7], 5]])
    assert number.pretty() == should_be.pretty()

    assert not day18._split(number)


def test__explode():
    number = day18.Number.parse([[[[[9, 8], 1], 2], 3], 4])
    assert day18._explode(number, 0)
    should_be = day18.Number.parse([[[[0, 9], 2], 3], 4])
    assert number.pretty() == should_be.pretty()

    number = day18.Number.parse([7, [6, [5, [4, [3, 2]]]]])
    assert day18._explode(number, 0)
    should_be = day18.Number.parse([7, [6, [5, [7, 0]]]])
    assert number.pretty() == should_be.pretty()
    assert not day18._explode(number, 0)

    number = day18.Number.parse([[6, [5, [4, [3, 2]]]], 1])
    assert day18._explode(number, 0)
    should_be = day18.Number.parse([[6, [5, [7, 0]]], 3])
    assert number.pretty() == should_be.pretty()


def test_reduce():
    number = day18.Number.parse([[6, [5, [8, [3, 2]]]], 1])
    number.reduce()
    should_be = day18.Number.parse([[6, [[5, 5], [0, 6]]], 3])
    assert number.pretty() == should_be.pretty()


def test_add_again():
    left = day18.Number.parse([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
    right = day18.Number.parse([1, 1])
    new = left.add(right)
    should_be = day18.Number.parse([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])
    assert new.pretty() == should_be.pretty()


def test_part1(fixtures_path: Path):
    solution = day18.Day18(fixtures_path / "test_input18.txt")
    assert solution.part1() == 4140


def test_part2(fixtures_path: Path):
    solution = day18.Day18(fixtures_path / "test_input18.txt")
    assert solution.part2() == 3993
