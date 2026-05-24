from flask import Flask, request, jsonify

app = Flask(__name__)

data_store = []

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    data_store.append(data)
    return jsonify({"status": "ok", "received": data})

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(data_store)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
