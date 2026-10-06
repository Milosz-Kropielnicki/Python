import time, random, keyboard
import tetrisplay, importlib

def Start():
    grid = tetrisplay.build_clean_grid()
    return grid

def GameLoop(grid):
    importlib.reload(tetrisplay)

    while True:
        col = random.randint(0, tetrisplay._COLUMNS - 1)
        
        if grid[col][0] == tetrisplay._BLOCK:
            print("Game over!")
            return grid

        grid = tetrisplay.show_dropping_block(grid, col)

def Redraw():
    clear_output(wait=True)

    tetrisplay.display_grid(grid)

if __name__ == "__main__":
    grid = Start()
    GameLoop(grid)