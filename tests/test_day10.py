from pathlib import Path

from advent.solutions import day10


def test_part1(fixtures_path: Path):
    solution = day10.Day10(fixtures_path / "test_input10.txt")
    assert solution.part1() == 26397


def test_part2(fixtures_path: Path):
    solution = day10.Day10(fixtures_path / "test_input10.txt")
    assert solution.part2() == 288957
