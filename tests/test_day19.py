from pathlib import Path

from advent.solutions import day19


def test_part1(fixtures_path: Path):
    solution = day19.Day19(fixtures_path / "test_input19.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day19.Day19(fixtures_path / "test_input19.txt")
    assert solution.part2() == None
