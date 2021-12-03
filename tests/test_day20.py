from pathlib import Path

from advent.solutions import day20


def test_part1(fixtures_path: Path):
    solution = day20.Day20(fixtures_path / "test_input20.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day20.Day20(fixtures_path / "test_input20.txt")
    assert solution.part2() == None
