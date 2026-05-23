from flask import Flask, request, jsonify
import time

app = Flask(__name__)

clients = set()
logs = []

@app.route("/")
def home():
    return "OK"

@app.route("/message", methods=["POST"])
def message():
    data = request.json
    client_id = data.get("client_id", "unknown")

    clients.add(client_id)

    logs.append({
        "client": client_id,
        "message": data.get("message"),
        "time": time.strftime("%H:%M:%S")
    })

    return jsonify({"ok": True})

@app.route("/clients")
def get_clients():
    return jsonify(list(clients))

@app.route("/logs")
def get_logs():
    return jsonify(logs[-50:])
