import os
from pathlib import Path
from typing import Optional

import click
import requests
from dotenv import load_dotenv

from .solution import Solution

load_dotenv()


@click.command()
@click.argument("day", type=int)
@click.option("--input-file", type=str, default=None)
def run_solution(day: int, input_file: Optional[str]):
    """Advent of code 2021"""
    day = int(day)

    if not day in Solution._day_to_class:
        raise click.BadParameter("Not a valid day")

    if not input_file:
        input_file = Path(os.environ.get("DATA_DIR")) / f"input{day:02d}.txt"

    solution = Solution._day_to_class[day](input_file)
    click.echo(f"The solution to part 1 is: {solution.part1()}")
    click.echo(f"The solution to part 2 is: {solution.part2()}")


@click.command("download")
@click.argument("day", type=int)
@click.option("--input-file", type=str, default=None)
def download_data(day: int, input_file: Optional[str]):
    resp = requests.get(f"https://adventofcode.com/2021/day/{day}/input")
    resp.raise_for_status()

    if not input_file:
        input_file = Path(os.environ.get("DATA_DIR")) / f"input{day:02d}.txt"

    with open(input_file, "wb") as outfile:
        outfile.write(resp.content)


if __name__ == "__main__":
    run_solution()
