from pathlib import Path

from advent.solutions import day21


def test_simple_game():
    assert day21.play_game_from(1, 17, 8, 20, 2) == (0, 27)
    assert day21.play_game_from(1, 20, 8, 20, 2) == (0, 27)
    assert day21.play_game_from(1, 20, 8, 20, 1) == (27, 0)


def test_part1(fixtures_path: Path):
    solution = day21.Day21(fixtures_path / "test_input21.txt")
    assert solution.part1() == 739_785


def test_part2(fixtures_path: Path):
    solution = day21.Day21(fixtures_path / "test_input21.txt")
    assert solution.part2() == 444356092776315
