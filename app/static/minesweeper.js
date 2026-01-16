// TNPG: DuckieWarriors
// Roster: Cody, James, William

const grid = document.getElementById("gameBoard");
const rows = 8;
const cols = 8;
const totalMines = 10;
let board = [];

function initGame() {
    grid.innerHTML = "";
    board = [];

    for (let r = 0; r < rows; r++) {
        let row = [];
        for (let c = 0; c < cols; c++) {
            row.push({
                mine: false,
                revealed: false,
                flagged: false,
                count: 0
            });
        }
        board.push(row);
    }

    placeMines();
    countNeighbors();
    drawGrid();
}

function placeMines() {
    let placed = 0;
    while (placed < totalMines) {
        let r = Math.floor(Math.random() * rows);
        let c = Math.floor(Math.random() * cols);
        if (!board[r][c].mine) {
            board[r][c].mine = true;
            placed++;
        }
    }
}

function countNeighbors() {
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (board[r][c].mine) continue;
            let count = 0;
            for (let i = -1; i <= 1; i++) {
                for (let j = -1; j <= 1; j++) {
                    let nr = r + i, nc = c + j;
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
                        if (board[nr][nc].mine) count++;
                    }
                }
            }
            board[r][c].count = count;
        }
    }
}

function clickCell(r, c) {
    if (r < 0 || c < 0 || r >= rows || c >= cols) return;
    if (board[r][c].revealed || board[r][c].flagged) return;

    board[r][c].revealed = true;
    const cell = document.getElementById(`cell-${r}-${c}`);
    cell.classList.add("bg-orange-100");

    if (board[r][c].mine) {
        cell.textContent = "X";
        alert("Game Over!");
        initGame();
        return;
    }

    if (board[r][c].count > 0) {
        cell.textContent = board[r][c].count;
    } else {
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j++) {
                clickCell(r + i, c + j);
            }
        }
    }

    checkWin();
}

function toggleFlag(r, c) {
    if (board[r][c].revealed) return;

    const cell = board[r][c];
    const cellDiv = document.getElementById(`cell-${r}-${c}`);

    cell.flagged = !cell.flagged;

    if (cell.flagged) {
        cellDiv.textContent = "F";
        cellDiv.classList.add("bg-yellow-200", "font-bold");
    } else {
        cellDiv.textContent = "";
        cellDiv.classList.remove("bg-yellow-200", "font-bold");
    }
}

function checkWin() {
    let revealed = 0;
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (board[r][c].revealed) revealed++;
        }
    }

    if (revealed === rows * cols - totalMines) {
        window.location.href = "/unlock_recipe";
    }
}

function drawGrid() {
    for (let r = 0; r < rows; r++) {
        const rowDiv = document.createElement("div");
        rowDiv.className = "flex";

        for (let c = 0; c < cols; c++) {
            const cell = document.createElement("div");
            cell.id = `cell-${r}-${c}`;
            cell.className =
                "w-12 h-12 border flex items-center justify-center cursor-pointer select-none";

            cell.onclick = () => clickCell(r, c);

            cell.oncontextmenu = (e) => {
                e.preventDefault();
                toggleFlag(r, c);
            };

            rowDiv.appendChild(cell);
        }
        grid.appendChild(rowDiv);
    }
}

initGame();
