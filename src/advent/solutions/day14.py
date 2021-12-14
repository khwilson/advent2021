import itertools as its
from collections import Counter, defaultdict

from ..solution import Solution


class Day14(Solution, day=14):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            base = next(infile).strip()
            next(infile)
            infixes = {}
            for line in infile:
                line = line.strip()
                left = line[:2]
                right = line[-1]
                infixes[left] = right
        return {
            "base": base,
            "infixes": infixes,
        }

    def part1(self):
        base = self.data["base"]
        infixes = self.data["infixes"]
        for _ in range(10):
            new_base = []
            for left, right in its.pairwise(base):
                new_base.append(left)
                both = left + right
                if both in infixes:
                    new_base.append(infixes[both])
            new_base.append(base[-1])
            base = "".join(new_base)
        counts = Counter(base)
        return max(counts.values()) - min(counts.values())

    def part2(self):
        base = self.data["base"]
        infixes = self.data["infixes"]
        pairs_to_counts = defaultdict(int)
        for left, right in its.pairwise(base):
            pairs_to_counts[left + right] += 1

        for _ in range(40):
            new_pairs_to_counts = defaultdict(int)
            for key, val in pairs_to_counts.items():
                left, right = key
                if key in infixes:
                    new_pairs_to_counts[left + infixes[key]] += val
                    new_pairs_to_counts[infixes[key] + right] += val
                else:
                    new_pairs_to_counts[key] += pairs_to_counts[key]
            pairs_to_counts = new_pairs_to_counts

        final_counts = defaultdict(int)
        for key, val in pairs_to_counts.items():
            left, right = key
            final_counts[left] += val
        final_counts[base[-1]] += 1

        return max(final_counts.values()) - min(final_counts.values())
