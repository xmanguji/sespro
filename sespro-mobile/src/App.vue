<template>
  <div id="app">
    <router-view :key="$route.path"></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
};
</script>

<style>
html {
  overflow-y: hidden;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  height: 100% !important;
}

@font-face {
  font-family: "AvenirLTStd-Roman";
  src: url("assets/fonts/AvenirLTStd-Roman.otf") format("opentype");
}

* {
  font-family: "AvenirLTStd-Roman", serif;
}

</style>
