<template>
  <div class="game-screen">
    <div class="game-header">
      <h2>Игра #{{ props.game?.id }}</h2>
      <div class="players-list" v-if="props.me">
        <div
            v-for="player in props.game?.players"
            :key="player.username"
            class="player-badge"
            :style="{ backgroundColor: player.color }"
        >
          {{ props.me.username === player.username ? 'You' : player.username }}: {{ player.score }}
        </div>
      </div>
    </div>
    <div class="game-board">
      <div
          v-for="(row, y) in props.game?.field"
          :key="y"
          class="row"
      >
        <div
            v-for="(cell, x) in row"
            :key="x"
            class="cell"
            :style="{
            backgroundColor: cell.player ? cell.player.color : '#f0f0f0',
            cursor: 'pointer'
          }"
            @click="emits('move', x, y)"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  game: never
  me: never
}>();

const emits = defineEmits(["move"]);
</script>

<style scoped>
.game-screen {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.players-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.player-badge {
  padding: 5px 10px;
  border-radius: 15px;
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.game-board {
  margin-top: 20px;
}

.row {
  display: flex;
  justify-content: center;
}

.cell {
  width: 50px;
  height: 50px;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
