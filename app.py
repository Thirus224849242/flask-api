from flask import Flask, jsonify, request
import os
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = os.environ.get("DATA_FILE", "/data/notes.json")

def load_notes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_notes(notes):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "SIT323 Cloud-Native API", "version": "1.0.0"})

@app.route("/notes", methods=["GET"])
def get_notes():
    notes = load_notes()
    return jsonify({"notes": notes, "count": len(notes)})

@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    if not data or "content" not in data:
        return jsonify({"error": "content field is required"}), 400
    notes = load_notes()
    note = {"id": len(notes) + 1, "content": data["content"], "created_at": datetime.utcnow().isoformat()}
    notes.append(note)
    save_notes(notes)
    return jsonify(note), 201

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    notes = load_notes()
    notes = [n for n in notes if n["id"] != note_id]
    save_notes(notes)
    return jsonify({"message": f"Note {note_id} deleted"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
