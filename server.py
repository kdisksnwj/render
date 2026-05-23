from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

clients = {}
logs = []

@app.route("/")
def home():
    return jsonify({"status": "online"})

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()

    hostname = data.get("hostname", "unknown")

    clients[hostname] = {
        "user": data.get("user", "unknown"),
        "hostname": hostname,
        "os": data.get("os", "unknown"),
        "last_seen": datetime.utcnow().isoformat()
    }

    logs.append({
        "time": datetime.utcnow().isoformat(),
        "user": data.get("user", "unknown"),
        "hostname": hostname,
        "message": data.get("message", "")
    })

    return jsonify({"status": "ok"})

@app.route("/clients")
def get_clients():
    return jsonify(list(clients.values()))

@app.route("/logs")
def get_logs():
    return jsonify(logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
