import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, RoomState, GamePhase } from '@/types'

export const useGameStore = defineStore('game', () => {
  const roomId = ref<string>('')
  const phase = ref<GamePhase>('estimating')
  const users = ref<Record<string, User>>({})
  const deck = ref<string[]>(['0', '1', '2', '3', '5', '8', '13', '?'])
  const currentUserId = ref<string>('')
  const selectedCard = ref<string | null>(null)
  const showConsensus = ref<boolean>(false)
  const consensusValue = ref<string | null>(null)

  const currentUser = computed(() => users.value[currentUserId.value])
  
  const otherUsers = computed(() =>
    Object.values(users.value).filter((u) => u.id !== currentUserId.value)
  )

  const estimators = computed(() =>
    Object.values(users.value).filter((u) => u.role === 'estimator')
  )

  const allEstimated = computed(() =>
    estimators.value.length > 0 && estimators.value.every((u) => u.has_voted)
  )

  const hasConsensus = computed(() => {
    const votes = estimators.value.filter((u) => u.vote).map((u) => u.vote)
    return votes.length > 0 && new Set(votes).size === 1
  })

  function updateRoomState(state: RoomState): void {
    const wasRevealed = phase.value === 'revealed'
    
    roomId.value = state.room_id
    phase.value = state.phase
    users.value = state.users
    deck.value = state.deck

    if (state.phase === 'estimating') {
      showConsensus.value = false
      consensusValue.value = null
      
      if (wasRevealed) {
        selectedCard.value = null
      }
    }
  }

  function setCurrentUserId(id: string): void {
    currentUserId.value = id
  }

  function setSelectedCard(value: string | null): void {
    selectedCard.value = value
  }

  function triggerConsensus(value: string): void {
    showConsensus.value = true
    consensusValue.value = value
  }

  function reset(): void {
    selectedCard.value = null
    showConsensus.value = false
    consensusValue.value = null
  }

  return {
    roomId,
    phase,
    users,
    deck,
    currentUserId,
    selectedCard,
    showConsensus,
    consensusValue,
    currentUser,
    otherUsers,
    estimators,
    allEstimated,
    hasConsensus,
    updateRoomState,
    setCurrentUserId,
    setSelectedCard,
    triggerConsensus,
    reset,
  }
})
