from pathlib import Path

from advent.solutions import day25


def test_part1(fixtures_path: Path):
    solution = day25.Day25(fixtures_path / "test_input25.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day25.Day25(fixtures_path / "test_input25.txt")
    assert solution.part2() == None
