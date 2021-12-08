from pathlib import Path

from advent.solutions import day08


def test_part1(fixtures_path: Path):
    solution = day08.Day08(fixtures_path / "test_input08.txt")
    assert solution.part1() == 26


def test_part2(fixtures_path: Path):
    solution = day08.Day08(fixtures_path / "test_input08.txt")
    assert solution.part2() == 61229
