from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "online"})

@app.route("/message", methods=["POST"])
def message():
    data = request.get_json()

    user = data.get("user")
    msg = data.get("message")

    print(f"[RECU] {user}: {msg}")

    response = f"Salut {user}, j'ai reçu: {msg}"

    return jsonify({
        "response": response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
