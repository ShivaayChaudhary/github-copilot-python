# Copilot Instructions for Flask Sudoku

## Project Overview

This project is a Flask-based Sudoku game using Python, HTML, CSS, and JavaScript.

## Development Guidelines

- Preserve the existing Flask application structure and behavior.
- Keep Sudoku generation and solving logic modular and reusable.
- Generated puzzles must have exactly one unique solution.
- Keep Easy, Medium, and Hard difficulty levels.
- Prefilled Sudoku cells must remain locked.
- Keep the timer, Hint, and Check Puzzle functionality working.
- Check Puzzle must distinguish between empty, incorrect, and correctly completed cells.
- Hints must fill one valid empty cell and lock that cell.
- Preserve the Top 10 leaderboard and browser localStorage functionality.
- Preserve Dark Mode and responsive styling.
- Keep the 3×3 Sudoku regions visually distinguishable.
- Use clear, maintainable JavaScript and CSS.
- Avoid unnecessary dependencies or large architectural changes.
- Do not modify working functionality unless required by the feature being implemented.

## Testing

- Use pytest for backend and logic tests.
- Do not remove existing tests.
- Run the complete test suite after significant changes.
- Fix regressions rather than weakening tests.

## Copilot Workflow

Before making significant changes:
1. Inspect the existing implementation.
2. Explain the proposed approach.
3. Identify the files that will change.
4. Make the smallest reasonable changes.
5. Run the existing tests.
6. Report the files changed and test results.

When a suggestion is outside the project requirements or could unnecessarily change working behavior, evaluate it before implementing it.