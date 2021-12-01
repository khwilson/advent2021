from pathlib import Path

from advent.solutions import day02


def test_part1(fixtures_path: Path):
    solution = day02.Day02(fixtures_path / "test_input02.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day02.Day02(fixtures_path / "test_input02.txt")
    assert solution.part2() == None
