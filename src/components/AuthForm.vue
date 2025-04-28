<template>
  <form
      @submit.prevent="emits('submit')"
      class="auth-form"
  >
    <slot/>
    <button
        type="submit"
        class="auth-button"
        :disabled="props.loading"
    >
      <span v-if="props.loading">{{ props.loadingText }}</span>
      <span v-else>{{ props.submitText }}</span>
    </button>
    <div
        v-if="props.error"
        class="error-message"
    >
      {{ props.error }}
    </div>
  </form>
</template>

<script setup lang="ts">
const props = defineProps(
    {
      loading: Boolean,
      error: String,
      submitText: {
        type: String,
        default: "Войти"
      },
      loadingText: {
        type: String,
        default: "Вход..."
      }
    }
);

const emits = defineEmits(["submit"]);
</script>

<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.auth-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.auth-button:hover {
  background-color: #3aa876;
}

.auth-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #ff4444;
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
}
</style>
