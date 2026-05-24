import os
from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# 🔐 IMPORTANT: mettre ça dans Render Environment Variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

REPO = "kdisksnwj/crotte"
FILE_PATH = "data.txt"


def get_sha():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.json()["sha"]
    return None


@app.route("/send", methods=["POST"])
def send():
    data = request.json

    # 📦 convertir en base64 (format GitHub obligatoire)
    content = base64.b64encode(
        str(data).encode("utf-8")
    ).decode("utf-8")

    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

    payload = {
        "message": "update from render",
        "content": content
    }

    sha = get_sha()
    if sha:
        payload["sha"] = sha

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    r = requests.put(url, json=payload, headers=headers)

    # 🔥 DEBUG IMPORTANT (pour voir pourquoi ça marche pas)
    print("GITHUB STATUS:", r.status_code)
    print("GITHUB RESPONSE:", r.text)

    return jsonify({
        "render": "ok",
        "github_status": r.status_code,
        "github_response": r.text
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
