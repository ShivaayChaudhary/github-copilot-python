from sudoku_board import EMPTY, SIZE, find_empty_cell, is_safe
import random


def solve_board(board):
    return _solve(board)


def _solve(board):
    empty = find_empty_cell(board)
    if empty is None:
        return True

    row, col = empty
    possible = list(range(1, SIZE + 1))
    random.shuffle(possible)
    for candidate in possible:
        if is_safe(board, row, col, candidate):
            board[row][col] = candidate
            if _solve(board):
                return True
            board[row][col] = EMPTY
    return False


def count_solutions(board, limit=2):
    board = [row[:] for row in board]
    solutions = 0

    def search(state):
        nonlocal solutions
        if solutions >= limit:
            return

        empty = find_empty_cell(state)
        if empty is None:
            solutions += 1
            return

        row, col = empty
        for candidate in range(1, SIZE + 1):
            if is_safe(state, row, col, candidate):
                state[row][col] = candidate
                search(state)
                state[row][col] = EMPTY
                if solutions >= limit:
                    return

    search(board)
    return solutions


def has_unique_solution(board):
    return count_solutions(board, limit=2) == 1


def fill_board(board):
    return solve_board(board)
