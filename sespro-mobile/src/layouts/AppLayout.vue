<template>
  <div class="main-container">
    <div
      class="
        items-end
        flex flex-row
        justify-center
        bg-PrimaryDark
        h-28
        border-yellow-500	
        border-b-4
        pb-3
      "
    >
      <div v-if="back" class="flex-row items-center text-white absolute left-4 pb-3" @click="onBack()">
        <img src="@/assets/images/backIcon.png" class="h-6" />
      </div>
        <img src="@/assets/images/tree1.png" class="h-14" />
      <div class="flex flex-row bg-blue-700">
        <slot name="first"></slot>
      </div>
    </div>
    <div
      class="content-container"
      :style="scrollable ? 'overflow-y: scroll' : ''"
    >
      <b-loading
        :is-full-page="true"
        :active="loading"
        :can-cancel="false"
      ></b-loading>
      <slot></slot>
    </div>
  </div>
</template>

<script>
import defaultImage from "@/assets/images/tree.png";
import router from "@/routes";

export default {
  name: "AppLayout",
  props: {
    back: {
      default: false,
      type: Boolean,
    },
    loading: {
      default: false,
      type: Boolean,
    },
    scrollable: {
      default: true,
      type: Boolean,
    },
    submit: {
      default: false,
      type: Boolean,
    },
    imageLogo: {
      default: defaultImage,
      type: String,
    },
    headerTitle: {
      default: "Respro",
      type: String,
    },
  },
  methods: {
    getImage(imageLogo) {
      return require(imageLogo);
    },
    onBack(){
      router.go(-1);
    }
  },
};
</script>

<style lang="scss" scoped>
.main-container {
  width: 100%;
  height: 100%;
  padding: 0;
  user-select: none;
}

.header-container {
  width: 100%;
  height: 64pt;
  display: flex;
  background-color: "#1d3e57";
}

.header-container img {
  margin: 2px;
  max-height: 100%;
}

.content-container {
  height: calc(100% - 80pt);
  width: 94%;
  margin: auto;
  background-color: #f4f4f4;
}

.back {
  width: 36px;
  cursor: pointer;
  float: left;
}

.header {
  max-height: 100%;
}

.done-btn {
  border: 1.4px solid #ffffff !important;
  border-radius: 12px !important;
  background-color: #4173ac !important;
  color: #ffffff;
}

@media (max-width: 850px) {
  .header-container {
    min-height: 55px;
  }

  .header-container img {
    max-height: 50px;
  }

  .back {
    height: 36px;
    width: 55px;
  }

  .content-container {
    width: 100%;
    padding-left: 1rem;
    padding-right: 1rem;
    // padding-top: 5rem;
  }

  .header {
    max-width: 200px;
  }

  .done-btn {
    width: 50px !important;
  }
}

@media (max-width: 360px) {
  .header-container {
    height: 60pt;
  }
  .content-container {
    height: calc(100% - 60pt);
  }
  .header-container h2 {
    font-size: 24px;
    line-height: 32px;
  }
}
</style>
