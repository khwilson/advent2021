from typing import Optional, Union

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

    @property
    def data(self):
        if not self._data:
            self._data = self.parser()
        return self._data

    def parser(self):
        pass

    def part1(self) -> Optional[Union[int, str]]:
        return None

    def part2(self) -> Optional[Union[int, str]]:
        return None
