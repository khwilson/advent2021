import copy

from ..solution import Solution


def doit(code, board, num_rounds):
    for i in range(len(board)):
        board[i] = (
            [False] * (num_rounds * 2 + 2) + board[i] + [False] * (num_rounds * 2 + 2)
        )

    board = (
        [[0 for _ in range(len(board[0]))] for _ in range(num_rounds * 2 + 2)]
        + board
        + [[0 for _ in range(len(board[0]))] for _ in range(num_rounds * 2 + 2)]
    )
    for _ in range(num_rounds):
        new_board = copy.deepcopy(board)
        for i in range(1, len(board) - 1):
            for j in range(1, len(board[0]) - 1):
                x = (
                    (board[i - 1][j - 1] << 8)
                    + (board[i - 1][j] << 7)
                    + (board[i - 1][j + 1] << 6)
                    + (board[i][j - 1] << 5)
                    + (board[i][j] << 4)
                    + (board[i][j + 1] << 3)
                    + (board[i + 1][j - 1] << 2)
                    + (board[i + 1][j] << 1)
                    + (board[i + 1][j + 1])
                )
                new_board[i][j] = code[x]
        board = new_board

        # Shrink the board to deal with boundary issues
        board = board[1:-1]
        board = [row[1:-1] for row in board]

    return sum(sum(row) for row in board)


class Day20(Solution, day=20):
    def parse(self):
        with open(self.input_file, "rt") as infile:
            code = [c == "#" for c in next(infile).strip()]
            next(infile)
            board = [
                [c == "#" for c in sline] for line in infile if (sline := line.strip())
            ]

        return {
            "code": code,
            "board": board,
        }

    def part1(self):
        code = self.data["code"]
        board = copy.deepcopy(self.data["board"])
        return doit(code, board, 2)

    def part2(self):
        code = self.data["code"]
        board = copy.deepcopy(self.data["board"])
        return doit(code, board, 50)
