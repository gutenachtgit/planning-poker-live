<script setup lang="ts">
import { computed } from 'vue'
import { useGameStore } from '@/stores/gameStore'
import UserCard from './UserCard.vue'

const props = defineProps<{
  onNudge: (userId: string) => void
  onForceSpectator: (userId: string) => void
}>()

const store = useGameStore()

const tableUsers = computed(() => {
  const users = store.otherUsers
  const positions: { user: typeof users[0]; position: string }[] = []
  
  users.forEach((user, index) => {
    const total = users.length
    let position: string
    
    if (total <= 3) {
      position = ['top', 'left', 'right'][index] || 'top'
    } else {
      const angle = (index / total) * 360
      if (angle < 60 || angle >= 300) position = 'top'
      else if (angle < 120) position = 'right'
      else if (angle < 240) position = 'bottom'
      else position = 'left'
    }
    
    positions.push({ user, position })
  })
  
  return positions
})

const topUsers = computed(() => tableUsers.value.filter(u => u.position === 'top'))
const leftUsers = computed(() => tableUsers.value.filter(u => u.position === 'left'))
const rightUsers = computed(() => tableUsers.value.filter(u => u.position === 'right'))
const bottomUsers = computed(() => tableUsers.value.filter(u => u.position === 'bottom'))
</script>

<template>
  <div class="poker-table">
    <div class="table-position top">
      <UserCard
        v-for="{ user } in topUsers"
        :key="user.id"
        :user="user"
        :phase="store.phase"
        :show-admin-actions="store.currentUser?.is_admin"
        :on-nudge="() => props.onNudge(user.id)"
        :on-force-spectator="() => props.onForceSpectator(user.id)"
      />
    </div>
    
    <div class="table-middle">
      <div class="table-position left">
        <UserCard
          v-for="{ user } in leftUsers"
          :key="user.id"
          :user="user"
          :phase="store.phase"
          :show-admin-actions="store.currentUser?.is_admin"
          :on-nudge="() => props.onNudge(user.id)"
          :on-force-spectator="() => props.onForceSpectator(user.id)"
        />
      </div>
      
      <div class="table-center">
        <div class="table-felt">
          <div class="table-logo">
            <span class="logo-text">Planning</span>
            <span class="logo-text">Poker</span>
          </div>
        </div>
      </div>
      
      <div class="table-position right">
        <UserCard
          v-for="{ user } in rightUsers"
          :key="user.id"
          :user="user"
          :phase="store.phase"
          :show-admin-actions="store.currentUser?.is_admin"
          :on-nudge="() => props.onNudge(user.id)"
          :on-force-spectator="() => props.onForceSpectator(user.id)"
        />
      </div>
    </div>
    
    <div class="table-position bottom">
      <UserCard
        v-for="{ user } in bottomUsers"
        :key="user.id"
        :user="user"
        :phase="store.phase"
        :show-admin-actions="store.currentUser?.is_admin"
        :on-nudge="() => props.onNudge(user.id)"
        :on-force-spectator="() => props.onForceSpectator(user.id)"
      />
    </div>
  </div>
</template>

<style scoped>
.poker-table {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 24px;
}

.table-position {
  display: flex;
  gap: 16px;
  justify-content: center;
  min-height: 100px;
}

.table-middle {
  display: flex;
  align-items: center;
  gap: 24px;
}

.table-position.left,
.table-position.right {
  flex-direction: column;
  min-width: 80px;
}

.table-center {
  width: 300px;
  height: 180px;
}

.table-felt {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a365d 0%, #2d4a7c 50%, #1a365d 100%);
  border-radius: 100px;
  border: 8px solid #8b4513;
  box-shadow: 
    inset 0 0 30px rgba(0, 0, 0, 0.3),
    0 4px 20px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.table-felt::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    repeating-linear-gradient(
      45deg,
      transparent,
      transparent 10px,
      rgba(255, 255, 255, 0.02) 10px,
      rgba(255, 255, 255, 0.02) 20px
    );
}

.table-logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 1;
}

.logo-text {
  font-size: 24px;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.15);
  text-transform: uppercase;
  letter-spacing: 4px;
}
</style>
