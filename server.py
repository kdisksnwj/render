from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

clients = {}
messages = {}
blocked = set()

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

    # ❌ BLOCKED CLIENT
    if hostname in blocked:
        return jsonify({"blocked": True})

    # 🟢 UPDATE CLIENT STATUS
    clients[hostname] = {
        "user": data.get("user", "unknown"),
        "hostname": hostname,
        "os": data.get("os", "unknown"),
        "last_seen": datetime.utcnow().isoformat()
    }

    # 💬 STORE ONLY REAL MESSAGES
    if message and message != "heartbeat":
        messages.setdefault(hostname, []).append({
            "time": datetime.utcnow().isoformat(),
            "user": data.get("user", "unknown"),
            "message": message
        })

    return jsonify({"ok": True})


# ---------------- CLIENT LIST ----------------
@app.route("/clients")
def get_clients():
    return jsonify(list(clients.values()))


# ---------------- MESSAGES ----------------
@app.route("/messages/<hostname>")
def get_messages(hostname):
    return jsonify(messages.get(hostname, []))


# ---------------- STATUS (IMPORTANT FIX) ----------------
@app.route("/status/<hostname>")
def status(hostname):
    if hostname in blocked:
        return jsonify({"status": "down"})

    client = clients.get(hostname)

    if not client:
        return jsonify({"status": "offline"})

    last = datetime.fromisoformat(client["last_seen"])
    now = datetime.utcnow()

    # 🧠 anti fake offline (Render lag fix)
    if now - last > timedelta(seconds=30):
        return jsonify({"status": "offline"})

    return jsonify({"status": "up"})


# ---------------- DISCONNECT ----------------
@app.route("/disconnect/<hostname>")
def disconnect(hostname):
    blocked.add(hostname)
    return jsonify({"status": "disconnected"})


# ---------------- RECONNECT ----------------
@app.route("/reconnect/<hostname>")
def reconnect(hostname):
    blocked.discard(hostname)
    return jsonify({"status": "reconnected"})


# ---------------- LOGS ----------------
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
