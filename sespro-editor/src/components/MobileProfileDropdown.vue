<template>
  <dropdown class="ml-3 relative" v-slot="{ isOpen }">
    <dropdown-trigger
      class="max-w-xs bg-white dark:bg-gray-800 flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
    >
      <span class="sr-only">Open user menu</span>
      <img
        class="h-8 w-8 rounded-full"
        :src="profilePicture"
        :alt="''"
      />
    </dropdown-trigger>

    <transition
      enter-active-class="transition ease-out duration-100"
      enter-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <dropdown-menu
        v-show="isOpen"
        class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white dark:bg-gray-700 border border-transparent dark:border-gray-800 ring-1 ring-black ring-opacity-5 divide-y divide-gray-200 focus:outline-none"
      >
        <div class="py-1" role="none">
          <!-- Active: "bg-gray-100 text-gray-900", Not Active: "text-gray-700" -->
          <router-link
            :to="{ name: 'settings' }"
            class="text-gray-700 dark:text-gray-300 block px-4 py-2 text-sm hover:bg-gray-100 hover:text-gray-900 dark:hover:bg-gray-800 dark:hover:text-gray-100"
            role="menuitem"
            tabindex="-1"
            id="user-menu-item-0"
            >View profile</router-link
          >
          <!-- <a
            href="#"
            class="text-gray-700 dark:text-gray-300 block px-4 py-2 text-sm hover:bg-gray-100 hover:text-gray-900 dark:hover:bg-gray-800 dark:hover:text-gray-100"
            role="menuitem"
            tabindex="-1"
            id="user-menu-item-1"
            >Settings</a
          > -->
          <router-link
            :to="{ name: 'notifications' }"
            class="text-gray-700 dark:text-gray-300 block px-4 py-2 text-sm hover:bg-gray-100 hover:text-gray-900 dark:hover:bg-gray-800 dark:hover:text-gray-100"
            role="menuitem"
            tabindex="-1"
            id="user-menu-item-2"
            >Notifications</router-link
          >
          <router-link
            :to="{ name: 'settings' }"
            class="text-gray-700 dark:text-gray-300 block px-4 py-2 text-sm hover:bg-gray-100 hover:text-gray-900 dark:hover:bg-gray-800 dark:hover:text-gray-100"
            role="menuitem"
            tabindex="-1"
            id="options-menu-item-1"
            >Settings</router-link
          >
        </div>
        <!-- <div class="py-1" role="none">
          <a
            href="#"
            class="text-gray-700 dark:text-gray-300 block px-4 py-2 text-sm hover:bg-gray-100 hover:text-gray-900 dark:hover:bg-gray-800 dark:hover:text-gray-100"
            role="menuitem"
            tabindex="-1"
            id="user-menu-item-4"
            >Support</a
          >
        </div> -->
        <div class="py-1" role="none">
          <button
            @click="$store.commit('logout')"
            type="button"
            class="w-full text-left text-gray-700 dark:text-gray-300 block px-4 py-2 text-sm hover:bg-gray-100 hover:text-gray-900 dark:hover:bg-gray-800 dark:hover:text-gray-100 focus:outline-none"
            role="menuitem"
            tabindex="-1"
            id="user-menu-item-5"
          >
            Logout
          </button>
        </div>
      </dropdown-menu>
    </transition>
  </dropdown>
</template>

<script>
import { mapState } from "vuex";
import {
  Dropdown,
  DropdownMenu,
  DropdownTrigger,
} from "@/components/elements/Dropdown";

export default {
  components: {
    Dropdown,
    DropdownMenu,
    DropdownTrigger,
  },
  computed: {
    ...mapState(["user"]),
    profilePicture() {
      return "placeholder";
    },
  },
};
</script>
