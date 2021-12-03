from pathlib import Path

from advent.solutions import day13


def test_part1(fixtures_path: Path):
    solution = day13.Day13(fixtures_path / "test_input13.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day13.Day13(fixtures_path / "test_input13.txt")
    assert solution.part2() == None
