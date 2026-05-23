from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Serveur OK"

@app.route("/data", methods=["POST"])
def data():
    content = request.json
    return jsonify({
        "message": "Reçu",
        "data": content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
