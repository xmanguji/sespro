<template>
  <div class="h-screen flex overflow-hidden bg-white dark:bg-gray-700">
    <!-- Off-canvas menu for mobile, show/hide based on off-canvas menu state. -->
    <mobile-navigation
      :links="links"
      :route-is-active="routeIsActive"
    ></mobile-navigation>

    <!-- Static sidebar for desktop -->
    <main-navigation
      class="hidden lg:flex lg:flex-shrink-0"
      :links="links"
      :route-is-active="routeIsActive"
    ></main-navigation>

    <!-- Main column -->
    <div class="flex flex-col w-0 flex-1 overflow-hidden">
      <!-- Search header -->
      <div
        class="relative z-10 flex-shrink-0 flex h-16 bg-white dark:bg-gray-700 border-b border-gray-200 dark:border-gray-800 lg:hidden"
      >
        <button
          @click="openMobileNavigation"
          type="button"
          class="px-4 border-r border-gray-200 dark:border-gray-800 text-gray-500 dark:text-gray-400 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 lg:hidden"
        >
          <span class="sr-only">Open sidebar</span>
          <svg
            class="h-6 w-6"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h8m-8 6h16"
            />
          </svg>
        </button>
        <div class="flex-1 flex justify-end px-4 sm:px-6 lg:px-8">
          <div class="flex items-center">
            <mobile-profile-dropdown></mobile-profile-dropdown>
          </div>
        </div>
      </div>
      <transition
        enter-class="opacity-0"
        enter-to-class="opacity-100"
        enter-active-class="transition duration-150"
        leave-class="opacity-100"
        leave-to-class="opacity-0"
        leave-active-class="transition duration-100"
      >
        <div
          class="flex-1 flex flex-col relative z-0 overflow-y-auto focus:outline-none"
        >
          <main class="flex-1 dark:bg-gray-700 transition">
            <slot></slot>
          </main>
          <footer
            key="footer"
            class="flex-shrink-0 mt-8 py-6 pb-4 dark:bg-gray-800 transition"
          >
            <p class="text-center text-sm text-gray-600 dark:text-gray-200">
              {{ year }} &copy; Jounce Media
            </p>
          </footer>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { mixin as clickaway } from "vue-clickaway";
import { mapState } from "vuex";
import MainNavigation from "@/components/MainNavigation";
import MobileNavigation from "@/components/MobileNavigation";
import MobileProfileDropdown from "@/components/MobileProfileDropdown";

export default {
  mixins: [clickaway],
  components: {
    MainNavigation,
    MobileNavigation,
    MobileProfileDropdown,
  },
  data: () => ({
    links: [
      {
        label: "Reports",
        icon: "fas fa-file",
        url: "/reporting",
      }
    ],
    menuOpen: false,
    userPorfileDropdownOpen: false,
  }),
  computed: {
    ...mapState(["user"]),
    year() {
      return new Date().getFullYear();
    },
  },
  methods: {
    routeIsActive(route) {
      const paths = Array.isArray(route) ? route : [route];
      return paths.some((path) => {
        return this.$route.path.indexOf(path) === 0;
      });
    },
    openMobileNavigation() {
      this.$root.$emit("open-mobile-navigation");
    },
  },
};
</script>
