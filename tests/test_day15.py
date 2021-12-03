from pathlib import Path

from advent.solutions import day15


def test_part1(fixtures_path: Path):
    solution = day15.Day15(fixtures_path / "test_input15.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day15.Day15(fixtures_path / "test_input15.txt")
    assert solution.part2() == None
