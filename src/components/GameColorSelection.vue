<template>
  <div class="color-selection">
    <h2>Выберите цвет</h2>
    <div class="color-palette">
      <div
          v-for="color in props.game?.colors"
          :key="color"
          class="color-option"
          :style="{ backgroundColor: color }"
          :class="{
          selected: props.selectedColor === color ||
                  props.game?.players.some(player => player.color === color)
        }"
          @click="emits('selectColor', color)"
      ></div>
    </div>

    <div class="players-waiting">
      <div>
        Игра #{{ props.game?.id }}
      </div>
      <div>
        Ожидаем игроков... ({{ props.game?.players.length }})
      </div>
      <button
          @click="emits('exit')"
          class="btn exit-btn"
      >
        Выйти из игры
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  game: never
  selectedColor: string | null
}>();

const emits = defineEmits(["selectColor", "exit"]);
</script>

<style scoped>
.color-selection {
  text-align: center;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
  margin-bottom: 20px;
}

.color-palette {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin: 20px 0;
}

.color-option {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: transform 0.2s;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.selected {
  border-color: #333;
  transform: scale(1.2);
}

.players-waiting {
  margin-top: 20px;
}
</style>
