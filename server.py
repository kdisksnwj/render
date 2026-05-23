from flask import Flask, request, jsonify
import time

app = Flask(__name__)

clients = {}     # client_id -> last_seen
messages = {}    # client_id -> list

TIMEOUT = 8

# 🔌 heartbeat
@app.route("/ping", methods=["POST"])
def ping():
    cid = request.json["client_id"]
    clients[cid] = time.time()

    if cid not in messages:
        messages[cid] = []

    return {"ok": True}

# 👥 clients + statut
@app.route("/clients")
def get_clients():
    now = time.time()

    result = []
    for cid, last in clients.items():
        status = "connected" if now - last < TIMEOUT else "not connected"
        result.append({"id": cid, "status": status})

    return jsonify(result)

# ✉️ envoyer message
@app.route("/send", methods=["POST"])
def send():
    cid = request.json["client_id"]
    msg = request.json["message"]

    if cid not in messages:
        messages[cid] = []

    messages[cid].append({
        "msg": msg,
        "time": time.strftime("%H:%M:%S")
    })

    return {"ok": True}

# 📥 recevoir messages
@app.route("/receive", methods=["POST"])
def receive():
    cid = request.json["client_id"]

    msgs = messages.get(cid, [])
    messages[cid] = []

    return jsonify(msgs)
