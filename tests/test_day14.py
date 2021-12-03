from pathlib import Path

from advent.solutions import day14


def test_part1(fixtures_path: Path):
    solution = day14.Day14(fixtures_path / "test_input14.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day14.Day14(fixtures_path / "test_input14.txt")
    assert solution.part2() == None
