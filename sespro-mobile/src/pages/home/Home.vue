<template>
  <AppLayout :scrollable="true" :imageLogo="defaultImage" headerTitle="">

    <template v-slot:default>

      <div class="background-container h-80 w-full flex justify-center items-center mt-5 rounded-2xl relative">
        <img class="w-28" src="../../assets/images/Respro_logo.png" />
        <div class="text-Primary font-bold bg-gray-300 w-32 text-base pt-1 rounded-xl absolute right-4 bottom-4" @click="onAudit">START AUDIT</div>
      </div>

      <div class="flex flex-row mt-4 max-w-4xl lg:mx-auto">
        <div class="flex-1 flex flex-row justify-end"></div>
      </div>

      <div class="list-container shadow-xl p-0 max-w-4xl lg:mx-auto mb-40">
        <div class="p-4">
          <div class="list-view" @click="onPremises">
            <div>
              <img class="w-8" src="../../assets/images/icons/icon_premise.png" />
              <label>{{ labelPremise }}</label>
            </div>
            <img class="w-5" src="../../assets/images/icons/icon_right_arrow.png" />
          </div>
          <div class="list-view" @click="onTemplates">
            <div>
              <img class="w-8" src="../../assets/images/icons/icon_audit.png" />
              <label>{{ labelTemplates }}</label>
            </div>
            <img class="w-5" src="../../assets/images/icons/icon_right_arrow.png" />
          </div>
          <div class="list-view" @click="onLogout">
            <div>
              <img class="w-8" src="../../assets/images/icons/icon_logout.png" />
              <label>{{ logout }}</label>
            </div>
            <img class="w-5" src="../../assets/images/icons/icon_right_arrow.png"/>
          </div>
        </div>
      </div>
      
    </template>
  </AppLayout>
</template>
<script>
import router from "../../routes";
import AppLayout from "../../layouts/AppLayout";
import { sync } from "vuex-pathify";
import ImageLogo from "@/assets/images/Respro_Health&Safety.svg";
import Repeat from "vue-material-design-icons/Repeat.vue";
import Play from "vue-material-design-icons/Play.vue";

export default {
  name: "Home",
  components: { AppLayout, Repeat, Play },
  data() {
    return {
      defaultImage: ImageLogo,
      audit: "Respro Audit",
      labelPremise: "Select Premise",
      labelTemplates: "Select Audit",
      logout: "Logout",
    };
  },
  computed: {
    premises: sync("app/premises"),
    templates: sync("template/templates"),
    selectedTemplateIndex: sync("template/selectedTemplateIndex"),
    token: sync("app/session"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    auditItem: sync("audit/audits[:currentAuditIndex]"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
  },
  methods: {
    onAudit() {
      if (this.location) router.push({ name: "audit" });
      else this.onPremises();
    },
    onPremises() {
      router.push({ name: "premises" });

      // if (this.premises.length > 1) {
      //   router.push({ name: "premises" });
      // } else if (this.premises.length === 1) {
      //   this.currentAuditIndex = 0;
      //   this.auditItem.location = this.premises[0].uuid;
      //   router.push({ name: "audit" });
      // } else {
      //   this.$buefy.dialog.alert(
      //     "No locations found. If you expect to see a new location, try logging out first."
      //   );
      // }
    },
    onTemplates() {
      router.push({ name: "templates" });
    },
    onDisclaimer() {
      router.push({ name: "legal" });
    },
    onTutorial() {
      router.push({ name: "tutorial" });
    },
    signOut() {
      this.token = "invalid";
      router.push({ name: "login" });
      console.log("Session terminated - token wiped");
    },
    onLogout() {
      this.$buefy.dialog.confirm({
        message: "Are you sure you want to log out?",
        onConfirm: () => this.signOut(),
      });
    },
  },
  mounted() {
    if (this.location) {
      this.labelPremise = this.premises.find(
        (item) => item.uuid == this.location
      ).name;
    }
    if (this.selectedTemplateIndex > -1) {
      this.labelTemplates = this.templates[this.selectedTemplateIndex].name;
    }
  },
};
</script>

<style lang="scss" scoped>
.background-container {
  background-size: cover;
  background-position: center;
  background-image: url(../../assets/images/25101.jpg);
}
.logo {
  height: 60%;
}

.banner-center {
  top: 40%;
  position: absolute;
  left: 50%;
  width: 100%;
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}

.banner-center img {
  margin: auto;
}
.banner-container:after {
  padding-bottom: 100%;
  content: "";
  display: block;
}

@media (max-width: 850px) {
  .header-container {
    min-height: 55px;
  }
  .header-container img {
    height: 50px;
  }
}
</style>
