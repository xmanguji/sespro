<template>
  <div class="login-page">
    <div class="login-container">

      <div class="text-Primary text-left" @click="onBack()">Welcome</div>

      <h3 class="text-left text-3xl font-black">Don't have an account?</h3>

      <div class="logo-container">
        <img src="../assets/images/Respro_Health&Safety.svg" style="height: 150px;" />
      </div>

      <div class="button-container w-full">
        <p class="text-base mt-8">Your company needs to have an existing Respro account to use this app.</p>
        <p class="textt-base mt-4">If your company already has a Respro account, please ask the Account Owner to invite you. Thanks!</p>
      </div>
    </div>
  </div>
</template>

<script>
import router from "@/routes";

export default {
  methods: {
    onBack(){
      router.push({ name: "login" });
    }
  }
}
</script>

<style scoped>
.login-page {
  height: 100%;
  padding: 12px;
  margin-top: 20px;
}
.login-container {
  width: 100%;
}
.logo-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 8%;
}

.login-text {
  text-align: center;
  font-size: 28px;
  font-weight: 500;
  cursor: pointer;
}

.button-container {
  width: 100%;
  justify-content: center;
}
</style>
