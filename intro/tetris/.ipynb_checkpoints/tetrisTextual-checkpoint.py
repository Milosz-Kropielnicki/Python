from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Static, Footer, Header

class GridLayout(App):
    CSS_PATH = "Grid_Layout.tcss"

    def compose(self) -> ComposeResult:
        yield Static("One", classes="box")
        yield Static("Two", classes="box")
        yield Static("Three", classes="box")
        yield Static("Four", classes="box")
        yield Static("Five", classes="box")
        yield Static("Six", classes="box")

class TetrisApp(App):
    """A Textual app to manage tetris."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""

        self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")

if __name__ == "__main__":
    app = TetrisApp()
    app.run()