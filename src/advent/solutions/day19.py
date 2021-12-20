import itertools as its

from tqdm.cli import tqdm

from ..solution import Solution

even_permutations = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (y, z, x),
]

odd_permutations = [
    lambda x, y, z: (y, x, z),
    lambda x, y, z: (x, z, y),
    lambda x, y, z: (z, y, x),
]

even_reflections = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (-x, y, -z),
]

odd_reflections = [
    lambda x, y, z: (-x, -y, -z),
    lambda x, y, z: (-x, y, z),
    lambda x, y, z: (x, -y, z),
    lambda x, y, z: (x, y, -z),
]

rotations = [
    (refl, perm) for refl in even_reflections for perm in even_permutations
] + [(refl, perm) for refl in odd_reflections for perm in odd_permutations]


def do_round(scanners, reference_beacons, scanner_to_position):

    for scanner_id, scanner in enumerate(scanners):
        if scanner_id in scanner_to_position:
            continue

        # For each of the 24 rotations
        for refl, perm in rotations:
            # Rotate the beacons relative to their found scanner
            base_data = [refl(*perm(*beacon)) for beacon in scanner]

            # But now _shift_ them relative to a reference beacon
            for local_beacon in base_data:
                for reference_beacon in reference_beacons:
                    this_data = {
                        (
                            beacon[0] - local_beacon[0] + reference_beacon[0],
                            beacon[1] - local_beacon[1] + reference_beacon[1],
                            beacon[2] - local_beacon[2] + reference_beacon[2],
                        )
                        for beacon in base_data
                    }
                    if len(this_data & reference_beacons) >= 12:
                        scanner_pos = (
                            -local_beacon[0] + reference_beacon[0],
                            -local_beacon[1] + reference_beacon[1],
                            -local_beacon[2] + reference_beacon[2],
                        )
                        scanner_to_position[scanner_id] = scanner_pos
                        return (reference_beacons | this_data), scanner_to_position


class Day19(Solution, day=19):
    def parse(self):
        current_scanner = None
        scanners = []
        with open(self.input_file, "rt") as infile:
            for line in infile:
                line = line.strip()
                if line.startswith("---"):
                    if current_scanner:
                        scanners.append(current_scanner)
                    current_scanner = []
                elif line:
                    current_scanner.append(tuple(map(int, line.split(","))))
        scanners.append(current_scanner)
        return scanners

    def part1(self):
        # Scanner 0 will be fixed at 0, 0, 0 so all its coordinates are absolute
        reference_beacons = set(self.data[0])
        scanner_to_position = {0: (0, 0, 0)}

        for _ in tqdm(range(len(self.data) - 1)):
            reference_beacons, scanner_to_position = do_round(
                self.data, reference_beacons, scanner_to_position
            )

        return len(reference_beacons)

    def part2(self):
        reference_beacons = set(self.data[0])
        scanner_to_position = {0: (0, 0, 0)}
        for _ in tqdm(range(len(self.data) - 1)):
            reference_beacons, scanner_to_position = do_round(
                self.data, reference_beacons, scanner_to_position
            )

        return max(
            abs(lx - rx) + abs(ly - ry) + abs(lz - rz)
            for (lx, ly, lz), (rx, ry, rz) in its.product(
                scanner_to_position.values(), scanner_to_position.values()
            )
        )
