from pathlib import Path

from advent.solutions import day12


def test_part1(fixtures_path: Path):
    solution = day12.Day12(fixtures_path / "test_input12.txt")
    assert solution.part1() == 10


def test_part2(fixtures_path: Path):
    solution = day12.Day12(fixtures_path / "test_input12.txt")
    assert solution.part2() == 36
