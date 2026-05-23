from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)

clients = {}

TIMEOUT = 10  # secondes sans ping = déconnecté

# 🧹 nettoyage automatique
def cleaner():
    while True:
        now = time.time()
        to_remove = []

        for cid, data in clients.items():
            if now - data["last_seen"] > TIMEOUT:
                to_remove.append(cid)

        for cid in to_remove:
            del clients[cid]

        time.sleep(5)

@app.route("/")
def home():
    return "OK"

# 🔌 ping client
@app.route("/ping", methods=["POST"])
def ping():
    data = request.json
    cid = data["client_id"]

    clients[cid] = {
        "last_seen": time.time()
    }

    return jsonify({"status": "ok"})

@app.route("/clients")
def get_clients():
    return jsonify(list(clients.keys()))

threading.Thread(target=cleaner, daemon=True).start()
