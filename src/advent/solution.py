"""
Generic solution template for Advent of Code 2021
"""
from __future__ import annotations

from typing import Any, List, Optional, Union

from .types import FilenameType


class Solution:

    _day_to_class = {}

    def __init__(self, input_file: Optional[FilenameType] = None):
        self.input_file = input_file
        self._data = None

    def __init_subclass__(cls, day: int, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.day = day
        Solution._day_to_class[day] = cls

    @staticmethod
    def for_day(day: int) -> Solution:
        return Solution._day_to_class[day]

    @property
    def data(self):
        """Parsed data for the problem"""
        if not self._data:
            self._data = self.parse()
        return self._data

    def parse(self) -> List[Any]:
        """A parser for the input file. Should be overwritten by subclass"""

    def part1(self) -> Optional[Union[int, str]]:
        """Solution to part 1"""

    def part2(self) -> Optional[Union[int, str]]:
        """Solution to part 2"""
