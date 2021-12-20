from pathlib import Path

from advent.solutions import day19


def test_rotations():
    base = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    refl, perm = day19.rotations[0]
    assert refl(*perm(1, 2, 3)) == (1, 2, 3)
    assert len(day19.rotations) == 24
    assert (
        len(
            {
                (refl(*perm(*base[0])), refl(*perm(*base[1])), refl(*perm(*base[2])))
                for refl, perm in day19.rotations
            }
        )
        == 24
    )


def test_part1(fixtures_path: Path):
    solution = day19.Day19(fixtures_path / "test_input19.txt")
    assert solution.part1() == 79


def test_part2(fixtures_path: Path):
    solution = day19.Day19(fixtures_path / "test_input19.txt")
    assert solution.part2() == 3621
