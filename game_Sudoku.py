# import random
#
# choices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#
# index = random.randint(0, len(choices) - 1)
# index = random.randrange(len(choices))
# item = random.choice(choices)
#
# choices[index]

import math
import random


class SudokuCell:
    def __init__(self, value, fixed):
        self.value = value
        self.fixed = fixed

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"SudokuCell({self.value}, {self.fixed})"


initial_puzzle_array = [
    [4, 0, 0, 2, 6, 9, 0, 0, 0],
    [6, 8, 2, 0, 7, 1, 0, 9, 3],
    [1, 0, 7, 8, 3, 4, 5, 6, 2],
    [0, 2, 6, 0, 0, 0, 0, 4, 7],
    [3, 0, 4, 6, 8, 2, 9, 1, 5],
    [9, 0, 1, 7, 4, 3, 0, 2, 8],
    [5, 1, 9, 0, 2, 6, 0, 0, 4],
    [2, 4, 0, 9, 5, 7, 1, 3, 6],
    [7, 6, 3, 4, 1, 0, 2, 5, 9]
]

solved = [
    [7, 4, 5, 6, 9, 8, 2, 1, 3],
    [2, 9, 1, 7, 3, 4, 8, 6, 5],
    [3, 8, 6, 5, 2, 1, 4, 9, 7],
    [4, 6, 3, 8, 5, 2, 9, 7, 1],
    [5, 2, 9, 3, 1, 7, 6, 8, 4],
    [1, 7, 8, 9, 4, 6, 5, 3, 2],
    [6, 3, 4, 1, 8, 5, 7, 2, 9],
    [8, 1, 2, 4, 7, 9, 3, 5, 6],
    [9, 5, 7, 2, 6, 3, 1, 4, 8]
]


class SudokuBoard:
    def __init__(self, initial_puzzle = None, size = None, difficulty = None):

        if initial_puzzle:
            self.puzzle = []
            for row in initial_puzzle:
                _row = []
                for value in row:
                    _row.append(SudokuCell(value, value != 0))
                self.puzzle.append(_row)
            self.size = len(self.puzzle)
            return

        if size and difficulty:
            zero_puzzle = []
            for i in range(size):
                zero_puzzle.append([0] * size)

            self.puzzle = []
            for row in zero_puzzle:
                _row = []
                for value in row:
                    _row.append(SudokuCell(value, value != 0))
                self.puzzle.append(_row)
            self.size = len(self.puzzle)

            SudokuSolver.solve_sudoku(self)

            if difficulty == "e":
                keep_cells_ratio = 0.75
            elif difficulty == "m":
                keep_cells_ratio = 0.5
            elif difficulty == "h":
                keep_cells_ratio = 0.25
            else:
                raise ValueError("Difficulty must be either e, m, or h.")

            remove_cells_count = int(size * size - size * size * keep_cells_ratio)

            counter = 0
            while counter < remove_cells_count:
            # for _ in range(remove_cells_count):
                cell = self.puzzle[random.randint(0, size - 1)][random.randint(0, size - 1)]

                if cell.value != 0:
                    cell.value = 0
                    counter += 1
            return

    def print_board(self):
        box_size = int(math.sqrt(self.size))

        # for i in range(0, len(self.puzzle)):
        for i, row in enumerate(self.puzzle):
            if i % box_size == 0:
                print("-\t" * (self.size + box_size + 1))
            print_str = ""
            for j, cell in enumerate(row):
                if j % box_size == 0:
                    print_str += f"|\t"
                print_str += f"{str(cell)}\t"  # cell.value
                # \t = tab character
                # print(str(cell), end=" ")
            print_str += f"|\t"
            print(print_str)

        print("-\t" * (self.size + box_size + 1))

    def checkIfValueIsOk(self, i, j):
        value = self.puzzle[i][j].value

        if value == 0:
            return True

        for k, row in enumerate(self.puzzle):
            if self.puzzle[i][k].value == value and k != j:
                # print("Value in row")
                return False
            if self.puzzle[k][j].value == value and k != i:
                # print("Value in column")
                return False

        box_size = int(math.sqrt(self.size))

        for k in range((i // box_size) * box_size,  (i // box_size) * box_size + box_size):
            for l in range((j // box_size) * box_size, (j // box_size) * box_size + box_size):
                if self.puzzle[k][l].value == value and k != i and l != j:
                    # print("Value in small grid")
                    return False

        return True

    def checkIfIsSolved(self):
        for i, row in enumerate(self.puzzle):
            for j, cell in enumerate(row):
                if cell.value == 0:
                    return False
                if not self.checkIfValueIsOk(i, j):
                    return False

        return True

    def get_cell(self, i, j):
        return self.puzzle[i][j]


class SudokuSolver:
    @staticmethod
    def solve_sudoku(sudoku_board):
        return SudokuSolver.__solve_sudoku(sudoku_board, 0, 0)

    @staticmethod
    def __solve_sudoku(sudoku_board, i, j):
        length = sudoku_board.size

        next_i = i
        next_j = j + 1

        if i >= length:
            # as all other cells have valid values at this point
            return True

        if j >= length - 1:
            next_i = i + 1
            next_j = 0

        if not sudoku_board.get_cell(i, j).fixed:
            # Generate an array from 1 to n
            values = [value for value in range(1, length + 1)]
            # Shuffle the array randomly
            random.shuffle(values)  # [ 4, 6, 7, 3, 5, ...]

            for k in range(length):
                sudoku_board.get_cell(i, j).value = values[k]
                if sudoku_board.checkIfValueIsOk(i, j):
                    if SudokuSolver.__solve_sudoku(sudoku_board, next_i, next_j):
                        # the call from below has found a solution, no need to keep trying other values
                        return True

            sudoku_board.get_cell(i, j).value = 0
            return False
        else:
            return SudokuSolver.__solve_sudoku(sudoku_board, next_i, next_j)


if __name__ == "__main__":
    # board = SudokuBoard(initial_puzzle_array)
    # solver = SudokuSolver()
    # SudokuSolver.solve_sudoku(board)
    # print(board.puzzle)


    # i = 8
    # j = 7
    # box_size = 3
    # for k in range((i // box_size) * box_size, (i // box_size) * box_size + box_size):
    #     print(k)

    #
    # board.print_board()
    # print(board.checkIfValueIsOk(2, 6))
    # print(board.checkIfIsSolved())

    board = SudokuBoard(size=9, difficulty='h')

    board.print_board()