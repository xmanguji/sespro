<template>
  <div class="login-page">
    <div class="login-container">
      <div class="logo-container">
        <img
          src="@/assets/images/Respro_health_and_safety_blue_bg.png"
          style="height: 150px;"
        />
      </div>
      <div class="login-text">
        <span>Help</span>
      </div>
      <div class="button-container">
        <h3>Don't have an account?</h3>
        <p>
          You need an existing Respro account to use this app. If your
          organization already has Respro, refer to the account manager(s) for
          details.
        </p>
        <p>
          If you want to create a new Respro account for your organization, you
          need to contact Respro.
          <!-- <a class="hover:text-editIconColor" href="https://hygienecheck.net/"
            >contact us.</a
          > -->
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.login-page {
  width: 100%;
  height: 100%;
  padding: 0;
  background-color: #1d3e57;
  user-select: none;
}
.login-container {
  overflow-y: auto;
  height: 100%;
  width: 50%;
  margin: auto;
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
  color: white;
  font-weight: 500;
  cursor: pointer;
}

.button-container {
  align-content: center;
  color: white;
}

@media (max-width: 850px) {
  .login-container {
    width: 80%;
  }
  .logo-container {
    margin-top: 15%;
  }
  .login-text {
    font-size: 24px;
    font-weight: 500;
  }
}
@media (max-width: 600px) {
  .login-text {
    margin-top: 5%;
  }
}
</style>
