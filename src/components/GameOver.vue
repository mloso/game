<template>
  <div class="game-over">
    <h2>Игра окончена!</h2>
    <div
        v-if="props.winners"
        class="winners"
    >
      <h3>Победители:</h3>
      <div
          v-for="winner in props.winners"
          :key="winner.username"
          class="winner-badge"
      >
        <span
            class="winner-color"
            :style="{ backgroundColor: winner.color }"
        ></span>
        {{ winner.username }}: ({{ winner.score }} клеток)
      </div>
    </div>
    <div class="scoreboard">
      <h3>Все игроки:</h3>
      <div
          v-for="player in props.players"
          :key="player.username"
          class="player-score"
          :style="{ color: player.color }"
      >
        {{ player.username }}: {{ player.score }} клеток
      </div>
    </div>
    <button
        @click="emits('exit')"
        class="btn"
    >
      Вернуться в лобби
    </button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  winners: never[] | null
  players: never[]
}>();

const emits = defineEmits(["exit"]);
</script>

<style scoped>
.game-over {
  text-align: center;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
}

.winners {
  margin: 20px 0;
}

.winner-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 10px 0;
}

.winner-color {
  display: inline-block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #333;
}

.scoreboard {
  margin: 30px 0;
}

.player-score {
  font-size: 18px;
  margin: 10px 0;
}
</style>
