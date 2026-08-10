// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let timerInterval = null;
let elapsedSeconds = 0;
let solution = null;
let hintCount = 0;
let gameSaved = false;

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
  const secs = (seconds % 60).toString().padStart(2, '0');
  return `${mins}:${secs}`;
}

function updateTimerDisplay() {
  const timerEl = document.getElementById('timer');
  if (timerEl) {
    timerEl.innerText = formatTime(elapsedSeconds);
  }
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function startTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
  timerInterval = setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  // Create a 9x9 grid of inputs; grid styling handled in CSS
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = 'numeric';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      // mark thicker box borders
      if ((j + 1) % 3 === 0 && j !== SIZE - 1) input.classList.add('box-border-right');
      if ((i + 1) % 3 === 0 && i !== SIZE - 1) input.classList.add('box-border-bottom');
      // alternate 3x3 boxes background
      if (((Math.floor(i / 3) + Math.floor(j / 3)) % 2) === 0) input.classList.add('box-alt');

      // basic input filtering and highlighting hooks
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        highlightSameNumbers(val);
      });
      input.addEventListener('focus', (e) => highlightSameNumbers(e.target.value));
      input.addEventListener('blur', (e) => clearSameNumberHighlights());

      boardDiv.appendChild(input);
    }
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  stopTimer();
  const difficultyEl = document.getElementById('difficulty');
  const difficulty = difficultyEl ? difficultyEl.value : '';
  const query = difficulty ? `?difficulty=${encodeURIComponent(difficulty)}` : '';
  const res = await fetch(`/new${query}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  // fetch solution for hinting and completion checks client-side
  const solRes = await fetch('/solution');
  if (solRes.ok) {
    const solJson = await solRes.json();
    solution = solJson.solution;
  } else {
    solution = null;
  }
  // reset hint count and saved flag
  hintCount = 0;
  gameSaved = false;
  updateHintsDisplay();
  document.getElementById('message').innerText = '';
  startTimer();
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue; // prefilled/locked cells
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (data.complete) {
    stopTimer();
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';
    // prevent double-save
    if (!gameSaved) {
      saveScore();
      gameSaved = true;
    }
    // lock all inputs (prevent further edits)
    for (let inp of inputs) inp.disabled = true;
  } else if (incorrect.size === 0) {
    msg.style.color = '#1976d2';
    msg.innerText = 'All entered cells are correct; puzzle incomplete.';
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

function updateHintsDisplay(){
  const el = document.getElementById('hints-used');
  if(el) el.innerText = `Hints: ${hintCount}`;
}

async function useHint(){
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = Array.from(boardDiv.getElementsByTagName('input'));
  if (!solution) {
    document.getElementById('message').innerText = 'No solution available for hint.';
    return;
  }
  // find editable puzzle cells (original puzzle has 0) that are still empty (no player value)
  const candidates = [];
  for(let i=0;i<SIZE;i++){
    for(let j=0;j<SIZE;j++){
      if(puzzle[i][j] !== 0) continue; // original prefilled
      const idx = i*SIZE + j;
      const inp = inputs[idx];
      if(inp.disabled) continue; // locked or prefilled
      if(inp.value !== '') continue; // player-entered - do not overwrite
      candidates.push({i,j,idx});
    }
  }
  if(candidates.length === 0){
    document.getElementById('message').innerText = 'No empty editable cells available for a hint.';
    return;
  }
  // choose a random candidate to hint
  const pick = candidates[Math.floor(Math.random()*candidates.length)];
  const val = solution[pick.i][pick.j];
  const inp = inputs[pick.idx];
  inp.value = val;
  inp.disabled = true;
  inp.classList.add('locked');
  hintCount += 1;
  updateHintsDisplay();
  // leave timer running
  document.getElementById('message').innerText = '';
}

function saveScore(){
  const nameEl = document.getElementById('player-name');
  const difficulty = (document.getElementById('difficulty')||{}).value || '';
  const name = (nameEl && nameEl.value.trim()) || 'Anonymous';
  const entry = { name, time: elapsedSeconds, difficulty, hints: hintCount, ts: Date.now() };
  const key = 'sudoku_leaderboard_v1';
  let board = [];
  try{ board = JSON.parse(localStorage.getItem(key) || '[]'); }catch(e){ board = []; }
  board.push(entry);
  board.sort((a,b)=>a.time - b.time);
  board = board.slice(0,10);
  localStorage.setItem(key, JSON.stringify(board));
  renderLeaderboard();
}

function renderLeaderboard(){
  const key = 'sudoku_leaderboard_v1';
  let board = [];
  try{ board = JSON.parse(localStorage.getItem(key) || '[]'); }catch(e){ board = []; }
  const list = document.getElementById('leaderboard-list');
  if(!list) return;
  list.innerHTML = '';
  for(const item of board){
    const li = document.createElement('li');
    li.innerText = `${item.name} — ${formatTime(item.time)} — ${item.difficulty} — hints: ${item.hints}`;
    list.appendChild(li);
  }
}

function highlightSameNumbers(val){
  clearSameNumberHighlights();
  if(!val) return;
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for(const inp of inputs){
    if(inp.value === val && !inp.classList.contains('incorrect')){
      inp.classList.add('same-number');
    }
  }
}

function clearSameNumberHighlights(){
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for(const inp of inputs){ inp.classList.remove('same-number'); }
}

function toggleDarkMode(){
  const on = document.body.classList.toggle('dark');
  document.getElementById('dark-toggle').setAttribute('aria-pressed', String(on));
  try{ localStorage.setItem('sudoku_dark_v1', JSON.stringify(on)); }catch(e){}
}

function restoreDarkMode(){
  try{ const val = JSON.parse(localStorage.getItem('sudoku_dark_v1')); if(val) document.body.classList.add('dark'); }catch(e){}
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  const hintBtn = document.getElementById('hint-button');
  if(hintBtn) hintBtn.addEventListener('click', useHint);
  const darkBtn = document.getElementById('dark-toggle');
  if(darkBtn) darkBtn.addEventListener('click', toggleDarkMode);
  // restore UI state from localStorage
  restoreDarkMode();
  renderLeaderboard();
  updateHintsDisplay();
  // initialize
  newGame();
});