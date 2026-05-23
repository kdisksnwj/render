from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Serveur Render en ligne"

@app.route("/message", methods=["POST"])
def message():
    data = request.json
    return jsonify({"reponse": data.get("message", "")})
