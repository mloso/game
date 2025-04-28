<template>
  <div class="stats-container">
    <h3>Глобальная статистика</h3>
    <div class="stats-grid">
      <div class="stat-item">
        <div class="stat-value">
          {{ props.stats.total_games }}
        </div>
        <div class="stat-label">
          Всего игр
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-value">
          {{ props.stats.successfully_clicks || 0 }}
        </div>
        <div class="stat-label">
          Удачных ходов
        </div>
      </div>
      <div class="stat-item">
        <div class="stat-value">
          {{ props.stats.unsuccessfully_clicks || 0 }}
        </div>
        <div class="stat-label">
          Неудачных ходов
        </div>
      </div>
      <div class="stat-item">
        <div
            class="stat-color"
            :style="{ backgroundColor: props.stats.most_used_color }"
        ></div>
        <div class="stat-label">
          Популярный цвет
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  stats: {
    total_games: number
    successfully_clicks: number
    unsuccessfully_clicks: number
    most_used_color: string
  }
}>();
</script>

<style scoped>
.stats-container {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-top: 10px;
}

.stat-item {
  text-align: center;
  padding: 10px;
  background: white;
  border-radius: 6px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #42b983;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.stat-color {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 auto;
  border: 2px solid #ddd;
}
</style>
