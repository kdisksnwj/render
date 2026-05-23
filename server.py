from flask import Flask, request, jsonify
import time

app = Flask(__name__)

logs = []

@app.route("/")
def home():
    return "OK"

@app.route("/message", methods=["POST"])
def message():
    data = request.json

    logs.append({
        "message": data.get("message"),
        "time": time.strftime("%H:%M:%S")
    })

    return jsonify({"status": "ok"})

@app.route("/logs")
def get_logs():
    return jsonify(logs[-50:])  # derniers logs
