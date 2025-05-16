from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import redis.asyncio as redis

router = APIRouter()
r = redis.Redis()

connected_clients = set()

@router.websocket("/ws/feed")
async def websocket_feed(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)

    pubsub = r.pubsub()
    await pubsub.subscribe("task_feed")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                for client in connected_clients:
                    await client.send_text(message["data"].decode())
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        await pubsub.unsubscribe("task_feed")
