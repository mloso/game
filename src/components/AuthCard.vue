<template>
  <div class="auth-card">
    <h1 class="auth-title">
      <slot name="title"></slot>
    </h1>
    <slot name="form"></slot>
    <div class="auth-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<style scoped>
.auth-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 400px;
}

.auth-title {
  text-align: center;
  margin-bottom: 24px;
  color: #333;
  font-size: 24px;
}

.auth-footer {
  margin-top: 20px;
}
</style>
