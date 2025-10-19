# app.py
from datetime import datetime
from random import uniform
from threading import Lock
import time

from flask import Flask, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO

# ---- Global state (must be defined before use)
thread = None
thread_lock = Lock()

# ---- App / Socket.IO setup
app = Flask(__name__)
CORS(app)  # allow cross-origin during development

# Choose a simple, reliable async mode for local dev
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def on_connect():
    global thread
    print(f"Client connected: {request.sid}")
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    socketio.emit("Connected", {"message": "Welcome!"}, to=request.sid)


@socketio.on("disconnect")
def on_disconnect():
    print(f"Client disconnected: {request.sid}")


def background_thread():
    print("Starting background thread for random value generation")
    # Start within [16, 26]
    current_value = round(uniform(16.0, 26.0), 2)

    while True:
        # Random walk in [-1, +1], clamp to [16, 26]
        change = round(uniform(-1.0, 1.0), 2)
        current_value = max(16.0, min(26.0, current_value + change))

        current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f"Generated value: {current_value} at {current_time}")

        socketio.emit("updateValue", {"value": current_value, "time": current_time})

        # Use socketio.sleep for cooperative yielding with the selected async mode
        socketio.sleep(1)


if __name__ == "__main__":
    # The dev server is fine for local testing; don't use in production
    socketio.run(app, debug=True, host="127.0.0.1", port=5000, allow_unsafe_werkzeug=True)
