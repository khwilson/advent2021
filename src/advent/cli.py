""" CLI for AoC 2021 """
import os
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv

from .solution import Solution

load_dotenv()


@click.command()
@click.argument("day", type=int)
@click.option("--input-file", type=str, default=None)
def run_solution(day: int, input_file: Optional[str]):
    """Advent of code 2021"""
    day = int(day)

    try:
        solution = Solution.for_day(day)
    except KeyError:
        raise click.BadParameter("Not a valid day")

    if not input_file:
        input_file = Path(os.environ.get("DATA_DIR")) / f"input{day:02d}.txt"

    solution = solution(input_file)
    click.echo(f"The solution to part 1 is: {solution.part1()}")
    click.echo(f"The solution to part 2 is: {solution.part2()}")


if __name__ == "__main__":
    run_solution()
