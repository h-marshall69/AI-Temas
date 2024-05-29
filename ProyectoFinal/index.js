indexedDB.html:
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="styles.css">
  <title>Minesweeper</title>
</head>
<body class="col">
  <h1>Minesweeper</h1>
  <p>To start a new game, please enter the desired dimension of the board and the number of bombs.
  <div class="row">
    <h3>Board dimensions:</h3>
    <input id='dimensionsInput' type="number" min="1">
    <button id='playBtn'>Play</button>
  </div>
  <div id="content" class="row">
    <div class="col">
      <div id="game-state" class="col">
        <h2 id="timer"></h2>
        <div class="row">
          Number of unrevealed blocks:
          <h3 id="num-unrevealed-blocks"></h3>
        </div>
        <div class="row">
          Number of bombs left:
          <h3 id="num-bombs-left"></h3>
        </div>
      </div>
      <button id='auto-solve-one-move-btn'>Auto solve one move</button>
      <button id='auto-solve-everything-btn'>Auto solve game</button>
      <div id='board'></div>
    </div>
    <div id="leaderboard" class="col"></div>
  </div>

  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
  <script src="../js/utils.js"></script>
  <script src="../js/models.js"></script>
  <script src="../js/leaderboard.js"></script>
  <script src="../js/minesweeper.js"></script>
  <script src="../js/solver.js"></script>
  <script src="../js/app.js"></script>
  <script src="../js/index.js"></script>
</body>
</html>

utils.js:
/*

Some helpful utility methods.

*/

function runOnAllAdjacentBlocks(row, col, dimension, func) {
  if (row != 0 && col != 0) {
    func(row - 1, col - 1);
  }
  if (row != 0) {
    func(row - 1, col);
  }
  if (col != 0) {
    func(row, col - 1);
  }
  if (row != dimension - 1 && col != dimension - 1) {
    func(row + 1, col + 1);
  }
  if (row != dimension - 1) {
    func(row + 1, col);
  }
  if (col != dimension - 1) {
    func(row, col + 1);
  }
  if (row != 0 && col != dimension - 1) {
    func(row - 1, col + 1);
  }
  if (row != dimension - 1 && col != 0) {
    func(row + 1, col - 1);
  }
}

function forEachCell(matrix, func) {
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[i].length; j++) {
      func(matrix[i][j], i, j);
    }
  }
}

function toMMSS(sec_num) {
  var hours = Math.floor(sec_num / 3600);
  var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
  var seconds = sec_num - (hours * 3600) - (minutes * 60);

  if (minutes < 10) {
    minutes = "0" + minutes;
  }
  if (seconds < 10) {
    seconds = "0" + seconds;
  }
  return minutes+':'+seconds;
}

models.js:
/*

The cell represents a single cell in the minesweeper game

*/

class Cell {
  constructor() {
    this.isBomb = false;
    this.isFlagged = false;
    this.isRevealed = false;
    // Only care about this number if isBomb is false
    this.number = 0;
  }

  reveal() {
    if (!this.isBomb) {
      this.isFlagged = false;
    }
    this.isRevealed = true;
  }
}

leaderboard.js:
class Leaderboard {
  constructor() {
    this.leaderboard = {};
  }

  addWinData(dimension, time) {
    const leaderboardForDimen = this.leaderboard[dimension];
    if (!leaderboardForDimen) {
      this.leaderboard[dimension] = [time];
    } else {
      leaderboardForDimen.push(time);
      leaderboardForDimen.sort();
    }
  }

  getTop10ForDimen(dimension) {
    const leaderboardForDimen = this.leaderboard[dimension];
    if (leaderboardForDimen) {
      return leaderboardForDimen.splice(0, 10);
    }
    return [];
  }
}

minesweeper.js:
/*

Minesweeper class represents the state of a single game board. It initializes
itself according to the provided dimensions and number of bombs (randomly
chooses the bomb locations so that they don't overlap). It contains callbacks
for when a cell gets revealed or flagged so that the game board's internal
state gets updated accordingly.

*/

class Minesweeper {

    constructor(dimension) {
      this.dimension = dimension;
      this.numBombs = Math.floor(dimension * dimension / 7);
      this.won = false;
      this.lost = false;
  
      this.initializeBoard();
    }
  
