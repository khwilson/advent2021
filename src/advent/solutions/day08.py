from ..solution import Solution


class Day08(Solution, day=8):
    def parse(self):
        inputs = []
        outputs = []
        with open(self.input_file, "rt") as infile:
            for line in infile:
                the_in, the_out = line.strip().split('|')
                inputs.append(the_in.strip().split())
                outputs.append(the_out.strip().split())

        return {
            "inputs": inputs,
            "outputs": outputs,
        }

    def part1(self):
        return sum(1 for output in self.data["outputs"] for out in output if len(out) in [2, 3, 4, 7])

    def part2(self):
        # 2, 3, and 5 use five lines
        # 0, 6, and 9 use six lines
        # 1 uses 2 lines
        # 4 uses 4 lines
        # 7 uses 3 lines
        # 8 uses 7 lines
        total = 0
        for the_in, the_out in zip(self.data["inputs"], self.data["outputs"]):
            patterns = {}
            patterns[1] = frozenset([x for x in the_in if len(x) == 2][0])
            patterns[4] = frozenset([x for x in the_in if len(x) == 4][0])
            patterns[7] = frozenset([x for x in the_in if len(x) == 3][0])
            patterns[8] = frozenset([x for x in the_in if len(x) == 7][0])

            len_fives = [frozenset(x) for x in the_in if len(x) == 5]

            patterns[3] = [x for x in len_fives if patterns[1] <= x][0]
            len_fives.remove(patterns[3])
            patterns[2] = [x for x in len_fives if len(patterns[4] & x) == 2][0]
            patterns[5] = [x for x in len_fives if len(patterns[4] & x) == 3][0]

            patterns[6] = frozenset(patterns[5] | (patterns[8] - patterns[7]))
            patterns[9] = frozenset(patterns[3] | patterns[4])
            patterns[0] = [frozenset(x) for x in the_in if len(x) == 6 and set(x) not in [patterns[6], patterns[9]]][0]

            mapper = {val: key for key, val in patterns.items()}

            out = int("".join(str(mapper[frozenset(x)]) for x in the_out))
            total += out

        return total
