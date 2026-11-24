import random
import time

BLANK = "blank"
COLORS = ["red", "blue", "yellow", "green", "white", "orange"]

# Points for each scoring event (same as tetris/gameplay.py)
POINTS_PER_BLOCK = 1
POINTS_PER_ROW = 3
POINTS_PER_MINUTE = 1
POINTS_PER_HOUR = 5
ROW_BONUS = 50   # live on-screen score per completed row
CLASSIC_CELLS = 20 * 10


def new_game(rows, cols):
    """Return a fresh game state.
    grid[col][row], as in the terminal version."""
    state = {
        "grid": [[BLANK] * rows for _ in range(cols)],
        "col": 0,
        "row": 0,
        "blocks": 0,
        "rows_done": 0,
        "points": 0,
        "start": time.time(),
        "over": False,
        "elapsed": 0,
        "score": None,
        "user": None,
    }
    spawn(state)
    return state


def spawn(state):
    """Start a new block at the top of a random column; game over if it is occupied."""
    grid = state["grid"]
    col = random.randint(0, len(grid) - 1)
    if grid[col][0] != BLANK:
        state["over"] = True
        state["elapsed"] = int(time.time() - state["start"])
        state["score"] = score(state)
        return
    state["col"], state["row"] = col, 0
    grid[col][0] = random.choice(COLORS)


def full_row(grid):
    """If the bottom row is full, remove it and shift everything down. Returns 1 or 0."""
    bottom = len(grid[0]) - 1
    if all(column[bottom] != BLANK for column in grid):
        for column in grid:
            del column[bottom]
            column.insert(0, BLANK)
        return 1
    return 0


def tick(state):
    """One step of gravity."""
    if state["over"]:
        return
    grid, col, row = state["grid"], state["col"], state["row"]
    if row == len(grid[0]) - 1 or grid[col][row + 1] != BLANK:
        state["blocks"] += 1
        cleared = full_row(grid)
        state["rows_done"] += cleared
        state["points"] += cleared * ROW_BONUS
        spawn(state)
        return
    grid[col][row + 1] = grid[col][row]
    grid[col][row] = BLANK
    state["row"] += 1


def move(state, step):
    """Try to move the falling block sideways."""
    if state["over"]:
        return
    grid, col, row = state["grid"], state["col"], state["row"]
    new_col = col + step
    if 0 <= new_col < len(grid) and grid[new_col][row] == BLANK:
        grid[new_col][row] = grid[col][row]
        grid[col][row] = BLANK
        state["col"] = new_col


def score(state):
    total_seconds = state["elapsed"]
    minutes = total_seconds // 60
    hours = total_seconds // 3600
    points = (
        state["blocks"] * POINTS_PER_BLOCK
        + state["rows_done"] * POINTS_PER_ROW
        + minutes * POINTS_PER_MINUTE
        + hours * POINTS_PER_HOUR
    )
    cells = len(state["grid"]) * len(state["grid"][0])
    return round(points * cells / CLASSIC_CELLS)
