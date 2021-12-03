from pathlib import Path

from advent.solutions import day21


def test_part1(fixtures_path: Path):
    solution = day21.Day21(fixtures_path / "test_input21.txt")
    assert solution.part1() == None


def test_part2(fixtures_path: Path):
    solution = day21.Day21(fixtures_path / "test_input21.txt")
    assert solution.part2() == None
