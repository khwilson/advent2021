from pathlib import Path

from advent.solutions import day22


def test_part1(fixtures_path: Path):
    solution = day22.Day22(fixtures_path / "test_input22.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day22.Day22(fixtures_path / "test_input22.txt")
    assert solution.part2() == None
