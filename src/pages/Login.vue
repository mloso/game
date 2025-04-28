<template>
  <div class="auth-container">
    <AuthCard>
      <template #title>Вход в игру</template>
      <template #form>
        <AuthForm
            :loading="loading"
            :error="error"
            @submit="handleLogin"
        >
          <AuthInput
              v-model="form.username"
              label="Логин"
              type="text"
              placeholder="Введите ваш логин"
              autocomplete="username"
              required
          />
          <AuthInput
              v-model="form.password"
              label="Пароль"
              type="password"
              placeholder="Введите пароль"
              autocomplete="current-password"
              :minlength="3"
              :maxlength="8"
              required
          />
        </AuthForm>
      </template>
      <template #footer>
        <AuthFooter
            text="Нет аккаунта?"
            button-text="Зарегистрироваться"
            to="/register"
        />
      </template>
    </AuthCard>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive} from "vue";
import {useRouter} from "vue-router";
import {loginUser} from "../api.js";
import AuthInput from "../components/AuthInput.vue";
import AuthForm from "../components/AuthForm.vue";
import AuthCard from "../components/AuthCard.vue";
import AuthFooter from "../components/AuthFooter.vue";


const router = useRouter();

const form = reactive({
  username: null,
  password: null
});
const loading = ref(false);
const error = ref(null);

const handleLogin = async () => {
  error.value = null;
  loading.value = true;

  try {
    const response = await loginUser(form.username, form.password);
    localStorage.setItem("token", response.result.token);
    await router.push("/game");
  } catch (err) {
    error.value = err.message || "Ошибка входа";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}
</style>
