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

    hostname = data.get("hostname", "unknown")

    # clients online
    clients[hostname] = {
        "user": data.get("user", "unknown"),
        "hostname": hostname,
        "os": data.get("os", "unknown"),
        "last_seen": datetime.utcnow().isoformat()
    }

    # messages per client
    messages.setdefault(hostname, []).append({
        "time": datetime.utcnow().isoformat(),
        "user": data.get("user", "unknown"),
        "message": data.get("message", "")
    })

    return jsonify({"ok": True})

@app.route("/clients")
def get_clients():
    return jsonify(list(clients.values()))

@app.route("/messages/<hostname>")
def get_messages(hostname):
    return jsonify(messages.get(hostname, []))

# optional global logs
@app.route("/logs")
def logs():
    all_logs = []
    for host, msgs in messages.items():
        for m in msgs:
            all_logs.append({
                "hostname": host,
                "time": m["time"],
                "user": m["user"],
                "message": m["message"]
            })
    return jsonify(all_logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
