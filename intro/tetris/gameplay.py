import time, random, keyboard
import tetrisplay, importlib

def Start():
    print("Please input Row and column values to use:\n")
    playerRows = int(input("Rows: "))
    playerColumns = int(input("Columns: "))
    
    grid = tetrisplay.build_clean_grid(playerRows, playerColumns)
    return grid

def GameLoop(grid):
    importlib.reload(tetrisplay)

    while True:
        col = random.randint(0, len(grid) - 1)
        
        if grid[col][0] != tetrisplay._BLANK:
            print("Game over!")
            return grid

        grid = tetrisplay.show_dropping_block(grid, col)

def Redraw():
    clear_output(wait=True)

    tetrisplay.display_grid(grid)

if __name__ == "__main__":
    grid = Start()
    GameLoop(grid)