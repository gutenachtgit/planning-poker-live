<script setup lang="ts">
defineProps<{
  value: string | null
}>()
</script>

<template>
  <div class="consensus-cat">
    <div class="cat-container">
      <div class="cat-face">
        <div class="ears">
          <div class="ear left"></div>
          <div class="ear right"></div>
        </div>
        <div class="face">
          <div class="eyes">
            <div class="eye left">
              <div class="pupil"></div>
            </div>
            <div class="eye right">
              <div class="pupil"></div>
            </div>
          </div>
          <div class="nose"></div>
          <div class="mouth"></div>
          <div class="whiskers left">
            <div class="whisker"></div>
            <div class="whisker"></div>
            <div class="whisker"></div>
          </div>
          <div class="whiskers right">
            <div class="whisker"></div>
            <div class="whisker"></div>
            <div class="whisker"></div>
          </div>
        </div>
      </div>
      <div class="speech-bubble">
        <span class="consensus-value">{{ value }}</span>
        <span class="consensus-text">Konsens!</span>
      </div>
    </div>
    <div class="confetti">
      <span v-for="i in 20" :key="i" class="confetti-piece" :style="{ '--delay': i * 0.1 + 's', '--x': Math.random() * 100 + '%' }"></span>
    </div>
  </div>
</template>

<style scoped>
.consensus-cat {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
  to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}

.cat-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cat-face {
  width: 120px;
  height: 120px;
  position: relative;
}

.ears {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  display: flex;
  justify-content: space-between;
}

.ear {
  width: 0;
  height: 0;
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-bottom: 30px solid #ffa500;
}

.ear.left { transform: rotate(-15deg); }
.ear.right { transform: rotate(15deg); }

.face {
  width: 100px;
  height: 90px;
  background: #ffa500;
  border-radius: 50%;
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
}

.eyes {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding-top: 25px;
}

.eye {
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pupil {
  width: 10px;
  height: 10px;
  background: #333;
  border-radius: 50%;
  animation: blink 3s infinite;
}

@keyframes blink {
  0%, 90%, 100% { transform: scaleY(1); }
  95% { transform: scaleY(0.1); }
}

.nose {
  width: 10px;
  height: 8px;
  background: #ff6b6b;
  border-radius: 50%;
  margin: 8px auto 0;
}

.mouth {
  width: 20px;
  height: 10px;
  border: 2px solid #333;
  border-top: none;
  border-radius: 0 0 20px 20px;
  margin: 2px auto 0;
}

.whiskers {
  position: absolute;
  top: 55px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.whiskers.left { left: 5px; }
.whiskers.right { right: 5px; }

.whisker {
  width: 25px;
  height: 2px;
  background: #333;
}

.whiskers.left .whisker { transform-origin: right; }
.whiskers.right .whisker { transform-origin: left; }

.whiskers.left .whisker:nth-child(1) { transform: rotate(-10deg); }
.whiskers.left .whisker:nth-child(3) { transform: rotate(10deg); }
.whiskers.right .whisker:nth-child(1) { transform: rotate(10deg); }
.whiskers.right .whisker:nth-child(3) { transform: rotate(-10deg); }

.speech-bubble {
  background: white;
  border: 3px solid #333;
  border-radius: 20px;
  padding: 16px 24px;
  margin-top: 20px;
  text-align: center;
  position: relative;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.speech-bubble::before {
  content: '';
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  border: 10px solid transparent;
  border-bottom-color: #333;
}

.speech-bubble::after {
  content: '';
  position: absolute;
  top: -6px;
  left: 50%;
  transform: translateX(-50%);
  border: 8px solid transparent;
  border-bottom-color: white;
}

.consensus-value {
  font-size: 36px;
  font-weight: bold;
  color: #4a90d9;
  display: block;
}

.consensus-text {
  font-size: 18px;
  color: #666;
}

.confetti {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.confetti-piece {
  position: absolute;
  top: -20px;
  left: var(--x);
  width: 10px;
  height: 10px;
  background: hsl(calc(var(--delay, 0s) * 360), 80%, 60%);
  animation: fall 3s linear var(--delay) infinite;
}

.confetti-piece:nth-child(odd) {
  border-radius: 50%;
}

@keyframes fall {
  to {
    transform: translateY(100vh) rotate(720deg);
  }
}
</style>
