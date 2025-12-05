export type UserRole = 'estimator' | 'spectator'
export type GamePhase = 'estimating' | 'revealed'

export type EventType =
  | 'join'
  | 'leave'
  | 'select_card'
  | 'toggle_spectator'
  | 'force_spectator'
  | 'nudge'
  | 'force_reveal'
  | 'reset_round'
  | 'room_state'
  | 'user_updated'
  | 'cards_revealed'
  | 'consensus'
  | 'nudge_received'

export interface User {
  id: string
  name: string
  role: UserRole
  is_admin: boolean
  has_voted: boolean
  vote: string | null
}

export interface RoomState {
  room_id: string
  phase: GamePhase
  users: Record<string, User>
  deck: string[]
}

export interface WebSocketMessage {
  type: EventType
  payload: Record<string, unknown>
}
