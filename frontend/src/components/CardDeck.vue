<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '@/stores/gameStore'

const props = defineProps<{
  disabled?: boolean
  onSelect: (value: string) => void
}>()

const store = useGameStore()

const isDisabled = computed(() => 
  props.disabled || store.phase === 'revealed' || store.currentUser?.role === 'spectator'
)
</script>

<template>
  <div class="card-deck">
    <button
      v-for="card in store.deck"
      :key="card"
      class="card"
      :class="{ 
        selected: store.selectedCard === card,
        disabled: isDisabled
      }"
      :disabled="isDisabled"
      @click="onSelect(card)"
    >
      {{ card }}
    </button>
  </div>
</template>

<style scoped>
.card-deck {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 12px;
}

.card {
  width: 60px;
  height: 80px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background: white;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card:hover:not(.disabled) {
  border-color: #4a90d9;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(74, 144, 217, 0.3);
}

.card.selected {
  border-color: #4a90d9;
  background: #4a90d9;
  color: white;
  transform: translateY(-8px);
  box-shadow: 0 8px 16px rgba(74, 144, 217, 0.4);
}

.card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
