from pathlib import Path

from advent.solutions import day23


def test_create_new_hole():
    state = day23.BoardState(
        left=0,
        right=0,
        hall=(0, 0, 0, 0, 0),
        holes=(
            (0, 0),
            (0, 0),
            (0, 0),
            (0, 0),
        )
    )

    new_holes, dist, hole_num = day23.create_new_hole(state, 1)
    assert new_holes == (
            (0, 1),
            (0, 0),
            (0, 0),
            (0, 0),
        )
    assert dist == 1
    assert hole_num == 0

    state = day23.BoardState(
        left=0,
        right=0,
        hall=(0, 0, 0, 0, 0),
        holes=(
            (0, 0),
            (0, 0),
            (0, 100),
            (0, 0),
        )
    )

    new_holes, dist, hole_num = day23.create_new_hole(state, 100)
    assert new_holes == (
            (0, 0),
            (0, 0),
            (100, 100),
            (0, 0),
        )
    assert dist == 0
    assert hole_num == 2

    state = day23.BoardState(
        left=0,
        right=0,
        hall=(0, 0, 0, 0, 0),
        holes=(
            (0, 0),
            (0, 0),
            (0, 100),
            (0, 1),
        )
    )
    new_holes, dist, hole_num = day23.create_new_hole(state, 1000)
    assert new_holes is None
    assert dist is None
    assert hole_num is None


def test_part1(fixtures_path: Path):
    solution = day23.Day23(fixtures_path / "test_input23.txt")
    assert solution.part1() == 12521


def test_part2(fixtures_path: Path):
    solution = day23.Day23(fixtures_path / "test_input23.txt")
    assert solution.part2() == None
