# server.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
clients = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all clients
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            for client in clients:
                if client != websocket:
                    await client.send_text(msg)
    except:
        clients.remove(websocket)
