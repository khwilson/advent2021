from pathlib import Path

from advent.solutions import day04


def test_part1(fixtures_path: Path):
    solution = day04.Day04(fixtures_path / "test_input04.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day04.Day04(fixtures_path / "test_input04.txt")
    assert solution.part2() == None
