import { useWebSocket } from '@vueuse/core'
import { watch, ref } from 'vue'
import { useGameStore } from '@/stores/gameStore'
import type { WebSocketMessage, EventType, RoomState } from '@/types'

export function usePokerSocket(roomId: string, userName: string) {
  const store = useGameStore()
  const wsBaseUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8001'
  const wsUrl = `${wsBaseUrl}/ws/${roomId}?name=${encodeURIComponent(userName)}`
  const nudgeReceived = ref<string | null>(null)

  const { status, data, send, close } = useWebSocket(wsUrl, {
    autoReconnect: {
      retries: 3,
      delay: 1000,
    },
    onConnected: () => {
      console.log('WebSocket connected')
    },
    onDisconnected: () => {
      console.log('WebSocket disconnected')
    },
    onError: (_, event) => {
      console.error('WebSocket error:', event)
    },
  })

  watch(data, (newData) => {
    if (newData) {
      try {
        const message: WebSocketMessage = JSON.parse(newData)
        handleMessage(message)
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e)
      }
    }
  })

  function handleMessage(msg: WebSocketMessage): void {
    switch (msg.type) {
      case 'room_state': {
        const state = msg.payload as unknown as RoomState
        store.updateRoomState(state)
        
        if (!store.currentUserId) {
          const users = Object.values(state.users)
          const me = users.find((u) => u.name === userName)
          if (me) {
            store.setCurrentUserId(me.id)
          }
        }
        break
      }
      case 'consensus': {
        const value = msg.payload.value as string
        store.triggerConsensus(value)
        break
      }
      case 'nudge_received': {
        const fromUser = msg.payload.from_user as string
        nudgeReceived.value = fromUser
        playNudgeSound()
        setTimeout(() => {
          nudgeReceived.value = null
        }, 3000)
        break
      }
    }
  }

  function playNudgeSound(): void {
    try {
      const audio = new Audio('data:audio/wav;base64,UklGRl9vT19XQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YU')
      audio.volume = 0.3
      audio.play().catch(() => {})
    } catch {
      // Ignore audio errors
    }
  }

  function emit(type: EventType, payload: Record<string, unknown> = {}): void {
    const message: WebSocketMessage = { type, payload }
    send(JSON.stringify(message))
  }

  function selectCard(value: string): void {
    store.setSelectedCard(value)
    emit('select_card', { value })
  }

  function toggleSpectator(): void {
    emit('toggle_spectator')
  }

  function forceSpectator(userId: string): void {
    emit('force_spectator', { user_id: userId })
  }

  function nudge(targetId: string): void {
    emit('nudge', { target_id: targetId })
  }

  function forceReveal(): void {
    emit('force_reveal')
  }

  function resetRound(): void {
    store.reset()
    emit('reset_round')
  }

  return {
    status,
    nudgeReceived,
    selectCard,
    toggleSpectator,
    forceSpectator,
    nudge,
    forceReveal,
    resetRound,
    close,
  }
}
