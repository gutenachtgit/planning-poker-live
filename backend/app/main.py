import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware

from .models import User, UserRole, EventType, WebSocketMessage
from .websocket_manager import ConnectionManager

app = FastAPI(title="Planning Poker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "Planning Poker API running"}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    name: str = Query(...),
) -> None:
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        name=name,
        role=UserRole.ESTIMATOR,
    )

    await manager.connect(websocket, room_id, user)

    try:
        await manager.broadcast_room_state(room_id)

        while True:
            data = await websocket.receive_json()
            await handle_message(room_id, user_id, data)

    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id)
        await manager.broadcast_room_state(room_id)


async def handle_message(room_id: str, user_id: str, data: dict) -> None:
    try:
        msg = WebSocketMessage(**data)
    except Exception:
        return

    if msg.type == EventType.SELECT_CARD:
        value = msg.payload.get("value")
        if value and manager.select_card(room_id, user_id, value):
            await manager.broadcast_room_state(room_id)
            if manager.check_all_estimated(room_id):
                manager.reveal_cards(room_id)
                await manager.broadcast_room_state(room_id)
                has_consensus, consensus_value = manager.check_consensus(room_id)
                if has_consensus:
                    await manager.broadcast(
                        room_id,
                        WebSocketMessage(
                            type=EventType.CONSENSUS,
                            payload={"value": consensus_value}
                        )
                    )

    elif msg.type == EventType.TOGGLE_SPECTATOR:
        if manager.toggle_spectator(room_id, user_id):
            await manager.broadcast_room_state(room_id)

    elif msg.type == EventType.FORCE_SPECTATOR:
        target_id = msg.payload.get("user_id")
        if target_id and manager.force_spectator(room_id, user_id, target_id):
            await manager.broadcast_room_state(room_id)

    elif msg.type == EventType.NUDGE:
        target_id = msg.payload.get("target_id")
        sender = manager.get_user(room_id, user_id)
        if target_id and sender:
            await manager.send_personal(
                room_id,
                target_id,
                WebSocketMessage(
                    type=EventType.NUDGE_RECEIVED,
                    payload={"from_user": sender.name}
                )
            )

    elif msg.type == EventType.FORCE_REVEAL:
        user = manager.get_user(room_id, user_id)
        if user and user.is_admin:
            if manager.reveal_cards(room_id):
                await manager.broadcast_room_state(room_id)
                has_consensus, consensus_value = manager.check_consensus(room_id)
                if has_consensus:
                    await manager.broadcast(
                        room_id,
                        WebSocketMessage(
                            type=EventType.CONSENSUS,
                            payload={"value": consensus_value}
                        )
                    )

    elif msg.type == EventType.RESET_ROUND:
        user = manager.get_user(room_id, user_id)
        if user and user.is_admin:
            if manager.reset_round(room_id):
                await manager.broadcast_room_state(room_id)
