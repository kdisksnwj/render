from flask import Flask, request, jsonify
import os

app = Flask(__name__)

data_store = []

@app.route("/")
def home():
    return "API online"

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    data_store.append(data)
    return jsonify({"status": "ok"})

@app.route("/data", methods=["GET"])
def data():
    return jsonify(data_store)

# IMPORTANT POUR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
