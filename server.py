from flask import Flask, request, jsonify
import time

app = Flask(__name__)

connections = []

@app.route("/")
def home():
    return "Serveur en ligne"

@app.route("/message", methods=["POST"])
def message():
    data = request.json

    entry = {
        "message": data.get("message"),
        "time": time.strftime("%H:%M:%S")
    }

    connections.append(entry)

    print("CONNEXION :", entry)

    return jsonify({"reponse": data.get("message")})

@app.route("/logs")
def logs():
    return jsonify(connections)
