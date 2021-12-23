from pathlib import Path

from advent.solutions import day22


def test_part1(fixtures_path: Path):
    solution = day22.Day22(fixtures_path / "test_input22.txt")
    assert solution.part1() == 590_784


def test_part2(fixtures_path: Path):
    solution = day22.Day22(fixtures_path / "test_input222.txt")
    assert solution.part2() == 2_758_514_936_282_235
