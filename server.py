from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

TOKEN = "SECRET123"
clients = set()

@app.get("/")
def home():
    return {"status": "online"}

# 🔥 ENVOI D'ACTION DEPUIS GUI
@app.get("/send")
async def send(action: str, token: str):
    if token != TOKEN:
        return {"error": "unauthorized"}

    payload = json.dumps({"action": action})

    for ws in list(clients):
        await ws.send_text(payload)

    return {"status": "sent", "action": action}


# ⚡ WEBSOCKET CLIENT
@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        # 🔐 AUTH
        auth_msg = await ws.receive_text()
        data = json.loads(auth_msg)

        if data.get("token") != TOKEN:
            await ws.close()
            return

        clients.add(ws)
        await ws.send_text(json.dumps({"status": "connected"}))

        while True:
            msg = await ws.receive_text()
            print("CLIENT RESPONSE:", msg)

    except WebSocketDisconnect:
        clients.discard(ws)
