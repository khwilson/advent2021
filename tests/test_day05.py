from pathlib import Path

from advent.solutions import day05


def test_part1(fixtures_path: Path):
    solution = day05.Day05(fixtures_path / "test_input05.txt")
    assert solution.part1() == 5


def test_part2(fixtures_path: Path):
    solution = day05.Day05(fixtures_path / "test_input05.txt")
    assert solution.part2() == 12
