from pathlib import Path

from advent.solutions import day11


def test_part1(fixtures_path: Path):
    solution = day11.Day11(fixtures_path / "test_input11.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day11.Day11(fixtures_path / "test_input11.txt")
    assert solution.part2() == None
