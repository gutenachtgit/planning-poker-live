from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    ESTIMATOR = "estimator"
    SPECTATOR = "spectator"


class GamePhase(str, Enum):
    ESTIMATING = "estimating"
    REVEALED = "revealed"


class User(BaseModel):
    id: str
    name: str
    role: UserRole = UserRole.ESTIMATOR
    is_admin: bool = False
    has_voted: bool = False
    vote: Optional[str] = None


class RoomState(BaseModel):
    room_id: str
    phase: GamePhase = GamePhase.ESTIMATING
    users: dict[str, User] = Field(default_factory=dict)
    deck: list[str] = Field(default_factory=lambda: ["0", "1", "2", "3", "5", "8", "13", "?"])


class EventType(str, Enum):
    JOIN = "join"
    LEAVE = "leave"
    SELECT_CARD = "select_card"
    TOGGLE_SPECTATOR = "toggle_spectator"
    FORCE_SPECTATOR = "force_spectator"
    NUDGE = "nudge"
    FORCE_REVEAL = "force_reveal"
    RESET_ROUND = "reset_round"
    ROOM_STATE = "room_state"
    USER_UPDATED = "user_updated"
    CARDS_REVEALED = "cards_revealed"
    CONSENSUS = "consensus"
    NUDGE_RECEIVED = "nudge_received"


class WebSocketMessage(BaseModel):
    type: EventType
    payload: dict = Field(default_factory=dict)
