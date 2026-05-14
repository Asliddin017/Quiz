import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.redis_client import get_redis
from app.core.security import decode_token

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/session/{session_id}")
async def quiz_timer(websocket: WebSocket, session_id: int, token: str):
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=4001)
        return

    await websocket.accept()
    redis = get_redis()

    try:
        while True:
            # Redis va vaqt tekshiruvi parallel (asyncio.gather misoli)
            deadline_str, _ = await asyncio.gather(
                redis.get(f"session:{session_id}:deadline"),
                asyncio.sleep(0),  # yield to event loop
            )

            if not deadline_str:
                await websocket.send_json({"type": "time_up"})
                break

            remaining = float(deadline_str) - datetime.now(timezone.utc).timestamp()
            if remaining <= 0:
                await websocket.send_json({"type": "time_up"})
                await redis.delete(f"session:{session_id}:deadline")
                break

            await websocket.send_json(
                {"type": "timer", "remaining_seconds": int(remaining)}
            )
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass
