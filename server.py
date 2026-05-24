from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

TOKEN = "SECRET123"
clients = set()

@app.get("/")
def home():
    return {"status": "online"}

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()

    try:
        # 🔐 AUTH FIRST MESSAGE
        auth_msg = await ws.receive_text()
        data = json.loads(auth_msg)

        if data.get("token") != TOKEN:
            await ws.close()
            return

        clients.add(ws)
        await ws.send_text(json.dumps({"status": "connected"}))

        while True:
            msg = await ws.receive_text()
            print("Client:", msg)

    except WebSocketDisconnect:
        clients.discard(ws)
