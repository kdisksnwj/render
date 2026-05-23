from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime

app = Flask(__name__, static_folder="static")

clients = {}
messages = {}

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()

    hostname = data.get("hostname")

    clients[hostname] = {
        "user": data.get("user"),
        "hostname": hostname,
        "os": data.get("os"),
        "last_seen": datetime.utcnow().isoformat()
    }

    messages.setdefault(hostname, []).append({
        "time": datetime.utcnow().isoformat(),
        "message": data.get("message")
    })

    return jsonify({"ok": True})

@app.route("/clients")
def get_clients():
    return jsonify(list(clients.values()))

@app.route("/messages/<client>")
def get_messages(client):
    return jsonify(messages.get(client, []))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
