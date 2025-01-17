<template>
  <AppLayout :scrollable="true" :imageLogo="defaultImage" headerTitle="Premise Selection" :back="true" @back="onBack">
    <div class="list-container bg-white">
      <div
        v-for="p in this.premises"
        :key="p.uuid"
        class="list-view ml-4 mr-2"
        @click="select(p.uuid)"
      >
        <div>
          <img class="w-8" src="@/assets/images/icons/icon_premise.png" />
          <label>{{ p.name }}</label>
        </div>
        <img class="w-5" src="@/assets/images/icons/icon_right_arrow.png" />
      </div>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from "@/layouts/AppLayout";
import { sync } from "vuex-pathify";
import router from "@/routes";
import defaultImage from "@/assets/images/Respro_health_and_safety_blue_bg.png";

export default {
  components: { AppLayout },
  computed: {
    premises: sync("app/premises"),
    activeUserRole: sync("app/activeUserRole"),
    audits: sync("audit/audits"),
    audit: sync("audit/audits[:currentAuditIndex]"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
  },
  data() {
    return {
      defaultImage: defaultImage,
    }
  },
  methods: {
    select(uuid) {
      let val = this.audits.find((item) => item.premiseUuid === uuid);
      this.currentAuditIndex = val.auditIndex;
      this.audit.location = val.premiseUuid
      router.push({name:"home"})
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
    margin: 0 -1rem;
    padding: 1rem 0;
    .list-view{
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
