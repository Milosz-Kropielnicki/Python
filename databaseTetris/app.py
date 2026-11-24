import os
import threading

from flask import Flask, render_template, session, request
from pynput.keyboard import Key, Listener

import game

app = Flask(__name__)
app.secret_key = "fhdsjhgkjsadghhgdshdgdsngjdsfnvjdf njdfnvngdfkgjndfgj"

DEFAULT_ROWS = 8
DEFAULT_COLS = 4
MIN_SIZE = 2
MAX_SIZE = 20   # Keeps session cookie under 4KB limit

# pynput listens on the machine running the server, not in the browser, so the
# game lives here (not in the cookie session) where the key thread can reach it.
current = {"state": None}
lock = threading.Lock()


def on_key_press(key):
    """pynput callback: left/right arrows move the falling block."""
    if key not in (Key.left, Key.right):
        return
    with lock:
        state = current["state"]
        if state is not None:
            game.move(state, -1 if key == Key.left else 1)


def start_key_listener():
    listener = Listener(on_press=on_key_press)
    listener.daemon = True
    listener.start()


def read_size(name, default):
    """Read a number from the form, clamped to limit."""
    try:
        value = int(request.form.get(name, default))
    except ValueError:
        value = default
    return max(MIN_SIZE, min(MAX_SIZE, value))


def board_html():
    """The grid, marked to replace the element with id 'board'."""
    state = current["state"]
    grid = state["grid"]
    
    return render_template(
        "board.html",
        grid=grid,
        rowcount=len(grid[0]),
        colcount=len(grid),
        points=state["points"],
        oob=True,
    )


def over_html():
    """Game-over message with username form until a score has been submitted."""
    return render_template("over.html", state=current["state"])


@app.get("/")
@app.get("/showgrid")
def setup():
    return render_template(
        "setup.html",
        rows=DEFAULT_ROWS,
        cols=DEFAULT_COLS,
        min_size=MIN_SIZE,
        max_size=MAX_SIZE
    )

@app.post("/start")
def start():
    rows = read_size("rows", DEFAULT_ROWS)
    cols = read_size("cols", DEFAULT_COLS)
    session["count"] = 0
    with lock:
        current["state"] = game.new_game(rows, cols)
        grid = current["state"]["grid"]
    
    return render_template(
        "grid.html",
        grid=grid,
        rowcount=rows,
        colcount=cols,
        points=0,
        oob=False,
    )

@app.post("/tick")
def gravity():
    with lock:
        state = current["state"]
        
        # Game already ended and the form has been sent
        # Send nothing so the username is not rebuilt every tick
        if state["over"]:
            return ""
        game.tick(state)
        
        # Just ended on the tick
        # Send the board and the game-over form once
        if state["over"]:
            return board_html() + over_html()
        return board_html()


@app.post("/counting")
def maintain_count():
    if current["state"]["over"]:
        return "Time stopped: " + str(session["count"])
    session["count"] = session["count"] + 1
    return "Time is ticking: " + str(session["count"])


@app.post("/score")
def submit_score():
    with lock:
        state = current["state"]
        state["user"] = request.form["username"]
        return render_template("over.html", state=state)


if __name__ == "__main__":
    # The debug reloader runs this file twice; only start the listener in the serving process
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_key_listener()
    app.run(debug=True)
