<template>
  <div class="h-full flex flex-row bg-sonicSilver">
    <div class="items-start flex gap-y-10 flex-col bg-indigo w-72">
      <div class="pl-8 flex mt-8 flex flex-row">
        <img :src="imageLogo" class="w-24" @click="toDashboard" />
        <span class="text-gray-500">1.52</span>
      </div>
      <div class="flex flex-col w-full">
        <div class="pl-8 flex w-full pb-1 pt-2 hover:bg-indigoLight border-b border-gray-700">
          <div class="flex items-end justify-center h-12" @click="toDashboard">
            <ViewDashboard class="h-10 mr-3 text-white" />
            <label class="h-10 items-end font-bold text-white">Dashboard</label>
          </div>
        </div>
        <div class="pl-8 flex w-full pb-1 pt-2 hover:bg-indigoLight border-b border-gray-700 cursor-pointer"
          @click="toHome">
          <div class="flex items-end justify-center h-12">
            <ViewList class="h-10 mr-3 text-white" />
            <label class="h-10 items-end font-bold text-white cursor-pointer">Audits</label>
          </div>
        </div>
        <div class="pl-8 flex w-full pb-1 pt-2 hover:bg-indigoLight border-b border-gray-700 cursor-pointer"
          @click="toMyAudits">
          <div class="flex items-end justify-center h-12">
            <ViewList class="h-10 mr-3 text-white" />
            <label class="h-10 items-end font-bold text-white cursor-pointer">My Templates</label>
          </div>
        </div>
        <div v-if="userRole == 'ROLE_ROOT' || userRole == 'ROLE_OWNER'" class="pl-8 flex w-full pb-1 pt-2 hover:bg-indigoLight border-b border-gray-700 cursor-pointer"
          @click="toPremises">
          <div class="flex items-end justify-center h-12">
            <Domain class="h-10 mr-3 text-white" />
            <label class="h-10 items-end font-bold text-white cursor-pointer">Premises</label>
          </div>
        </div>
        <div v-if="userRole == 'ROLE_ROOT' || userRole == 'ROLE_OWNER'" class="pl-8 flex w-full pb-1 pt-2 hover:bg-indigoLight border-b border-gray-700 cursor-pointer"
          @click="toUsers">
          <div class="flex items-end justify-center h-12">
            <AccountGroup class="h-10 mr-3 text-white" />
            <label class="h-10 items-end font-bold text-white cursor-pointer">Users </label>
          </div>
        </div>
        <div v-if="userRole == 'ROLE_ROOT'" class="pl-8 flex w-full pb-1 pt-2 hover:bg-indigoLight border-b border-gray-700 cursor-pointer"
          @click="toRoles">
          <div class="flex items-end justify-center h-12">
            <ImageText class="h-10 mr-3 text-white" />
            <label class="h-10 items-end font-bold text-white cursor-pointer">Roles </label>
          </div>
        </div>
        <div class="pl-8 flex w-full pb-1 pt-2 hover:bg-indigoLight border-b border-gray-700 cursor-pointer"
          @click="toReports">
          <div class="flex items-end justify-center h-12">
            <ChartBar class="h-10 mr-3 text-white" />
            <label class="h-10 items-end font-bold text-white cursor-pointer">{{ `Report` }}</label>
          </div>
        </div>
        <div class="pl-8 flex w-full py-1 hover:bg-indigoLight border-b border-gray-700 cursor-pointer" @click="onLogout">
          <div class="flex items-end justify-center h-12">
            <Logout class="h-10 mr-3 text-white" />
            <label class="h-10 items-end font-bold text-white cursor-pointer"> Logout </label>
          </div>
        </div>
      </div>
    </div>
    <div class="flex flex-col w-full h-full bg-white">
      <div>

        <b-loading :is-full-page="true" :active="loading" :can-cancel="false"></b-loading>
        <slot></slot>
      </div>
    </div>
  </div>
</template>
  
<script>
import defaultImage from "@/assets/images/respro-logo.svg";
import router from "@/routes";
import Domain from 'vue-material-design-icons/Domain.vue';
import Logout from 'vue-material-design-icons/Logout.vue';
import AccountGroup from 'vue-material-design-icons/AccountGroup.vue';
import ChartBar from 'vue-material-design-icons/ChartBar.vue';
import ViewList from 'vue-material-design-icons/ViewList.vue';
import ImageText from 'vue-material-design-icons/ImageText.vue';
import ViewDashboard from "vue-material-design-icons/ViewDashboard.vue";

export default {
  name: "AppLayout",
  components: {
    Domain,
    Logout,
    AccountGroup,
    ViewDashboard,
    ViewList,
    ImageText,
    ChartBar
  },
  props: {
    userRole: {
      default: "",
      type: String,
    },
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
      default: "Hygiene Check",
      type: String,
    }
  },
  methods: {
    getImage(imageLogo) {
      return require(imageLogo);
    },
    signOut() {
      this.token = "invalid";
      router.push({ name: "login" });
      console.log("Session terminated - token wiped");
    },
    toHome() {
      if (this.$route.path !== "/home")
        router.push({ name: "home" });
    },
    toMyAudits() {
      if (this.$route.path !== "/mytemplates")
        router.push({ name: "mytemplates" });
    },
    toDashboard() {
      if (this.$route.path !== "/dashboard")
        router.push({ name: "dashboard" });

    },
    toPremises() {
      if (this.$route.path !== "/premises")
        router.push({ name: "premises" });
    },
    toUsers() {
      if (this.$route.path !== "/users")
        router.push({ name: "users" });
    },
    toRoles() {
      if (this.$route.path !== "/roles")
        router.push({ name: "roles" });
    },
    toReports() {
      if (this.$route.path !== "/reports")
        router.push({ name: "reports" });
    },
    onLogout() {
      this.$buefy.dialog.confirm({
        message: "Are you sure you want to log out?",
        onConfirm: () => this.signOut(),
      });
    },
    goBack() {
      this.$router.go(-1)
    }
  },
};
</script>
  
<style lang="scss" scoped>
// .main-container {
//   width: 100%;
//   height: 100%;
//   padding: 0;
//   background-color: #ececec;
//   user-select: none;
// }

// .header-container {
//   width: 100%;
//   height: 72pt;
//   display: flex;
// }

// .header-container img {
//   margin: 2px;
//   max-height: 100%;
// }

// .content-container {
//   height: calc(100% - 80pt);
//   width: 100%;
//   margin: auto;
// }

.back {
  width: 36px;
  cursor: pointer;
  float: left;
}

.header {
  height: 64px;
}

.done-btn {
  border: 1.4px solid #ffffff !important;
  border-radius: 12px !important;
  background-color: #ffffff !important;
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
  