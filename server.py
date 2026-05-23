from flask import Flask, request, jsonify

app = Flask(__name__)

latest_command = None
last_response = None

@app.route("/")
def home():
    return "Server online"

# envoyer une commande depuis GUI
@app.route("/send", methods=["POST"])
def send():
    global latest_command
    data = request.json
    latest_command = data.get("cmd")
    return jsonify({"status": "ok"})

# client récupère commande
@app.route("/get", methods=["GET"])
def get():
    return jsonify({"cmd": latest_command})

# client envoie réponse
@app.route("/response", methods=["POST"])
def response():
    global last_response
    last_response = request.json.get("result")
    return jsonify({"status": "saved"})

# GUI récupère réponse
@app.route("/result", methods=["GET"])
def result():
    return jsonify({"result": last_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
