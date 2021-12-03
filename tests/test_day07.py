from pathlib import Path

from advent.solutions import day07


def test_part1(fixtures_path: Path):
    solution = day07.Day07(fixtures_path / "test_input07.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day07.Day07(fixtures_path / "test_input07.txt")
    assert solution.part2() == None
