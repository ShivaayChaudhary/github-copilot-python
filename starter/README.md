# Flask Sudoku Game

A web-based 9×9 Sudoku game built with Python and Flask. The application allows players to generate and solve Sudoku puzzles with multiple difficulty levels, hints, puzzle checking, a timer, dark mode, and a Top 10 leaderboard stored in browser localStorage.

## Project Overview

The application provides an interactive Sudoku experience in the browser.

The backend generates valid Sudoku puzzles and ensures that generated puzzles have a unique solution. Sudoku solving and generation logic is organized into reusable modules using a backtracking approach.

The frontend provides difficulty selection, hints, puzzle validation, timer tracking, dark mode, and leaderboard functionality.

## Features

- Generate new 9×9 Sudoku puzzles
- Easy, Medium, and Hard difficulty levels
- Generated puzzles have exactly one unique solution
- Prefilled cells are locked
- Backtracking-based Sudoku solver
- Hint functionality
- Check Solution functionality
- Highlight incorrect user entries
- Completion detection with a congratulatory message
- Game timer
- Top 10 leaderboard
- Leaderboard persistence using browser localStorage
- Leaderboard stores:
  - Player name
  - Completion time
  - Difficulty
  - Number of hints used
- Light and dark mode
- Alternating colors for 3×3 Sudoku regions
- Responsive user interface
- Accessible UI elements and live feedback

## Technologies Used

- Python 3
- Flask
- HTML5
- CSS3
- JavaScript
- Jinja2
- pytest

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ShivaayChaudhary/github-copilot-python.git