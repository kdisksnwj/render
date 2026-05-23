from flask import Flask, request, jsonify

app = Flask(__name__)

logs = []

@app.route("/message", methods=["POST"])
def message():
    data = request.get_json()

    entry = {
        "user": data.get("user"),
        "message": data.get("message")
    }

    logs.append(entry)

    return jsonify({"status": "ok"})

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(logs)
