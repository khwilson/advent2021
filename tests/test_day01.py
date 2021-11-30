from pathlib import Path

from advent.solutions import day01


def test_part1(fixtures_path: Path):
    solution = day01.Day01(fixtures_path / "test_input01.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day01.Day01(fixtures_path / "test_input01.txt")
    assert solution.part2() == None
