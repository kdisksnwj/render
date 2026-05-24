from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

TOKEN = "SECRET123"

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    # AUTH
    auth = await ws.receive_text()
    data = json.loads(auth)

    if data.get("token") != TOKEN:
        await ws.close()
        return

    clients.add(ws)

    try:
        while True:
            msg = await ws.receive_text()
            print("From client:", msg)

    except WebSocketDisconnect:
        clients.remove(ws)


@app.get("/send")
async def send(action: str, token: str):
    if token != TOKEN:
        return {"error": "unauthorized"}

    payload = json.dumps({"action": action})

    for c in clients:
        await c.send_text(payload)

    return {"status": "sent"}
