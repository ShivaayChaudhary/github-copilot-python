import sudoku_logic as sl

def test_create_and_copy_board():
    b = sl.create_empty_board()
    assert len(b) == sl.SIZE
    assert all(len(row) == sl.SIZE for row in b)
    b2 = sl.deep_copy(b)
    b[0][0] = 1
    assert b2[0][0] == sl.EMPTY

def test_is_safe_basic():
    board = sl.create_empty_board()
    board[0][0] = 1
    assert not sl.is_safe(board, 0, 1, 1)
    assert sl.is_safe(board, 0, 1, 2)

def test_fill_board_and_solution_properties():
    board = sl.create_empty_board()
    assert sl.fill_board(board) is True
    assert all(all(cell != sl.EMPTY for cell in row) for row in board)
    for row in board:
        assert set(row) == set(range(1, sl.SIZE + 1))
    for col in range(sl.SIZE):
        col_vals = {board[row][col] for row in range(sl.SIZE)}
        assert col_vals == set(range(1, sl.SIZE + 1))

def test_remove_cells_and_generate_puzzle():
    board = sl.create_empty_board()
    sl.fill_board(board)
    clues = 30
    sl.remove_cells(board, clues)
    non_empty = sum(1 for r in board for c in r if c != sl.EMPTY)
    assert non_empty == clues
    puzzle, solution = sl.generate_puzzle(clues=28)
    assert all(all(c != sl.EMPTY for c in row) for row in solution)
    non_empty2 = sum(1 for r in puzzle for c in r if c != sl.EMPTY)
    assert non_empty2 == 28
