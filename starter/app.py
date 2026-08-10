from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

DIFFICULTY_TO_CLUES = {
    'easy': 40,
    'medium': 34,
    'hard': 28
}

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', '').lower()
    clues_arg = request.args.get('clues')
    if difficulty in DIFFICULTY_TO_CLUES:
        clues = DIFFICULTY_TO_CLUES[difficulty]
    else:
        try:
            clues = int(clues_arg) if clues_arg is not None else 35
        except ValueError:
            clues = 35
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    puzzle = CURRENT.get('puzzle')
    if solution is None or puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400

    incorrect = []
    has_empty = False
    # Only validate user-editable cells (where puzzle has EMPTY)
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if puzzle[i][j] != sudoku_logic.EMPTY:
                # prefilled/locked cell - ignore
                continue
            # safe-guard: missing board rows/cols treated as empty
            try:
                v = board[i][j]
            except Exception:
                v = sudoku_logic.EMPTY
            if not v:
                has_empty = True
                continue
            if v != solution[i][j]:
                incorrect.append([i, j])

    complete = (len(incorrect) == 0 and not has_empty)
    return jsonify({'incorrect': incorrect, 'complete': complete})

if __name__ == '__main__':
    app.run(debug=True)