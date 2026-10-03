// Function to dynamically create a 10x10 grid of cells for the game board

function createGameBoard(containerId, cellClass) {
    const container = document.getElementById(containerId);

    // Return if ID does not exist
    if (!container){
        return;
    }

    for (let row = 0; row < 10; row++) {
        for (let col = 0; col < 10; col++) {
            const cell = document.createElement('div');
            cell.classList.add(cellClass);
            cell.id = `${cellClass}-${row}-${col}`;
            cell.value = `${row}${col}`;
            container.appendChild(cell);
        }
    }
}

// Immediately create the game board when the script is loaded
createGameBoard('game-container', 'cell');
createGameBoard('ai-board-container', 'ai-cell');
createGameBoard('player-board-container', 'player-cell');