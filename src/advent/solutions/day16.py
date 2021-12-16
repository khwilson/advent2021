from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import reduce
from operator import __mul__
from typing import List, Optional, Union

import numpy as np
import pandas as pd

from ..solution import Solution


@dataclass
class Packet:
    version: int
    type_id: int
    data: Union[int, List[Packet]]
    excess: Optional[str] = None

    def total_version(self) -> int:
        if isinstance(self.data, int):
            return self.version
        return self.version + sum(datum.total_version() for datum in self.data)

    def value(self) -> int:
        match self.type_id:
            case 0:
                return sum(datum.value() for datum in self.data)
            case 1:
                return reduce(__mul__, (datum.value() for datum in self.data), 1)
            case 2:
                return min(datum.value() for datum in self.data)
            case 3:
                return max(datum.value() for datum in self.data)
            case 4:
                return self.data
            case 5:
                return int(self.data[0].value() > self.data[1].value())
            case 6:
                return int(self.data[0].value() < self.data[1].value())
            case 7:
                return int(self.data[0].value() == self.data[1].value())
            case _:
                raise ValueError("Can't happen")

    @classmethod
    def parse(cls, packet: str) -> Packet:
        version = int(packet[:3], 2)
        type_id = int(packet[3:6], 2)
        if type_id == 4:
            # Parse a literal
            bits = []
            offset = 6
            while True:
                bits.append(packet[offset + 1 : offset + 5])
                keep_going = packet[offset] != "0"
                offset += 5
                if not keep_going:
                    break
            return Packet(
                version, type_id, int("".join(bits), 2), excess=packet[offset:]
            )
        else:
            # Parse subpackets
            if packet[6] == "0":
                total_length = int(packet[7 : 7 + 15], 2)
                excess = packet[22 : 22 + total_length]
                packets = []
                while excess:
                    packets.append(Packet.parse(excess))
                    excess = packets[-1].excess
                excess = packet[total_length + 22 :]
            else:
                num_packets = int(packet[7 : 7 + 11], 2)
                packets = []
                excess = packet[18:]
                for _ in range(num_packets):
                    packets.append(Packet.parse(excess))
                    excess = packets[-1].excess

            return Packet(
                version=version,
                type_id=type_id,
                data=packets,
                excess=excess,
            )


class Day16(Solution, day=16):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return "".join(f"{int(c, 16):04b}" for c in infile.read().strip())

    def part1(self):
        packet = Packet.parse(self.data)
        return packet.total_version()

    def part2(self):
        packet = Packet.parse(self.data)
        return packet.value()
