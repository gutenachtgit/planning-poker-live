<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '@/stores/gameStore'
import { usePokerSocket } from '@/composables/usePokerSocket'
import PokerTable from '@/components/PokerTable.vue'
import CardDeck from '@/components/CardDeck.vue'
import UserCard from '@/components/UserCard.vue'
import SettingsPanel from '@/components/SettingsPanel.vue'
import ConsensusCat from '@/components/ConsensusCat.vue'

const store = useGameStore()

const isJoined = ref(false)
const joinName = ref('')
const joinRoom = ref('')
const showSettings = ref(false)
const copySuccess = ref(false)

const socket = ref<ReturnType<typeof usePokerSocket> | null>(null)

onMounted(() => {
  const params = new URLSearchParams(window.location.search)
  const roomFromUrl = params.get('room')
  if (roomFromUrl) {
    joinRoom.value = roomFromUrl
  } else {
    joinRoom.value = generateRoomId()
  }
})

function generateRoomId(): string {
  return Math.random().toString(36).substring(2, 8)
}

function joinGame(): void {
  if (!joinName.value.trim()) return
  
  socket.value = usePokerSocket(joinRoom.value, joinName.value)
  isJoined.value = true
  
  // URL aktualisieren ohne Reload
  const url = new URL(window.location.href)
  url.searchParams.set('room', joinRoom.value)
  window.history.replaceState({}, '', url.toString())
}

function copyInviteUrl(): void {
  const url = new URL(window.location.href)
  url.searchParams.set('room', store.roomId)
  navigator.clipboard.writeText(url.toString()).then(() => {
    copySuccess.value = true
    setTimeout(() => {
      copySuccess.value = false
    }, 2000)
  })
}

function handleSelectCard(value: string): void {
  socket.value?.selectCard(value)
}

function handleToggleSpectator(): void {
  socket.value?.toggleSpectator()
}

function handleForceReveal(): void {
  socket.value?.forceReveal()
}

function handleResetRound(): void {
  socket.value?.resetRound()
}

function handleNudge(userId: string): void {
  socket.value?.nudge(userId)
}

function handleForceSpectator(userId: string): void {
  socket.value?.forceSpectator(userId)
}

const connectionStatus = computed(() => socket.value?.status || 'CLOSED')
</script>

<template>
  <div class="app">
    <template v-if="!isJoined">
      <div class="join-screen">
        <div class="join-card">
          <h1>Planning Poker</h1>
          <div class="form-group">
            <label for="name">Dein Name</label>
            <input
              id="name"
              v-model="joinName"
              type="text"
              placeholder="Name eingeben..."
              @keyup.enter="joinGame"
            />
          </div>
          <div class="form-group">
            <label for="room">Raum</label>
            <input
              id="room"
              v-model="joinRoom"
              type="text"
              placeholder="Raum-ID..."
            />
          </div>
          <button class="join-btn" @click="joinGame" :disabled="!joinName.trim()">
            Beitreten
          </button>
        </div>
      </div>
    </template>

    <template v-else>
      <header class="header">
        <div class="header-left">
          <button class="invite-btn" @click="copyInviteUrl">
            {{ copySuccess ? '✓ Kopiert!' : '📋 Einladen' }}
          </button>
        </div>
        <div class="header-center">
          <span class="room-name">Raum: {{ store.roomId }}</span>
          <span class="connection-status" :class="connectionStatus.toLowerCase()">
            {{ connectionStatus }}
          </span>
        </div>
        <div class="header-right">
          <span class="phase-badge" :class="store.phase">
            {{ store.phase === 'estimating' ? 'Schaetzen' : 'Aufgedeckt' }}
          </span>
          <button class="settings-btn" @click="showSettings = !showSettings">
            ⚙️
          </button>
        </div>
      </header>

      <div class="settings-dropdown" v-if="showSettings">
        <SettingsPanel
          :on-toggle-spectator="handleToggleSpectator"
          :on-force-reveal="handleForceReveal"
          :on-reset-round="handleResetRound"
        />
      </div>

      <main class="main">
        <PokerTable
          :on-nudge="handleNudge"
          :on-force-spectator="handleForceSpectator"
        />

        <div class="current-user-section" v-if="store.currentUser">
          <UserCard
            :user="store.currentUser"
            :phase="store.phase"
            :is-current-user="true"
          />
        </div>

        <CardDeck :on-select="handleSelectCard" />
      </main>

      <div class="nudge-notification" v-if="socket && socket.nudgeReceived">
        👋 {{ socket.nudgeReceived }} stupst dich an!
      </div>

      <ConsensusCat v-if="store.showConsensus" :value="store.consensusValue" />
    </template>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f0f2f5;
  min-height: 100vh;
}
</style>

<style scoped>
.app {
  min-height: 100vh;
}

.join-screen {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a365d 0%, #2d4a7c 100%);
}

.join-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

.join-card h1 {
  text-align: center;
  margin-bottom: 32px;
  color: #1a365d;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-group input[type="text"] {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.2s;
}

.form-group input[type="text"]:focus {
  outline: none;
  border-color: #4a90d9;
}

.form-group.checkbox label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.join-btn {
  width: 100%;
  padding: 14px;
  background: #4a90d9;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.join-btn:hover:not(:disabled) {
  background: #3a7fc8;
}

.join-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #e0e0e0;
}

.header-left,
.header-center,
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-center {
  flex: 1;
  justify-content: center;
}

.invite-btn {
  padding: 8px 16px;
  background: #4a90d9;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.invite-btn:hover {
  background: #3a7fc8;
}

.room-name {
  font-weight: 600;
  color: #333;
}

.connection-status {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}

.connection-status.open {
  background: #d4edda;
  color: #155724;
}

.connection-status.connecting {
  background: #fff3cd;
  color: #856404;
}

.connection-status.closed {
  background: #f8d7da;
  color: #721c24;
}

.phase-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.phase-badge.estimating {
  background: #e3f2fd;
  color: #1565c0;
}

.phase-badge.revealed {
  background: #e8f5e9;
  color: #2e7d32;
}

.settings-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 8px;
  background: #f5f5f5;
  cursor: pointer;
  font-size: 20px;
  transition: background 0.2s;
}

.settings-btn:hover {
  background: #e0e0e0;
}

.settings-dropdown {
  position: absolute;
  top: 70px;
  right: 24px;
  z-index: 100;
}

.main {
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  min-height: calc(100vh - 73px);
}

.current-user-section {
  padding: 16px;
  background: rgba(74, 144, 217, 0.1);
  border-radius: 12px;
}

.nudge-notification {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  background: #ffeeba;
  color: #856404;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  animation: slideUp 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}
</style>
