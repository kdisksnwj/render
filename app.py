from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = "kdisksnwj/crotte"

@app.route("/send", methods=["POST"])
def send():
    data = request.json

    content = base64.b64encode(str(data).encode()).decode()

    url = f"https://api.github.com/repos/{REPO}/contents/data.txt"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # récupérer SHA si fichier existe
    r = requests.get(url, headers=headers)
    sha = r.json().get("sha") if r.status_code == 200 else None

    payload = {
        "message": "update from render",
        "content": content
    }

    if sha:
        payload["sha"] = sha

    r = requests.put(url, json=payload, headers=headers)

    return jsonify({
        "render": "ok",
        "github_status": r.status_code
    })
