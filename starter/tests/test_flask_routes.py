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
    board = [row[:] for row in solution]
    board[0][0] = (board[0][0] % 9) + 1
    resp = client.post('/check', json={'board': board})
    data = resp.get_json()
    assert len(data.get('incorrect')) >= 1
