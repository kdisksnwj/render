from flask import Flask, request, jsonify

app = Flask(__name__)

logs = []

@app.route("/")
def home():
    return "ONLINE"

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()

    logs.append({
        "user": data.get("user", "unknown"),
        "message": data.get("message", ""),
        "ip": request.remote_addr
    })

    return jsonify({"status": "ok"})

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
