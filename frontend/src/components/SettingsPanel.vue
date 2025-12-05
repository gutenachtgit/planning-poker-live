<script setup lang="ts">
import { useGameStore } from '@/stores/gameStore'

const store = useGameStore()

defineProps<{
  onToggleSpectator: () => void
  onForceReveal: () => void
  onResetRound: () => void
}>()
</script>

<template>
  <div class="settings-panel">
    <div class="setting-item">
      <label>
        <input
          type="checkbox"
          :checked="store.currentUser?.role === 'spectator'"
          @change="onToggleSpectator"
        />
        Spectator Mode
      </label>
    </div>
    
    <template v-if="store.currentUser?.is_admin">
      <hr />
      <div class="admin-section">
        <h4>Admin</h4>
        <button 
          class="btn btn-reveal"
          :disabled="store.phase === 'revealed'"
          @click="onForceReveal"
        >
          Force Reveal
        </button>
        <button 
          class="btn btn-reset"
          @click="onResetRound"
        >
          Neue Runde
        </button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.settings-panel {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  min-width: 180px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.setting-item {
  margin-bottom: 8px;
}

.setting-item label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
}

hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 12px 0;
}

.admin-section h4 {
  margin: 0 0 12px 0;
  font-size: 12px;
  text-transform: uppercase;
  color: #888;
}

.btn {
  width: 100%;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 8px;
  transition: all 0.2s ease;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-reveal {
  background: #4a90d9;
  color: white;
}

.btn-reveal:hover:not(:disabled) {
  background: #3a7fc8;
}

.btn-reset {
  background: #28a745;
  color: white;
}

.btn-reset:hover {
  background: #218838;
}
</style>
