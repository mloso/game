<template>
  <div class="auth-switch">
    <span>{{ props.text }}</span>
    <router-link
        :to="props.to"
        class="switch-button"
    >
      {{ props.buttonText }}
    </router-link>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  text: string,
  buttonText: string,
  to: string
}>();
</script>

<style scoped>
.auth-switch {
  text-align: center;
  color: #666;
}

.switch-button {
  background: none;
  border: none;
  color: #42b983;
  cursor: pointer;
  font-weight: 500;
  margin-left: 5px;
  padding: 5px;
}

.switch-button:hover {
  text-decoration: underline;
}
</style>