    initializeBoard() {
      this.createBoard();
  
      const bombs = this.generateBombs();
      for (let i = 0; i < bombs.length; i++) {
        const bomb = bombs[i];
        this.board[bomb[0]][bomb[1]].isBomb = true;
        runOnAllAdjacentBlocks(bomb[0], bomb[1], this.dimension, (row, col) => {
          const cell = this.board[row][col];
          if (!cell.isBomb) {
            cell.number++;
          }
        })
      }
    }
  
    createBoard() {
      this.board = [];
      for (let i = 0; i < this.dimension; i++) {
        const innerArr = [];
        for (let j = 0; j < this.dimension; j++) {
          innerArr.push(new Cell());
        }
        this.board.push(innerArr);
      }
    }
  
    // Array of array, each subarray represents [row, column].
    generateBombs() {
      const bombLocations = [];
      for (var i = 0; i < this.numBombs; i++) {
        let bomb = this.generateRandomBomb();
        while (this.doesBombExist(bombLocations, bomb)) {
          bomb = this.generateRandomBomb();
        }
        bombLocations.push(bomb);
      }
      return bombLocations;
    }
  
    generateRandomBomb() {
      const rowBomb = Math.floor(Math.random() * this.dimension);
      const colBomb = Math.floor(Math.random() * this.dimension);
      return [rowBomb, colBomb];
    }
  
    doesBombExist(bombLocations, bomb) {
      for (let i = 0; i < bombLocations.length; i++) {
        const match = bomb[0] === bombLocations[i][0] && 
          bomb[1] === bombLocations[i][1];
        if (match) {
          return true;
        }
      }
      return false;
    }
  
    onCellClicked(row, col) {
      if (this.won || this.lost) {
        return;
      }
  
      const cell = this.board[row][col];
      if (cell.isBomb) {
        this.handleLoss();
      } else {
        this.revealNonBombCellsAndAdjacent(row, col);
        this.checkWin();
      }
    }
  
    revealNonBombCellsAndAdjacent(row, col) {
      const cell = this.board[row][col];
      if (cell.isRevealed || cell.isBomb) {
        return;
      }
      cell.reveal();
      if (cell.number === 0) {
        runOnAllAdjacentBlocks(row, col, this.dimension, (newRow, newCol) => {
          this.revealNonBombCellsAndAdjacent(newRow, newCol);
        })
      }
    }
  
    handleLoss() {
      this.lost = true;
  
      forEachCell(this.board, cell => {
        if (cell.isBomb) {
          cell.reveal();
        }
      })
    }
  
    checkWin() {
      let hasWon = true;
      forEachCell(this.board, newCell => {
        // Check if there is a cell that is not a bomb and hasn't been revealed.
        if (!newCell.isFlagged && !newCell.isRevealed) {
          hasWon = false;
        }
      })
  
      if (hasWon) {
        this.won = true;
      }
    }
  
    onCellRightClicked(row, col) {
      if (this.won || this.lost) {
        return;
      }
  
      const cell = this.board[row][col];
      if (cell.isRevealed) {
        return;
      }
  
      cell.isFlagged = !cell.isFlagged;
      this.checkWin();
    }
  }

  solver.js:
  /*

Solver bot that tries to generate safe moves for you to make. It will default
to a random move if no safe move is found.

*/

class Solver {
    constructor(minesweeper) {
      this.minesweeper = minesweeper;
    }
  
    // Returns [isLeftClick, row, col]
    getNextMove() {
      const cellToFlag = this.findCellToFlag();
      if (cellToFlag) {
        return [false, cellToFlag[0], cellToFlag[1]];
      }
  
      const cellToClick = this.findCellToClick();
      if (cellToClick) {
        return [true, cellToClick[0], cellToClick[1]];
      }
  
      // All hope is lost, generate a random location to click
      const dimen = this.minesweeper.dimension;
      const row = Math.floor(Math.random() * (dimen - 1));
      const col = Math.floor(Math.random() * (dimen - 1));
      return [true, row, col];
    }
  
