<template>
  <div class="auth-container">
    <AuthCard>
      <template #title>Регистрация</template>
      <template #form>
        <AuthForm
            :loading="loading"
            :error="error"
            @submit="handleRegister"
            submit-text="Зарегистрироваться"
            loading-text="Регистрация..."
        >
          <AuthInput
              v-model="form.username"
              label="Логин"
              type="text"
              placeholder="Придумайте логин"
              autocomplete="username"
              :minlength="3"
              :maxlength="32"
              required
          />
          <AuthInput
              v-model="form.password"
              label="Пароль"
              type="password"
              placeholder="Придумайте пароль"
              autocomplete="new-password"
              :minlength="3"
              :maxlength="8"
              required
          />
        </AuthForm>
      </template>
      <template #footer>
        <AuthFooter
            text="Уже есть аккаунт?"
            button-text="Войти"
            to="/login"
        />
      </template>
    </AuthCard>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive} from "vue";
import {useRouter} from "vue-router";
import {registerUser} from "../api.js";
import AuthForm from "../components/AuthForm.vue";
import AuthCard from "../components/AuthCard.vue";
import AuthInput from "../components/AuthInput.vue";
import AuthFooter from "../components/AuthFooter.vue";

const router = useRouter();

const form = reactive({
  username: null,
  password: null
});
const loading = ref(false);
const error = ref(null);

const handleRegister = async () => {
  error.value = null;
  loading.value = true;

  try {
    const response = await registerUser(form.username, form.password);
    localStorage.setItem("token", response.result.token);
    await router.push("/game");
  } catch (err) {
    error.value = err.message || "Ошибка регистрации";
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
