<template>
  <div>
    <div class="flex justify-center">
      <img class="w-24 mt-12" src="@/assets/images/icons/icon_audit.png" />
    </div>
    <div class="text-4xl font-black text-black mt-12">Audit selection</div>
    <div class="text-base mt-12">Please select an audit. </div>
    <div class="list-container">
      <div v-for="p in this.templates" :key="p.uuid" class="list-view" @click="select(p.uuid)">
        <div>
          <img class="w-8" src="@/assets/images/icons/icon_audit.png" />
          <label>{{ p.name }}</label>
        </div>
        <img class="w-5" src="@/assets/images/icons/icon_right_arrow.png" />
      </div>
    </div>
  </div>
</template>

<script>
import AppLayout from "@/layouts/AppLayout";
import { sync } from "vuex-pathify";
import router from "@/routes";
import defaultImage from "@/assets/images/Respro_Health&Safety.svg";

export default {
  components: { AppLayout },
  computed: {
    templates: sync("template/templates"),
    selectedTemplateIndex: sync("template/selectedTemplateIndex"),
  },
  data() {
    return {
      defaultImage: defaultImage,
    }
  },
  methods: {
    select(uuid) {
      let val = this.templates.find((item) => item.uuid === uuid);
      this.selectedTemplateIndex = this.templates.indexOf(val);
      router.push({ name: "home" })
    },
    onBack() {
      this.selectedTemplateIndex = -1;
      this.$router.push({ name: "home" });
      console.log("User voluntarily stopped location selection");
    },
  },
};
</script>

<style  scoped></style>
