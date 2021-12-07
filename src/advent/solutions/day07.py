import numpy as np

from ..solution import Solution


class Day07(Solution, day=7):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            return [int(x) for x in infile.read().strip().split(",")]

    def part1(self):
        """
        Want to compute argmin_x s(x) where s(x) = Σ_{d ∈ data} |x - d|. Unfortunately,
        s isn't smooth, but we can use the notion of subdifferentials.

        In particular, the subdifferential ∂_d(x) of |x - d| is {-1} for x < d, {1}
        for x > d, and [-1, 1] for x = d. Then the subdifferential of s is

            ∂s(x) = ∑_d ∂_d(x)

        where the sum is the Minkowski sum A + B = { a + b | a ∈ A and b ∈ B }.

        Now the minimum of s will occur at x such that 0 ∈ ∂s(x). Thus, 0 ∈ ∂s(x)
        if and only if::

            |#{d' ∈ data | d' < x} - #{d' ∈ data | d' > x}| ≤ #{d' ∈ data | d' = x} (1)

        (Note that in the above, each of these sets is considered as a multiset.)

        Now consider the case when (1) is satisfied by some x ∉ data. Then let
        D = min {d' ∈ data | d' > x } and d = max {d' ∈ data | d' > x }. Note d < D.

        Claim 1: When data != ∅, d and D exist. For if x > than all d' ∈ data, we would
        have the LHS of (1) to #data > 0 where as the RHS is definitionally 0. Thus,
        D exists. Similarly for d.

        Claim 2: At least one of d and D also satisfies (1). Consider the case when

            #{d' ∈ data | d' < x} > #{d' ∈ data | d' > x}

        so the LHS of (1) is

            #{d' ∈ data | d' < x} - #{d' ∈ data | d' > x} ≥ 0.

        By assumption, this is 0 since the RHS is 0. But then

            #{d' ∈ data | d' < x} = #{d' ∈ data | d' < D}

        and

            #{d' ∈ data | d' > x} = #{d' ∈ data | d' > D} + #{d' ∈ data | d' = D}.

        Putting this altogether:

            #{d' ∈ data | d' < D} - #{d' ∈ data | d' > D} = #{d' ∈ data | d' = D}

        and so (1) is satisfied by D. If on the other hand,

            #{d' ∈ data | d' < x} < #{d' ∈ data | d' > x}

        then d satisfies (1) by the same logic.

        Thus, since we only need one argmin, we need only check for values that
        appear in data.
        """
        data = np.array(self.data)  # Assume this is nonempty
        values, counts = np.unique(data, return_counts=True)
        cumsum = np.cumsum(counts)
        count_lt_value = np.hstack([[0], cumsum[:-1]])

        cumsum = np.cumsum(counts[::-1])[::-1]
        count_gt_value = np.hstack([cumsum[1:], [0]])

        subgradient_has_zero = np.where(
            np.abs(count_lt_value - count_gt_value) <= counts
        )[0]
        if len(subgradient_has_zero) == 0:
            raise ValueError("Something went wrong in the math!")

        argmin = values[subgradient_has_zero[0]]
        return np.sum(np.abs(values - argmin) * counts)

    def part2(self):
        """
        In this part, our s(x) is

            s(x) = Σ_{d ∈ data} |x - d| * (|x - d| + 1) / 2 = 1/2 Σ ((x - d)^2 + |x - d|)

        We can throw away the 1/2 for the gradient computation. The resulting terms of
        our sum have a derivative 2(x - d) + ∂_d(x) which is:

            * 2(x - d) + 1 if x > d
            * 2(x - d) - 1 if x < d
            * [-1, 1] if x = d

        And thus the equivalent of (1) above is:

            |#{d' ∈ data | d' < x} - #{d' ∈ data | d' > x} + Σ_{d' ∈ data} 2(x - d')| ≤ #{d' ∈ data | d' = x} (2)

        Now Σ_{d' ∈ data} 2(x - d') = 2 * x * #data - 2 Σ_{d' ∈ data} d', which is convenient.

        Moreover, it is no longer the case that the argmin actually has to reside in
        data, as the example problem makes clear! So we have two cases: When the
        RHS of (2) is 0 and when the RHS of (2) is _not_ zero.

        In the case the RHS of (2) is not zero, then we proceed as in the previous case.

        In the case where the RHS of (2) is zero, we're looking between the various
        d' ∈ data. Consider the case where a, b ∈ data are two consecutive values in
        data. Then on the interval (a, b) we have

            #{d' ∈ data | d' < x} - #{d' ∈ data | d' > x} - 2 * Σ_{d' ∈ data} d'  (3)

        is constant, and we want to ask if (3) + 2a * #data and (3) + 2b * #data have opposite signs.
        """
        data = np.array(self.data)  # Assume this is nonempty
        values, counts = np.unique(data, return_counts=True)
        cumsum = np.cumsum(counts)
        count_lt_value = np.hstack([[0], cumsum[:-1]])

        cumsum = np.cumsum(counts[::-1])[::-1]
        count_gt_value = np.hstack([cumsum[1:], [0]])

        extra_term = 2 * (values - np.sum(data))

        # The case when the RHS of (2) is not 0:
        subgradient_has_zero = np.where(
            np.abs(count_lt_value - count_gt_value + extra_term) <= counts
        )[0]
        if len(subgradient_has_zero) != 0:
            argmin = values[subgradient_has_zero[0]]
            return np.sum(np.abs(values - argmin) * counts) / 2

        # The case when the RHS of (2) is 0. Here we're considering the values to be the
        # indexed by the a of (a, b) above. So we need to add back in (counts) to the
        # the sum to account for more d' < x.
        lhs = (count_lt_value - count_gt_value - 2 * np.sum(data) + counts)[:-1]
        opp_sign = ((lhs + 2 * values[:-1] * len(data)) < 0) != (
            lhs + 2 * values[1:] * len(data) < 0
        )
        if not opp_sign.any():
            raise ValueError("Need to deal with off to the left and right cases")

        # Now the true minimum is at this value:
        idx = np.where(opp_sign)[0][0]
        a = values[idx]
        b = values[idx + 1]
        ya = lhs[idx] + 2 * a * len(data)
        yb = lhs[idx + 1] + 2 * b * len(data)
        argmin = -ya * (b - a) / (yb - ya) + a

        # However, we're only allowed to move integer amounts, so we have to round
        lower = np.abs(values - np.floor(argmin))
        upper = np.abs(values - np.ceil(argmin))

        return int(
            min(
                [
                    np.sum(lower * (lower + 1) * counts) / 2,
                    np.sum(upper * (upper + 1) * counts) / 2,
                ]
            )
        )