    findCellToFlag() {
      const dimen = this.minesweeper.dimension;
  
      // See if there is any cell that we can flag
      let rowToFlag = undefined;
      let colToFlag = undefined;
      forEachCell(this.minesweeper.board, (cell, row, col) => {
        if (cell.isRevealed || cell.isFlagged || (rowToFlag !== undefined)) {
          return;
        }
  
        // A cell can be flagged if there is one neighbor that has bombs
        // that cannot be accounted for otherwise.
        runOnAllAdjacentBlocks(row, col, dimen, (neighborRow, neighborCol) => {
          const neighbor = this.minesweeper.board[neighborRow][neighborCol];
          // probably need to change this structure, technically I can just access
          // neighbor.isBomb or neighbor.number since there is no restrictions here.
          if (neighbor.isRevealed && neighbor.number > 0) {
            let numUnrevealedAroundNeighbor = 0;
            runOnAllAdjacentBlocks(neighborRow, neighborCol, dimen, (i, j) => {
              const neighborOfNeighbor = this.minesweeper.board[i][j];
              if (!neighborOfNeighbor.isRevealed) {
                numUnrevealedAroundNeighbor++;
              }
            });
  
            // If the number of bombs is equal to the number of unrevealed
            // neighbors, then all of the unrevealed neighbors must be bombs.
            if (numUnrevealedAroundNeighbor === neighbor.number) {
              // This must be a bomb
              rowToFlag = row;
              colToFlag = col;
            }
          }
        });
      });
  
      if (rowToFlag !== undefined) {
        return [rowToFlag, colToFlag];
      }
      return undefined;
    }
  
    findCellToClick() {
      const dimen = this.minesweeper.dimension;
  
      let rowToClick = undefined;
      let colToClick = undefined;
      forEachCell(this.minesweeper.board, (cell, row, col) => {
        if (cell.isRevealed || cell.isFlagged || (rowToClick !== undefined)) {
          return;
        }
  
        // A cell can be clicked on if there is one neighbor that has all of its
        // bombs accounted for
        runOnAllAdjacentBlocks(row, col, dimen, (neighborRow, neighborCol) => {
          const neighbor = this.minesweeper.board[neighborRow][neighborCol];
          if (neighbor.isRevealed) {
            let numFlagged = 0;
            runOnAllAdjacentBlocks(neighborRow, neighborCol, dimen, (i, j) => {
              const neighborOfNeighbor = this.minesweeper.board[i][j];
              if (!neighborOfNeighbor.isRevealed && neighborOfNeighbor.isFlagged) {
                numFlagged++;
              }
            });
  
            if (numFlagged === neighbor.number) {
              // All bombs are accounted for
              rowToClick = row;
              colToClick = col;
            }
          }
        });
      });
  
      if (rowToClick !== undefined) {
        return [rowToClick, colToClick];
      }
      return undefined;
    }
  }

  app.js:
  /*

App represents the primary logic for hooking up the various elements
on the page with the appropriate handlers. It contains the initialization
code to start a new game, calls back to the minesweeper class whenever
there is any kind of interaction (such as click), and redraws the game
board whenever anything changes.

*/

class App {

    constructor() {
      this.boardDom = $('#board');
      this.timerDom = $('#timer');
      this.numUnrevealedBlocksDom = $('#num-unrevealed-blocks');
      this.numBombsLeftDom = $('#num-bombs-left');
      this.leaderboardDom = $('#leaderboard');
  
      this.leaderboard = new Leaderboard();
  
      $('#playBtn').on('click', () => {
        const dimensionsInput = $('#dimensionsInput').val();
        if (dimensionsInput < 1) {
          return;
        }
        this.playGame(dimensionsInput);
      })
  
      $('#auto-solve-one-move-btn').on('click', () => {
        this.autoSolveOneMove();
      });
      $('#auto-solve-everything-btn').on('click', () => {
        this.autoSolveGame();
      })
    }
  
    playGame(dimen) {
      this.resetState();
  
      this.minesweeper = new Minesweeper(dimen);
      this.solver = new Solver(this.minesweeper);
      this.drawBoard();
      this.drawLeaderboard();
  
      // Start and render timer
      this.timeElapsed = 0;
      this.timerDom.text(toMMSS(this.timeElapsed));
      this.timer = setInterval(() => {
        this.timeElapsed++;
        this.timerDom.text(toMMSS(this.timeElapsed));
      }, 1000);
    }
  
