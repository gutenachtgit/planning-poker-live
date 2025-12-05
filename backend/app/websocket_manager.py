from fastapi import WebSocket
from typing import Dict, Optional, Tuple
from .models import WebSocketMessage, RoomState, User, GamePhase, UserRole, EventType


class ConnectionManager:
    def __init__(self) -> None:
        self.rooms: Dict[str, RoomState] = {}
        self.connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str, user: User) -> None:
        await websocket.accept()
        
        # Erster User im Raum wird automatisch Admin
        is_first_user = room_id not in self.rooms or len(self.rooms[room_id].users) == 0
        user.is_admin = is_first_user
        
        if room_id not in self.rooms:
            self.rooms[room_id] = RoomState(room_id=room_id)
        self.rooms[room_id].users[user.id] = user
        if room_id not in self.connections:
            self.connections[room_id] = {}
        self.connections[room_id][user.id] = websocket

    def disconnect(self, room_id: str, user_id: str) -> None:
        if room_id in self.connections:
            self.connections[room_id].pop(user_id, None)
        if room_id in self.rooms:
            self.rooms[room_id].users.pop(user_id, None)

    def get_room(self, room_id: str) -> Optional[RoomState]:
        return self.rooms.get(room_id)

    def get_user(self, room_id: str, user_id: str) -> Optional[User]:
        room = self.get_room(room_id)
        if room:
            return room.users.get(user_id)
        return None

    async def broadcast(self, room_id: str, message: WebSocketMessage) -> None:
        if room_id in self.connections:
            disconnected = []
            for user_id, ws in self.connections[room_id].items():
                try:
                    await ws.send_json(message.model_dump())
                except Exception:
                    disconnected.append(user_id)
            for user_id in disconnected:
                self.disconnect(room_id, user_id)

    async def send_personal(self, room_id: str, user_id: str, message: WebSocketMessage) -> None:
        if room_id in self.connections and user_id in self.connections[room_id]:
            try:
                await self.connections[room_id][user_id].send_json(message.model_dump())
            except Exception:
                self.disconnect(room_id, user_id)

    async def broadcast_room_state(self, room_id: str) -> None:
        room = self.get_room(room_id)
        if room:
            users_public = {}
            for uid, user in room.users.items():
                user_data = user.model_dump()
                if room.phase == GamePhase.ESTIMATING:
                    user_data["vote"] = None
                users_public[uid] = user_data
            
            message = WebSocketMessage(
                type=EventType.ROOM_STATE,
                payload={
                    "room_id": room.room_id,
                    "phase": room.phase.value,
                    "users": users_public,
                    "deck": room.deck
                }
            )
            await self.broadcast(room_id, message)

    def select_card(self, room_id: str, user_id: str, value: str) -> bool:
        room = self.get_room(room_id)
        if not room or room.phase != GamePhase.ESTIMATING:
            return False
        user = room.users.get(user_id)
        if not user or user.role != UserRole.ESTIMATOR:
            return False
        user.vote = value
        user.has_voted = True
        return True

    def toggle_spectator(self, room_id: str, user_id: str) -> bool:
        room = self.get_room(room_id)
        if not room:
            return False
        user = room.users.get(user_id)
        if not user:
            return False
        if user.role == UserRole.ESTIMATOR:
            user.role = UserRole.SPECTATOR
            user.vote = None
            user.has_voted = False
        else:
            user.role = UserRole.ESTIMATOR
        return True

    def force_spectator(self, room_id: str, admin_id: str, target_id: str) -> bool:
        room = self.get_room(room_id)
        if not room:
            return False
        admin = room.users.get(admin_id)
        target = room.users.get(target_id)
        if not admin or not admin.is_admin or not target:
            return False
        target.role = UserRole.SPECTATOR
        target.vote = None
        target.has_voted = False
        return True

    def check_all_estimated(self, room_id: str) -> bool:
        room = self.get_room(room_id)
        if not room:
            return False
        estimators = [u for u in room.users.values() if u.role == UserRole.ESTIMATOR]
        if not estimators:
            return False
        return all(u.has_voted for u in estimators)

    def reveal_cards(self, room_id: str) -> bool:
        room = self.get_room(room_id)
        if not room or room.phase != GamePhase.ESTIMATING:
            return False
        room.phase = GamePhase.REVEALED
        return True

    def check_consensus(self, room_id: str) -> Tuple[bool, Optional[str]]:
        room = self.get_room(room_id)
        if not room or room.phase != GamePhase.REVEALED:
            return False, None
        votes = [u.vote for u in room.users.values() if u.role == UserRole.ESTIMATOR and u.vote]
        if not votes:
            return False, None
        if len(set(votes)) == 1:
            return True, votes[0]
        return False, None

    def reset_round(self, room_id: str) -> bool:
        room = self.get_room(room_id)
        if not room:
            return False
        room.phase = GamePhase.ESTIMATING
        for user in room.users.values():
            if user.role == UserRole.ESTIMATOR:
                user.vote = None
                user.has_voted = False
        return True
