<template>
  <div class="lobby">
    <h1>Игра</h1>
    <div class="action-buttons">
      <button
          @click="emits('create')"
          class="btn"
      >
        Создать игру
      </button>
      <div class="join-game">
        <input
            v-model="joinGameId"
            placeholder="ID игры"
        />
        <button
            @click="emits('join')"
            class="btn"
        >
          Присоединиться
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed} from "vue";

const props = defineProps<{
  joinGameId: string | null
}>();

const emits = defineEmits(["create", "join", "update:joinGameId"]);

const joinGameId = computed({
  get: () => props.joinGameId,
  set: (value) => emits("update:joinGameId", value)
});
</script>

<style scoped>
.lobby {
  text-align: center;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
  margin-bottom: 20px;
}

.join-game {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.join-game input {
  flex: 1;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}
</style>
