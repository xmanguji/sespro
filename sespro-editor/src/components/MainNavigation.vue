<template>
  <div class="h-full">
    <div
      class="flex flex-col w-72 border-r border-gray-200 dark:border-black pt-5 pb-4 bg-gray-100 dark:bg-gray-900 transition"
    >
      <router-link class="flex items-center flex-shrink-0 px-6" to="/">
        <img src="@/assets/jounce-black-logo.png" class="h-14" />
      </router-link>
      <!-- Sidebar component, swap this element with another sidebar if you like -->
      <div class="h-0 flex-1 flex flex-col overflow-y-auto">
        <!-- User account dropdown -->

        <!-- Navigation -->
        <nav class="px-3 mt-6" id="main-navigation">
          <div class="space-y-1">
            <!-- Current: "bg-gray-200 text-gray-900", Default: "text-gray-700 hover:text-gray-900 hover:bg-gray-50" -->
            <router-link
              v-for="(link, index) in links"
              :key="`dekstop-navbar-link-${index}`"
              :to="link.url"
              class="text-gray-700 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-50 dark:hover:bg-black group flex items-center px-2 py-2 text-sm font-medium rounded-md"
              :class="{
                'is-active': routeIsActive(link.url) && link.url !== '/',
              }"
              aria-current="page"
              exact
            >
              <span
                class="mr-3 flex-shrink-0 inline-flex w-6 items-center justify-center"
              >
                <i
                  :class="link.icon"
                  class="text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-200"
                ></i>
              </span>
              {{ link.label }}
            </router-link>
          </div>
        </nav>
      </div>
      <!-- <div class="px-4 flex justify-center">
        <button
          type="button"
          class="inline-block p-2 rounded-full focus:outline-none"
          @click="toggleDarkMode"
        >
          <transition
            mode="out-in"
            enter-class="transform -translate-x-full opacity-0"
            enter-to-class="transform translate-x-0 opacity-100"
            leave-class="transform translate-x-0 opacity-100"
            leave-to-class="transform translate-x-full opacity-0"
            enter-active-class="transition"
            leave-active-class="transition"
          >
            <i key="moon" v-if="!darkMode" class="fas fa fa-moon"></i>
            <i key="sun" v-else class="text-gray-200 fas fa fa-sun"></i>
          </transition>
        </button>
      </div> -->
    </div>
  </div>
</template>

<script>
import { mixin as clickaway } from "vue-clickaway";
import { mapState, mapMutations } from "vuex";

import SidebarSearch from "@/components/SidebarSearch";
import HorizontalLogo from "@/components/logos/Horizontal";

export default {
  mixins: [clickaway],
  props: ["links", "routeIsActive"],
  data() {
    return {
      profileDropdownOpen: false,
    };
  },
  computed: {
    ...mapState(["user", "darkMode"]),
    // todo: add a placeholder image when there is no profile picture
    profilePicture() {
      return "placeholder";
    },
  },
  watch: {
    darkMode(val) {
      const body = document.querySelector("body");
      val ? body.classList.add("dark") : body.classList.remove("dark");
    },
  },
  methods: {
    ...mapMutations(["toggleDarkMode"]),
    logout() {
      window.localStorage.setItem("ts-token", "");
      this.$store.commit("setToken", null);
      this.$store.commit("setUser", null);
      this.$router.push("/");
      this.$success("Logged Out", "Successfully logged out!");
    },
    closeProfileDropdown() {
      this.profileDropdownOpen = false;
    },
  },
  components: {
    SidebarSearch,
    HorizontalLogo,
  },
};
</script>
