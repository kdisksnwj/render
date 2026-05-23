from flask import Flask, request, jsonify
import time

app = Flask(__name__)

clients = {}

@app.route("/")
def home():
    return "OK"

# 🔌 connexion client
@app.route("/connect", methods=["POST"])
def connect():
    data = request.json
    client_id = data.get("client_id")

    clients[client_id] = {
        "last_seen": time.time()
    }

    return jsonify({"status": "connected"})

# 💬 message
@app.route("/message", methods=["POST"])
def message():
    data = request.json
    client_id = data.get("client_id")
    msg = data.get("message")

    return jsonify({
        "from": client_id,
        "message": msg
    })

# 👥 liste clients connectés
@app.route("/clients")
def get_clients():
    return jsonify(list(clients.keys()))
