_ROWS = 10
_COLUMNS = 5
_INTERVAL = 0.3
_BLANK = "  "
_BLOCK = "\u2588\u2588"


import os, sys, time, keyboard
from IPython.display import clear_output


def build_clean_grid():
    """Reset the tetris grid to empty."""
    return [["  " for i in range(_ROWS)] for i in range(_COLUMNS)]
    

def redraw(grid):
    """Clear the output and show the grid."""

    # If running in kernel notebook, clear notebook cell, else use cls if run in terminal
    if "ipykernel" in sys.modules:
        clear_output(wait=True)
    else:
        os.system("cls" if os.name == "nt" else "clear")
        
    display_grid(grid)

def move_block(grid, col, row, step):
    """Try to move the block sideways. Return the block's column after the move."""
    new_col = col + step

    # Safety check to stop block from moving past col 0 and 4
    if 0 <= new_col < _COLUMNS and grid[new_col][row] == _BLANK:
        grid[col][row] = _BLANK
        grid[new_col][row] = _BLOCK
        redraw(grid)
        return new_col

    # This return (and the previous one) let the caller know the block has moved
    return col


def display_grid(grid):
    """Display the current state of the tetris grid "vertically" up the screen. Remember: by default,
    the grid dispays across the screen, row-wise (which, usually, isn't what we want here)."""
    the_columns = tuple(range(0, _COLUMNS))
    the_rows = tuple(range(0, _ROWS))
    for r in the_rows:
        print("|", sep="", end="")
        for c in the_columns:
            print(grid[c][r], "|", sep="", end="")
        print()


def show_dropping_block(grid, column_number):
    """Given a grid and a column to drop into, simulate a visual drop of a box."""

    # Tracks falling INSIDE the function so moving and falling apply to the same block at the same time
    col = column_number
    row = 0
    grid[col][row] = _BLOCK
    redraw(grid)

    while True:
        # Checks the keys five times between each one-row drop
        for index in range(5):
            time.sleep(_INTERVAL / 5)

            if keyboard.is_pressed('right'):
                col = move_block(grid, col, row, +1)
            elif keyboard.is_pressed('left'):
                col = move_block(grid, col, row, -1)

        # Checks if landed on bottom row, ELSE IF landed on block
        if row == _ROWS - 1:
            return grid
        elif grid[col][row + 1] == _BLOCK:
            return grid
        
        # Otherwise continue falling for one
        grid[col][row] = _BLANK
        row += 1
        grid[col][row] = _BLOCK
        redraw(grid)