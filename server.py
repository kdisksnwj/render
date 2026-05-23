from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

clients = []

@app.route("/")
def home():
    return "ONLINE"

@socketio.on("connect")
def on_connect():
    print("Client connected")

@socketio.on("message")
def handle_message(data):

    msg = {
        "user": data.get("user"),
        "message": data.get("message"),
        "ip": request.remote_addr,
        "hostname": data.get("hostname")
    }

    print(msg)

    emit("broadcast", msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
