<script setup lang="ts">
import { computed } from 'vue'
import type { User, GamePhase } from '@/types'

const props = defineProps<{
  user: User
  phase: GamePhase
  isCurrentUser?: boolean
  onNudge?: () => void
  onForceSpectator?: () => void
  showAdminActions?: boolean
}>()

const cardDisplay = computed(() => {
  if (props.user.role === 'spectator') {
    return { text: '👁', class: 'spectator' }
  }
  if (props.phase === 'revealed' && props.user.vote) {
    return { text: props.user.vote, class: 'revealed' }
  }
  if (props.user.has_voted) {
    return { text: '✓', class: 'voted' }
  }
  return { text: '?', class: 'waiting' }
})
</script>

<template>
  <div class="user-card" :class="{ 'is-current': isCurrentUser }">
    <div class="card-face" :class="cardDisplay.class">
      {{ cardDisplay.text }}
    </div>
    <div class="user-name">
      {{ user.name }}
      <span v-if="user.is_admin" class="admin-badge">Admin</span>
    </div>
    <div v-if="showAdminActions && !isCurrentUser" class="actions">
      <button 
        v-if="!user.has_voted && user.role === 'estimator'" 
        class="nudge-btn"
        @click="onNudge"
        title="Anstupsen"
      >
        👋
      </button>
      <button 
        v-if="user.role === 'estimator'"
        class="spectator-btn"
        @click="onForceSpectator"
        title="Zum Spectator machen"
      >
        👁
      </button>
    </div>
  </div>
</template>

<style scoped>
.user-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.user-card.is-current {
  background: rgba(74, 144, 217, 0.1);
}

.card-face {
  width: 50px;
  height: 70px;
  border: 2px solid #ccc;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  background: white;
  transition: all 0.3s ease;
}

.card-face.spectator {
  background: #f0f0f0;
  border-style: dashed;
}

.card-face.voted {
  background: linear-gradient(135deg, #1a365d 0%, #2d4a7c 100%);
  color: white;
  border-color: #1a365d;
}

.card-face.revealed {
  background: #4a90d9;
  color: white;
  border-color: #4a90d9;
  animation: flip 0.5s ease;
}

.card-face.waiting {
  background: #fff;
  color: #ccc;
}

@keyframes flip {
  0% { transform: rotateY(0deg); }
  50% { transform: rotateY(90deg); }
  100% { transform: rotateY(0deg); }
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.admin-badge {
  font-size: 10px;
  background: #ffd700;
  color: #333;
  padding: 2px 6px;
  border-radius: 4px;
}

.actions {
  display: flex;
  gap: 4px;
}

.nudge-btn,
.spectator-btn {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  transition: transform 0.2s ease;
}

.nudge-btn {
  background: #ffeeba;
}

.spectator-btn {
  background: #e0e0e0;
}

.nudge-btn:hover,
.spectator-btn:hover {
  transform: scale(1.1);
}
</style>
