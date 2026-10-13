import random
from datetime import datetime, timedelta

from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, Static
from textual.containers import Container, Vertical

import tetrisplay
import gameplay

_COLORS = ["red", "blue", "yellow", "green", "white", "orange"]

class Board(Container):
    """tetris grid via CSS."""

    def __init__(self, columns, rows):
        super().__init__(id="board")
        self.columns = columns
        self.rows = rows

    def compose(self) -> ComposeResult:
        for row in range(self.rows):
            for column in range(self.columns):
                yield Static(classes="cell blank")

    def on_mount(self) -> None:
        self.styles.grid_size_columns = self.columns
        self.border_title = "TETRIS"

    def show(self, grid):
        "Displays the grid."

        cells = self.query(".cell")

        for row in range(self.rows):
            for column in range(self.columns):
                cell = grid[column][row]
                colour = "blank" if cell == tetrisplay._BLANK else cell
                cells[row * self.columns + column].set_classes(["cell", colour])

class TetrisApp(App):
    CSS_PATH = "Grid_Layout.tcss"

    BINDINGS = [
        ("left", "move(-1)", "Left"),
        ("right", "move(1)", "Right"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.blocksLanded = 0
        self.rowsCompleted = 0
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Board(len(self.grid), len(self.grid[0]))
        with Vertical(id="sidebar"):
            yield Static(id="status")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#sidebar").border_title = "Stats" 
        self.startTime = datetime.now()
        self.spawn_block()
        self.timer = self.set_interval(tetrisplay._INTERVAL, self.tick)

    def spawn_block(self):
        """Start a new block at the top of a random column."""

        self.col = random.randint(0, len(self.grid) - 1)
        self.row = 0

        if self.grid[self.col][0] != tetrisplay._BLANK:
            self.game_over()
            return

        self.grid[self.col][self.row] = random.choice(_COLORS)
        self.redraw()

    def tick(self):
        """One step of gravity."""

        if self.row == len(self.grid[0]) - 1 or self.grid[self.col][self.row + 1] != tetrisplay._BLANK:
            self.blocksLanded += 1
            self.rowsCompleted += tetrisplay.full_row(self.grid)
            self.spawn_block()
            return
        block = self.grid[self.col][self.row]
        self.grid[self.col][self.row] = tetrisplay._BLANK
        self.row += 1
        self.grid[self.col][self.row] = block
        self.redraw()

    def action_move(self, step: int) -> None:
        """Replaces keyboard.is_pressed."""

        if self.timer is None:
            return
        self.col = tetrisplay.move_block(self.grid, self.col, self.row, step)
        self.redraw()

    def redraw(self):
        self.query_one(Board).show(self.grid)
        elapsed = timedelta(seconds=int((datetime.now() - self.startTime).total_seconds()))
        self.query_one("#status", Static).update(f"Blocks: {self.blocksLanded} Rows: {self.rowsCompleted} Time: {elapsed}")

    def game_over(self):
        self.timer.stop()
        self.timer = None
        self.elapsed = timedelta(seconds=int((datetime.now() - self.startTime).total_seconds()))
        self.query_one("#sidebar").mount(Input(placeholder="Username"))
        self.query_one("#status", Static).update("Game Over! Enter your username:")
        self.mount(Input(placeholder="Username"), before=self.query_one(Footer))
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        score = gameplay.CalculateScore(self.grid, self.blocksLanded, self.rowsCompleted, self.elapsed)
        event.input.remove()
        self.query_one("#status", Static).update(f"User {event.value} survived for {self.elapsed}\nScore: {score}\n\nPress Ctrl+Q to quit")

    def action_toggle_dark(self) -> None:
        self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")

if __name__ == "__main__":
    grid = gameplay.Start()
    TetrisApp(grid).run()