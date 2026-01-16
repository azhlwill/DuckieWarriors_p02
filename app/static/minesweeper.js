// TNPG: DuckieWarriors
// Roster: Cody, James, William
// Description: Minesweeper game logic

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
            row.push({ isMine: false, revealed: false, neighborCount: 0 });
        }
        board.push(row);
    }
    placeMines();
    countNeighbors();
    drawGrid();
}

function placeMines() {
    let mines = 0;
    while (mines < totalMines) {
        let r = Math.floor(Math.random() * rows);
        let c = Math.floor(Math.random() * cols);
        if (!board[r][c].isMine) {
            board[r][c].isMine = true;
            mines++;
        }
    }
}

function countNeighbors() {
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (board[r][c].isMine) continue;
            let count = 0;
            for (let i = -1; i <= 1; i++) {
                for (let j = -1; j <= 1; j++) {
                    let nr = r + i, nc = c + j;
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && board[nr][nc].isMine) count++;
                }
            }
            board[r][c].neighborCount = count;
        }
    }
}

function clickCell(r, c) {
    if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c].revealed) return;
    const cell = board[r][c];
    cell.revealed = true;
    const cellDiv = document.getElementById(`cell-${r}-${c}`);
    cellDiv.classList.add("bg-orange-100");

    if (cell.isMine) {
        cellDiv.classList.add("bg-red-500");
        cellDiv.innerText = "💣";
        alert("Burnt the food! (Game Over)");
        initGame();
    } else {
        if (cell.neighborCount > 0) {
            cellDiv.innerText = cell.neighborCount;
            cellDiv.classList.add("text-orange-800", "font-bold");
        } else {
            for (let i = -1; i <= 1; i++) {
                for (let j = -1; j <= 1; j++) clickCell(r + i, c + j);
            }
        }
        checkWin();
    }
}

function checkWin() {
    let revealedCount = 0;
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (board[r][c].revealed) revealedCount++;
        }
    }
    if (revealedCount === (rows * cols) - totalMines) {
        alert("Kitchen Cleaned! Unlocking Recipe...");
        window.location.href = "/unlock_recipe"; 
    }
}

function drawGrid() {
    for (let r = 0; r < rows; r++) {
        const rowDiv = document.createElement("div");
        rowDiv.className = "flex justify-center";
        for (let c = 0; c < cols; c++) {
            const cell = document.createElement("div");
            cell.id = `cell-${r}-${c}`;
            cell.className = "w-12 h-12 border border-orange-300 bg-white flex items-center justify-center cursor-pointer hover:bg-orange-50 text-lg transition-colors duration-200";
            cell.addEventListener("click", () => clickCell(r, c));
            rowDiv.appendChild(cell);
        }
        grid.appendChild(rowDiv);
    }
}

initGame();