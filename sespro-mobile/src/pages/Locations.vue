<template v-slot:default>
<div class="rounded-t-lg">
  <div class="flex justify-center">
    <img class="w-24 mt-12" src="@/assets/images/icons/icon_premise.png" />
  </div>
  <div class="text-4xl font-black text-black mt-12">Premise selection</div>
    <div class="text-base mt-12">Please select a location. </div>
     <div class="list-container mt-2 max-w-4xl my-0 -mx-1 lg:m-auto">
        <div
          v-for="p in this.premises"
          :key="p.uuid"
          class="list-view"
          @click="select(p.uuid)"
        >
          <div>
            <img class="w-8" src="@/assets/images/icons/icon_premise.png" />
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
    premises: sync("app/premises"),
    audits: sync("audit/audits"),
    audit: sync("audit/audits[:currentAuditIndex]"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
  },
  data() {
    return {
      defaultImage: defaultImage,
    };
  },
  methods: {
    select(uuid) {
      let val = this.audits.find((item) => item.premiseUuid === uuid);
      this.currentAuditIndex = val.auditIndex;
      this.audit.location = val.premiseUuid;
      router.push({ name: "home" });
    },
    onBack() {
      this.currentAuditIndex = -1;
      this.$router.push({ name: "home" });
      console.log("User voluntarily stopped location selection");
    },
  },
};
</script>

<style lang="scss" scoped>
.main-container {
  background-color: white;
  .list-container {
    padding: 1rem 0;
    .list-view {
      border-bottom: 1px solid #e2e2e3;
    }
  }
}
.list-view label {
  font-size: 18px;
  color: #4a4d4a;
  cursor: pointer;
}
</style>
