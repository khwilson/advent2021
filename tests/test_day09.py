from pathlib import Path

from advent.solutions import day09


def test_part1(fixtures_path: Path):
    solution = day09.Day09(fixtures_path / "test_input09.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day09.Day09(fixtures_path / "test_input09.txt")
    assert solution.part2() == None
