from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

GITHUB_TOKEN = "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"
REPO = "kdisksnwj/crotte"

@app.route("/send", methods=["POST"])
def send():
    data = request.json

    # envoyer vers GitHub
    content = base64.b64encode(str(data).encode()).decode()

    url = f"https://api.github.com/repos/{REPO}/contents/data.txt"

    payload = {
        "message": "update from render",
        "content": content
    }

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    r = requests.put(url, json=payload, headers=headers)

    return jsonify({"render": "ok", "github": r.status_code})
