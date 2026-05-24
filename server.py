import asyncio
import websockets
import json
import platform
import socket

# 🔐 CONFIG
TOKEN = "SECRET123"
SERVER = "wss://render-e5pg.onrender.com/ws"

# 🧠 ACTIONS AUTORISÉES (SAFE)
def run_action(action):
    if action == "system_info":
        return {
            "os": platform.system(),
            "pc": platform.node(),
            "ip": socket.gethostbyname(socket.gethostname())
        }

    elif action == "ping":
        return "pong"

    elif action == "cpu":
        return "simulated_cpu_info"

    else:
        return "blocked_action"


async def main():
    try:
        async with websockets.connect(SERVER) as ws:

            # 🔐 AUTH (OBLIGATOIRE)
            await ws.send(json.dumps({"token": TOKEN}))
            print("[+] Connected to server")

            while True:
                # 📩 recevoir action serveur
                msg = await ws.recv()
                data = json.loads(msg)

                action = data.get("action")
                print("[SERVER ACTION]", action)

                # ⚙️ exécuter action whitelist
                result = run_action(action)

                # 📤 envoyer résultat
                await ws.send(json.dumps({
                    "action": action,
                    "result": result
                }))

                print("[RESULT SENT]", result)

    except Exception as e:
        print("[ERROR]", e)


# 🚀 START CLIENT
asyncio.run(main())
