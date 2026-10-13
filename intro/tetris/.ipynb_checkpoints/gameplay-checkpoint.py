import time, random, keyboard
import tetrisplay, importlib
from datetime import timedelta, datetime

# Points for each scoring event
_POINTS_PER_BLOCK = 1
_POINTS_PER_ROW = 3
_POINTS_PER_MINUTE = 1
_POINTS_PER_HOUR = 5

_CLASSIC_CELLS = 20 * 10

def Start():
    print("Please input Row and column values to use:\n")
    playerRows = int(input("Rows: "))
    playerColumns = int(input("Columns: "))
    
    grid = tetrisplay.build_clean_grid(playerRows, playerColumns)
    return grid

def CalculateScore(grid, blocksLanded, rowsCompleted, timeElapsed):
    """Work out the score."""

    totalSeconds = int(timeElapsed.total_seconds())
    minutes = totalSeconds
    hours = totalSeconds

    points = (blocksLanded * _POINTS_PER_BLOCK + rowsCompleted * _POINTS_PER_ROW + minutes * _POINTS_PER_MINUTE + hours * _POINTS_PER_HOUR)

    cells = len(grid) * len(grid[0])
    multiplier = cells / _CLASSIC_CELLS

    return round(points * multiplier)

def GameLoop(grid):
    importlib.reload(tetrisplay)

    startTime = datetime.now()
    blocksLanded = 0
    rowsCompleted = 0
    
    while True:
        col = random.randint(0, len(grid) - 1)
        
        if grid[col][0] != tetrisplay._BLANK:
            timeElapsed = datetime.now() - startTime
            timeElapsed = timedelta(seconds=int(timeElapsed.total_seconds()))
            score = CalculateScore(grid, blocksLanded, rowsCompleted, timeElapsed)
            
            print("Game over!")
            username = input("Username: ")
            print(f"User {username} survived for {timeElapsed}")
            print(f"Score: {score}")
            return grid

        grid, rowsCleared = tetrisplay.show_dropping_block(grid, col)
        blocksLanded += 1
        rowsCompleted += rowsCleared

def Redraw():
    clear_output(wait=True)

    tetrisplay.display_grid(grid)

if __name__ == "__main__":
    grid = Start()
    GameLoop(grid)