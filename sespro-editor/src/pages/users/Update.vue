<template>
  <AppLayout :imageLogo="defaultImage" headerTitle="Update User">
    <div
      class="
        px-4
        w-full
        flex flex-col
        justify-center
        items-center
        gap-x-12
        bg-white
        text-PrimaryText
      "
    >
      <form class="w-full max-w-xl mt-8">
        <div class="flex flex-wrap -mx-3 mb-6">
          <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
            <label
              class="
                block
                uppercase
                tracking-wide
                text-gray-700 text-xs
                font-bold
                mb-2
              "
              for="grid-fullname"
            >
              Name
            </label>
            <input
              class="
                appearance-none
                block
                w-full
                bg-gray-200
                text-gray-700
                border border-gray-200
                rounded
                py-3
                px-4
                mb-3
                leading-tight
                focus:outline-none focus:bg-white focus:border-gray-500
              "
              id="grid-fullname"
              type="text"
              placeholder="fullname"
              v-model="fullname"
            />
          </div>
          <div class="w-full md:w-1/2 px-3">
            <label
              class="
                block
                uppercase
                tracking-wide
                text-gray-700 text-xs
                font-bold
                mb-2
              "
              for="grid-last-name"
            >
              Email
            </label>
            <input
              class="
                appearance-none
                block
                w-full
                bg-gray-200
                text-gray-700
                border border-gray-200
                rounded
                py-3
                px-4
                leading-tight
                focus:outline-none focus:bg-white focus:border-gray-500
              "
              id="grid-last-name"
              type="text"
              placeholder="email"
              v-model="email"
            />
          </div>
        </div>
        <div class="flex flex-wrap -mx-3 mb-6">
          <div class="w-full px-3">
            <label
              class="
                block
                uppercase
                tracking-wide
                text-gray-700 text-xs
                font-bold
                mb-2
              "
              for="grid-password"
            >
              Password
            </label>
            <input
              class="
                appearance-none
                block
                w-full
                bg-gray-200
                text-gray-700
                border border-gray-200
                rounded
                py-3
                px-4
                mb-3
                leading-tight
                focus:outline-none focus:bg-white focus:border-gray-500
              "
              id="grid-password"
              type="password"
              placeholder="******************"
              v-model="password"
            />
          </div>
        </div>
        <div class="flex flex-wrap -mx-3 mb-2">
          <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
            <label
              class="
                block
                uppercase
                tracking-wide
                text-gray-700 text-xs
                font-bold
                mb-2
              "
              for="grid-template"
            >
              Templates
            </label>
            <div class="relative">
              <select
                class="
                  block
                  appearance-none
                  w-full
                  bg-gray-200
                  border border-gray-200
                  text-gray-700
                  py-3
                  px-4
                  pr-8
                  rounded
                  leading-tight
                  focus:outline-none focus:bg-white focus:border-gray-500
                "
                id="grid-template"
                v-model="selected_templates"
                multiple
              >
                <option
                  v-for="option in templates"
                  :value="option.uuid"
                  :key="option.name"
                >
                  {{ option.name }}
                </option>
              </select>
              <div
                class="
                  pointer-events-none
                  absolute
                  inset-y-0
                  right-0
                  flex
                  items-center
                  px-2
                  text-gray-700
                "
              >
                <!-- <svg
                  class="fill-current h-4 w-4"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path
                    d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"
                  />
                </svg> -->
              </div>
            </div>
          </div>
          <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
            <label
              class="
                block
                uppercase
                tracking-wide
                text-gray-700 text-xs
                font-bold
                mb-2
              "
              for="grid-premises"
            >
              Premises
            </label>
            <div class="relative">
              <select
                class="
                  block
                  appearance-none
                  w-full
                  bg-gray-200
                  border border-gray-200
                  text-gray-700
                  py-3
                  px-4
                  pr-8
                  rounded
                  leading-tight
                  focus:outline-none focus:bg-white focus:border-gray-500
                "
                id="grid-premises"
                v-model="selected_premises"
                multiple
              >
                <option
                  v-for="option in premises"
                  :value="option.uuid"
                  :key="option.uuid"
                >
                  {{ option.name }}
                </option>
              </select>
              <div
                class="
                  pointer-events-none
                  absolute
                  inset-y-0
                  right-0
                  flex
                  items-center
                  px-2
                  text-gray-700
                "
              >
                <!-- <svg
                  class="fill-current h-4 w-4"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path
                    d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"
                  />
                </svg> -->
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-wrap -mx-3 mb-2 mt-4">
          <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
            <label
              class="
                block
                uppercase
                tracking-wide
                text-gray-700 text-xs
                font-bold
                mb-2
              "
              for="grid-role"
            >
              Role
            </label>
            <div class="relative">
              <select
                class="
                  block
                  appearance-none
                  w-full
                  bg-gray-200
                  border border-gray-200
                  text-gray-700
                  py-3
                  px-4
                  pr-8
                  rounded
                  leading-tight
                  focus:outline-none focus:bg-white focus:border-gray-500
                "
                id="grid-role"
                v-model="role"
              >
                <option
                  v-for="option in roles"
                  :value="option.uuid"
                  :key="option.uuid"
                >
                  {{ option.displayName }}
                </option>
              </select>
              <div
                class="
                  pointer-events-none
                  absolute
                  inset-y-0
                  right-0
                  flex
                  items-center
                  px-2
                  text-gray-700
                "
              >
                <svg
                  class="fill-current h-4 w-4"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                >
                  <path
                    d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"
                  />
                </svg>
              </div>
            </div>
          </div>
          <div class="w-full md:w-1/2 px-3 mb-6 md:mb-0">
            <div class="w-full px-3">
              <label
                class="
                  block
                  uppercase
                  tracking-wide
                  text-gray-700 text-xs
                  font-bold
                  mb-2
                "
                for="grid-is-active"
              >
                Active
              </label>
              <label
                class="
                  appearance-none
                  block
                  w-full
                  text-gray-700
                  bg-gray-200
                  border border-gray-200
                  rounded
                  py-3
                  mb-3
                  leading-tight
                "
              >
                <input
                  class="mr-2 leading-tight"
                  type="checkbox"
                  id="grid-is-active"
                  v-model="isActive"
                />
                <span class="text-sm">Is Active</span>
              </label>
            </div>
          </div>
        </div>
        <div class="flex flex-wrap -mx-3 mb-2 mt-4 justify-end">
          <div
            class="
              w-full
              md:w-1/2
              px-3
              mb-6
              md:mb-0
              flex flex-row
              justify-end
              gap-2
            "
          >
            <button
              class="
                bg-indigoLight
                hover:bg-PrimaryDark
                text-white
                font-bold
                py-2
                px-4
                rounded
              "
              @click="cancel"
            >
              Cancel
            </button>
            <!-- <button
              class="
                bg-indigoLight
                hover:bg-PrimaryDark
                text-white
                font-bold
                py-2
                px-4
                rounded
              "
              @click="createUser"
            >
              Update
            </button> -->
          </div>
        </div>
      </form>
    </div>
  </AppLayout>
