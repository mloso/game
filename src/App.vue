<template>
  <router-view/>
</template>

<script setup>
import {onMounted} from "vue";
import {useRouter} from "vue-router";

const router = useRouter();

onMounted(async () => {
  const isAuthenticated = localStorage.getItem("access_token");
  if (isAuthenticated && window.location.pathname === "/") {
    await router.push({name: "game"});
  }
});
</script>
