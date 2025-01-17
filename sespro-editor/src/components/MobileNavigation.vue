<template>
  <div>
    <transition
      enter-class="opacity-0"
      leave-to-class="opacity-0"
      enter-to-class="opacity-100"
      leave-class="opacity-100"
      enter-active-class="transition-opacity ease-linear duration-150"
      leave-active-class="transition-opacity ease-linear duration-150"
    >
      <div
        v-if="showMenuContent"
        @click="showMenuContent = false"
        class="z-50 fixed inset-0 bg-gray-600 dark:bg-white bg-opacity-50 dark:bg-opacity-50"
        aria-hidden="true"
      ></div>
    </transition>

    <transition
      enter-class="-translate-x-full"
      leave-to-class="-translate-x-full"
      enter-to-class="translate-x-0"
      leave-class="translate-x-0"
      enter-active-class="transition ease-in-out duration-200 transform"
      leave-active-class="transition ease-in-out duration-150 transform"
    >
      <div
        v-if="showMenuContent"
        class="z-50 fixed inset-0 flex lg:hidden pointer-events-none"
        role="dialog"
        aria-modal="true"
      >
        <!-- @after-leave="menuOpen = false" -->
        <!-- v-if="showMenuContent" -->
        <div
          class="relative flex-1 flex flex-col max-w-xs w-full pt-5 pb-4 bg-white dark:bg-gray-700 dark:shadow pointer-events-auto"
        >
          <div class="absolute top-0 right-0 -mr-12 pt-2">
            <button
              @click="showMenuContent = false"
              type="button"
              class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            >
              <span class="sr-only">Close sidebar</span>
              <svg
                class="h-6 w-6 text-white"
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
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <router-link to="/" class="flex-shrink-0 flex items-center px-4">
            <img
              class="h-8 w-auto"
              src="@/assets/images/logo-h.png"
              alt="Workflow"
            />
          </router-link>
          <div class="mt-5 flex-1 h-0 overflow-y-auto">
            <nav class="px-2" id="mobile-navigation">
              <div class="space-y-1">
                <router-link
                  v-for="(link, index) in links"
                  :key="`dekstop-navbar-link-${index}`"
                  :to="link.url"
                  class="text-gray-700 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800 group flex items-center px-2 py-3 text-sm font-medium rounded-md"
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
                      class="text-gray-400 group-hover:text-gray-500"
                    ></i>
                  </span>
                  {{ link.label }}
                </router-link>
              </div>
            </nav>
          </div>
          <div class="px-4 flex justify-center">
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
          </div>
        </div>
        <div class="flex-shrink-0 w-14" aria-hidden="true">
          <!-- Dummy element to force sidebar to shrink to fit close icon -->
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";

export default {
  props: ["links", "routeIsActive"],
  data() {
    return {
      showMenuContent: false,
    };
  },
  computed: {
    ...mapState(["darkMode"]),
  },
  mounted() {
    this.$root.$on(
      "open-mobile-navigation",
      () => (this.showMenuContent = true)
    );
  },
  methods: {
    ...mapMutations(["toggleDarkMode"]),
  },
};
</script>
