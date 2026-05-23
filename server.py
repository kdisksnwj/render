from flask import Flask, request, jsonify
import time

app = Flask(__name__)

clients = {}        # client_id -> last_seen
messages = {}       # client_id -> list messages

# 🔌 ping client (pour apparaître dans la liste)
@app.route("/ping", methods=["POST"])
def ping():
    cid = request.json["client_id"]

    clients[cid] = time.time()

    if cid not in messages:
        messages[cid] = []

    return {"ok": True}

# 👥 liste clients
@app.route("/clients")
def get_clients():
    return jsonify(list(clients.keys()))

# ✉️ envoyer message à un client
@app.route("/send", methods=["POST"])
def send():
    data = request.json
    cid = data["client_id"]
    msg = data["message"]

    if cid not in messages:
        messages[cid] = []

    messages[cid].append({
        "msg": msg,
        "time": time.strftime("%H:%M:%S")
    })

    return {"ok": True}

# 📥 client récupère ses messages
@app.route("/receive", methods=["POST"])
def receive():
    cid = request.json["client_id"]

    msgs = messages.get(cid, [])
    messages[cid] = []  # vider après lecture

    return jsonify(msgs)
