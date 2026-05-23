from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

clients = {}
messages = {}

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "SERVER ONLINE"

# ---------------- SEND ----------------
@app.route("/send", methods=["POST"])
def send():
    data = request.get_json() or {}

    hostname = data.get("hostname", "unknown")
    message = data.get("message", "")

    # UPDATE CLIENT (always)
    clients[hostname] = {
        "user": data.get("user", "unknown"),
        "hostname": hostname,
        "os": data.get("os", "unknown"),
        "last_seen": datetime.utcnow().isoformat()
    }

    # ONLY STORE REAL MESSAGES (IMPORTANT FIX)
    if message and message != "heartbeat":
        messages.setdefault(hostname, []).append({
            "time": datetime.utcnow().isoformat(),
            "user": data.get("user", "unknown"),
            "message": message
        })

    return jsonify({"ok": True})

# ---------------- CLIENTS ----------------
@app.route("/clients")
def get_clients():
    return jsonify(list(clients.values()))

# ---------------- MESSAGES ----------------
@app.route("/messages/<hostname>")
def get_messages(hostname):
    return jsonify(messages.get(hostname, []))

# ---------------- CLEAN LOGS ----------------
@app.route("/logs")
def logs():
    all_logs = []

    for host, msgs in messages.items():
        for m in msgs:
            if m["message"] == "heartbeat":
                continue

            all_logs.append({
                "hostname": host,
                "time": m["time"],
                "user": m["user"],
                "message": m["message"]
            })

    return jsonify(all_logs)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
