from pathlib import Path

from advent.solutions import day23


def test_part1(fixtures_path: Path):
    solution = day23.Day23(fixtures_path / "test_input23.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day23.Day23(fixtures_path / "test_input23.txt")
    assert solution.part2() == None
