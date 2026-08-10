import random

from sudoku_board import EMPTY, SIZE, create_empty_board, deep_copy
from sudoku_solver import fill_board, has_unique_solution


def remove_cells(board, clues):
    target_removed = SIZE * SIZE - clues
    removed = 0
    attempts = 0
    while removed < target_removed and attempts < 1000:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] == EMPTY:
            attempts += 1
            continue

        original = board[row][col]
        board[row][col] = EMPTY
        if has_unique_solution(board):
            removed += 1
        else:
            board[row][col] = original
        attempts += 1


def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    puzzle = deep_copy(board)
    remove_cells(puzzle, clues)
    return puzzle, solution
