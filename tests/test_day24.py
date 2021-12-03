from pathlib import Path

from advent.solutions import day24


def test_part1(fixtures_path: Path):
    solution = day24.Day24(fixtures_path / "test_input24.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day24.Day24(fixtures_path / "test_input24.txt")
    assert solution.part2() == None