    resetState() {
      clearInterval(this.timer);
      clearInterval(this.solverTimer);
      this.timer = null;
      this.solverTimer = null;
    }
  
    autoSolveGame() {
      if (!this.solverTimer) {
        this.solverTimer = setInterval(() => {
          this.autoSolveOneMove();
        }, 500);
      }
    }
  
    autoSolveOneMove() {
      const move = this.solver.getNextMove();
      if (move[0]) {
        this.click(move[1], move[2]);
      } else {
        this.rightClick(move[1], move[2]);
      }
    }
  
    drawBoard() {
      console.log("Drawing board");
      this.boardDom.empty();
  
      for (let i = 0; i < this.minesweeper.dimension; i++) {
        const row = $('<div class="row"></div>');
        for (let j = 0; j < this.minesweeper.dimension; j++) {
          row.append(this.makeCell(i, j));
        }
        this.boardDom.append(row);
      }
  
      if (this.minesweeper.won) {
        this.onGameEnded(true);
      } else if (this.minesweeper.lost) {
        this.onGameEnded(false);
      }
  
      let numUnrevealedBlocks = 0;
      let numBombsLeft = this.minesweeper.numBombs;
      forEachCell(this.minesweeper.board, cell => {
        if (!cell.isRevealed) {
          numUnrevealedBlocks++;
        }
        if (cell.isFlagged) {
          numBombsLeft--;
        }
      })
      this.numUnrevealedBlocksDom.text(numUnrevealedBlocks);
      this.numBombsLeftDom.text(numBombsLeft);
    }
  
    makeCell(row, col) {
      const cell = this.minesweeper.board[row][col];
      const div = $('<div class="cell-wrapper"></div>');
      if (cell.isRevealed) {
        if (cell.isBomb) {
          if (cell.isFlagged) {
            div.append($('<img class="flagged"></img>'));
          } else {
            div.append($('<img class="bomb"></img>'));
          }
        } else {
          div.append($('<img class="revealed"></img>'));
  
          if (cell.number > 0) {
            const bombCount = $('<div class="bomb-count"></div>');
            bombCount.text(cell.number);
            div.append(bombCount);
          }
        }
  
      } else if (cell.isFlagged) {
        if (this.minesweeper.lost) {
          div.append($('<img class="misflagged"></img>'));
        } else {
          div.append($('<img class="flagged"></img>'));
        }
      } else {
        div.append($('<img class="cell"></img>'));
      }
  
      div.on('click', () => {
        this.click(row, col);
      });
      div.on('contextmenu', e => {
        e.preventDefault();
        this.rightClick(row, col);
      });
  
      return div;
    }
  
    click(row, col) {
      this.minesweeper.onCellClicked(row, col);
      this.drawBoard(this.minesweeper);
    }
  
    rightClick(row, col) {
      this.minesweeper.onCellRightClicked(row, col);
      this.drawBoard(this.minesweeper);
    }
  
    drawLeaderboard() {
      const dimen = this.minesweeper.dimension;
      const scores = this.leaderboard.getTop10ForDimen(dimen);
      this.leaderboardDom.empty();
  
      const header = $('<h3></h3>');
      header.text("Top scores for " + dimen + "x" + dimen);
      this.leaderboardDom.append(header);
  
      for (let i = 0; i < scores.length; i++) {
        const score = toMMSS(scores[i]);
        const scoreDom = $('<div></div>');
        scoreDom.text(score);
        this.leaderboardDom.append(scoreDom);
      }
    }
  
    onGameEnded(won) {
      let timerText = toMMSS(this.timeElapsed);
      if (won) {
        timerText = "You've won! Time: " + timerText;
        this.leaderboard.addWinData(this.minesweeper.dimension, this.timeElapsed);
      } else {
        timerText = "You've lost. Time: " + timerText;
      }
      this.timerDom.text(timerText);
  
      this.resetState();
      this.drawLeaderboard();
    }
  }

  indexedDB.js:
  /*

Main code that is run when the page gets loaded

*/

const app = new App();


// for testing
app.playGame(10);