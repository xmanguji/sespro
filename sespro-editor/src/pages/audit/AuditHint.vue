<template>
  <AppLayout :back="true" :submit="true">
    <div class="hint-page">
      <div class="hint-container">
        <div class="text-container">
          <p><vue-simple-markdown :source="hint.text"></vue-simple-markdown></p>
        </div>
        <div>
          <img
            v-for="image in hint.images"
            class="hint-image"
            :src="getImagePath(image)"
            :key="image"
          />
        </div>
      </div>
    </div>
  </AppLayout>
</template>


<script>
import AppLayout from "@/layouts/AppLayout";
export default {
  name: "AuditHint",
  components: { AppLayout },
  props: {
    hint: Object,
  },
  methods: {
    getImagePath(image) {
      // TODO: figure out why this works
      let images = require.context(
        "../../assets/images/hints/",
        false,
        /\.jpg$/
      );
      return images("./" + image + ".jpg");
    },
  },
};
</script>

<style lang="scss" scoped>
.main-container {
  background-color: white;
}
.hint-page {
  height: 100%;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 -1rem;
}

.hint-container {
  height: 100%;
  width: 50%;
  background-color: #ffffff;
  border-radius: 2px;
  padding: 0;
  margin: auto;
  overflow-y: scroll;
  display: flex;
  flex-direction: column;
}

.text-container {
  width: 100%;
  text-align: left;
  font-size: 16px;
  font-weight: 500;
  padding: 20px;
}

.hint-image {
  min-width: 100%;
}

@media (max-width: 850px) {
  .hint-container {
    height: 100%;
    width: 100%;
  }
}
</style>
