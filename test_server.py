from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from ecosystem import apply_building_choice, reset_game_state, serialize_game_state


ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
GAME_STATE = reset_game_state()


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/style.css")
def styles():
    return send_from_directory(ROOT, "style.css")


@app.get("/script.js")
def script():
    return send_from_directory(ROOT, "script.js")


@app.get("/images/<path:filename>")
def images(filename):
    return send_from_directory(ROOT / "images", filename)


@app.get("/api/game")
def get_game():
    return jsonify(serialize_game_state(GAME_STATE))


@app.post("/api/game/reset")
def reset_game():
    global GAME_STATE
    GAME_STATE = reset_game_state()
    return jsonify({"message": "New game started.", "state": serialize_game_state(GAME_STATE)})


@app.post("/api/game/choose")
def choose_building():
    payload = request.get_json(silent=True) or {}
    building = payload.get("building", "")
    success, message = apply_building_choice(GAME_STATE, building)
    return jsonify(
        {
            "success": success,
            "message": message,
            "state": serialize_game_state(GAME_STATE),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
