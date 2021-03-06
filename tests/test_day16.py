from pathlib import Path

from advent.solutions import day16


def test_part1(fixtures_path: Path):
    solution = day16.Day16(fixtures_path / "test_input16.txt")
    assert solution.part1() == 16


def test_part2(fixtures_path: Path):
    solution = day16.Day16(fixtures_path / "test_input162.txt")
    assert solution.part2() == 1
