from pathlib import Path

from advent.solutions import day17


def test_part1(fixtures_path: Path):
    solution = day17.Day17(fixtures_path / "test_input17.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day17.Day17(fixtures_path / "test_input17.txt")
    assert solution.part2() == None