</template>

<script>
import router from "@/routes";
import AppLayout from "@/layouts/AppLayout";
import API from "@/services/API";
import { sync, get } from "vuex-pathify";
import ImageLogo from "@/assets/images/respro-logo.svg";

export default {
  name: "Home",
  components: {
    AppLayout,
  },
  data() {
    return {
      defaultImage: ImageLogo,
      premisesSelecte: false,
      fullname: "",
      email: "",
      password: "",
      selected_templates: [],
      selected_premises: [],
      role: "",
      isActive: false,
    };
  },
  computed: {
    currentUserIndex: sync("users/currentUserIndex"),
    uuid: get("users/users[:currentUserIndex]@uuid"),
    users: sync("users/users"),
    token: sync("app/session"),
    premises: sync("premises/premises"),
    templates: sync("templates/templates"),
    roles: sync("roles/roles"),
    audits: sync("audit/audits"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
    selectedAuditUuid: sync("audit/selectedAuditUuid"),
    g_name: get("users/users[:currentUserIndex]@name"),
    g_email: get("users/users[:currentUserIndex]@email"),
    g_password: get("users/users[:currentUserIndex]@password"),
    g_active: get("users/users[:currentUserIndex]@active"),
  },
  methods: {
    createUser() {
      let json_data = {
        name: this.fullname,
        email: this.email,
        password: this.password,
        premises: this.selected_premises,
        templates: this.selected_templates,
        active: this.isActive,
        role: this.role,
      };

      API.create_user(this.token, json_data)
        .then((responses) => {
          console.log(responses);

          if (responses)
            this.$buefy.toast.open({
              message: "User has been created successfully",
              type: "is-success",
            });

          router.push({ name: "users" });
        })
        .catch((error) => {
          API.APILog(error);
        });
    },
    cancel() {
      router.push({ name: "users" });
    },
    onBack() {
      this.currentAuditIndex = -1;
      this.$router.push({ name: "home" });
      console.log("User voluntarily stopped location selection");
    },
    getPremisesName: function (premiseUuid) {
      console.log(premiseUuid);
      let val = this.premises.find((item) => item.uuid === premiseUuid);

      return val ? val["name"] : "";
    },
  },

  created() {

    const loadingComponent = this.$buefy.loading.open({ container: null });
    this.fullname = this.g_name;
    this.email = this.g_email;
    this.password = this.g_password;
    this.active = this.g_active;
    API.fetch_user_details(this.token, this.uuid).then((responses) => {
      
        let userDetails = responses.data

        console.log(userDetails)


      this.selected_premises = [...userDetails['userDetails']['premises']].map(i => i['uuid']);
      this.selected_templates = [...userDetails['userDetails']['templates']].map(i => i['uuid']);
      this.role = userDetails['userDetails']['role']['uuid'];

        loadingComponent.close();
      })
      .catch((error) => {
        API.APILog(error);
        loadingComponent.close();
        this.$buefy.dialog.alert("Error fetching account information.");
      });
    
  },
};
</script>
