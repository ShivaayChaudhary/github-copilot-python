from app import CURRENT

def test_index_route(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'<' in resp.data

def test_new_game_and_current_updated(client):
    resp = client.get('/new?clues=30')
    assert resp.status_code == 200
    data = resp.get_json()
    puzzle = data.get('puzzle')
    assert puzzle is not None
    assert len(puzzle) == 9
    non_empty = sum(1 for r in puzzle for c in r if c != 0)
    assert non_empty == 30
    assert CURRENT['solution'] is not None


def test_new_game_difficulty_levels(client):
    for difficulty, expected_clues in [('easy', 40), ('medium', 34), ('hard', 28)]:
        resp = client.get(f'/new?difficulty={difficulty}')
        assert resp.status_code == 200
        data = resp.get_json()
        puzzle = data.get('puzzle')
        assert puzzle is not None
        non_empty = sum(1 for r in puzzle for c in r if c != 0)
        assert non_empty == expected_clues
        assert CURRENT['solution'] is not None


def test_new_game_legacy_clues_parameter(client):
    resp = client.get('/new?clues=30')
    assert resp.status_code == 200
    data = resp.get_json()
    puzzle = data.get('puzzle')
    assert puzzle is not None
    non_empty = sum(1 for r in puzzle for c in r if c != 0)
    assert non_empty == 30


def test_check_no_game(client):
    from app import CURRENT as CUR
    backup = CUR.copy()
    try:
        CUR['solution'] = None
        resp = client.post('/check', json={'board': [[0]*9 for _ in range(9)]})
        assert resp.status_code == 400
        data = resp.get_json()
        assert 'error' in data
    finally:
        CUR.update(backup)

def test_check_correct_and_incorrect(client):
    resp = client.get('/new?clues=35')
    solution = CURRENT['solution']
    resp = client.post('/check', json={'board': solution})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get('incorrect') == []
    assert data.get('complete') is True

    # Make a copy and leave some empties - empty cells should not be marked incorrect
    board = [row[:] for row in solution]
    # find a user-editable cell from CURRENT['puzzle'] (where puzzle == 0)
    puzzle = CURRENT['puzzle']
    empty_i = empty_j = None
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                board[i][j] = 0
                empty_i, empty_j = i, j
                break
        if empty_i is not None:
            break
    resp = client.post('/check', json={'board': board})
    data = resp.get_json()
    # that empty should not be reported as incorrect
    assert data.get('complete') is False
    assert [empty_i, empty_j] not in data.get('incorrect')

    # Now modify a user-editable cell to an incorrect value and ensure it's reported
    board = [row[:] for row in solution]
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                board[i][j] = (board[i][j] % 9) + 1
                wrong_i, wrong_j = i, j
                break
        else:
            continue
        break
    resp = client.post('/check', json={'board': board})
    data = resp.get_json()
    assert [wrong_i, wrong_j] in data.get('incorrect')


def test_solution_endpoint(client):
    resp = client.get('/new?clues=35')
    assert resp.status_code == 200
    sol_resp = client.get('/solution')
    assert sol_resp.status_code == 200
    sol = sol_resp.get_json().get('solution')
    assert sol is not None
    # solution should match CURRENT['solution']
    from app import CURRENT
    assert sol == CURRENT['solution']
