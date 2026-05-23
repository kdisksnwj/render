from flask import Flask, request, jsonify
import time

app = Flask(__name__)

logs = []
clients = []
client_counter = 0

@app.route("/")
def home():
    return "OK"

@app.route("/message", methods=["POST"])
def message():
    global client_counter

    data = request.json
    client_id = data.get("client_id")

    # nouveau client
    if client_id not in clients:
        clients.append(client_id)

    logs.append({
        "client": client_id,
        "message": data.get("message"),
        "time": time.strftime("%H:%M:%S")
    })

    return jsonify({"reponse": data.get("message", "")})

@app.route("/logs")
def get_logs():
    return jsonify(logs[-50:])

@app.route("/clients")
def get_clients():
    return jsonify(clients)
