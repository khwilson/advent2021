from pathlib import Path

from advent.solutions import day06


def test_part1(fixtures_path: Path):
    solution = day06.Day06(fixtures_path / "test_input06.txt")
    assert solution.part1() == 5934


def test_part2(fixtures_path: Path):
    solution = day06.Day06(fixtures_path / "test_input06.txt")
    assert solution.part2() == 26984457539
