from pathlib import Path

from advent.solutions import day18


def test_part1(fixtures_path: Path):
    solution = day18.Day18(fixtures_path / "test_input18.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day18.Day18(fixtures_path / "test_input18.txt")
    assert solution.part2() == None
