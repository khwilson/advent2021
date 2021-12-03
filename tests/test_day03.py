from pathlib import Path

from advent.solutions import day03


def test_part1(fixtures_path: Path):
    solution = day03.Day03(fixtures_path / "test_input03.txt")
    assert solution.part1() == 198


def test_part2(fixtures_path: Path):
    solution = day03.Day03(fixtures_path / "test_input03.txt")
    assert solution.part2() == 230
