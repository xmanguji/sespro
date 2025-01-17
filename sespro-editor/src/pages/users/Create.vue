<template>
  <AppLayout :back="true" :imageLogo="defaultImage" headerTitle="User Details" :userRole="activeUserRole">
    <div class="px-4 w-full bg-white text-PrimaryText ">
      <div>
        <!-- Edit Button -->
        <div class="text-right mt-6">
          <button class="btn-edit bg-spanishOrange hover:bg-PrimaryDark text-white mr-2 font-bold py-2 px-4 rounded"
            @click="cancelUser">
            Cancel
          </button>
          <button class="btn-edit bg-PrimaryDark hover:bg-PrimaryDark text-white font-bold py-2 px-4 rounded"
            @click="saveUser">
            Save
          </button>
        </div>
        <div class=" grid grid-cols-2 py-8 gap-x-3" style="grid-auto-rows: max-content;">

          <!-- Basic Info Row -->
          <div class="mb-4 card-wrapper row-span-1 col-span-1">
            <div class="card">
              <h3 class="text-2xl font-semibold mt-4 mb-4">Basic Information</h3>
              <div class="flex flex-row">
                <div class="w-1/2 pr-8 ml-2">
                  <div class="mb-4">
                    <label class="text-lg font-semibold">Name</label>
                    <b-input v-model="name" type="text" class="text-lg"></b-input>
                  </div>
                  <div class="mb-4">
                    <label class="text-lg font-semibold">Email</label>
                    <b-input v-model="email" type="email" class="text-lg"></b-input>
                  </div>
                </div>
                <div class="w-1/2 pl-8 mr-2">
                  <div class="mb-4">
                    <label class="text-lg font-semibold">Role</label>
                    <select v-model="role" class="border rounded-md bg-white py-2 pl-3 pr-8 w-full text-gray-700">
                      <option v-for="option in roles" :key="option.uuid" :value="option">{{
                        option.displayName }}</option>
                    </select>
                  </div>
                  <div class="mb-4">
                    <label class="text-lg font-semibold">Password</label>
                    <b-field :type="showPassword ? 'text' : 'password'" label-position="on-border">
                      <b-input v-model="password" class="text-lg"></b-input>
                      <b-icon icon="eye" pack="fas" v-if="!showPassword" @click="showPassword = true" slot="icon"
                        class="cursor-pointer"></b-icon>
                      <b-icon icon="eye-slash" pack="fas" v-else @click="showPassword = false" slot="icon"
                        class="cursor-pointer"></b-icon>
                    </b-field>
                  </div>
                  <!-- Add other basic user info as needed -->
                </div>
              </div>
            </div>
          </div>



          <!-- Templates Row -->
          <div class="mb-4 card-wrapper row-span-1 col-span-1"
            >
            <div class="card pt-4">
              <h3 class="text-2xl font-semibold mb-4">Templates</h3>
              <div class="grid grid-cols-2 gap-4  px-4">
                <template v-for="(template, index) in filteredTemplates">
                  <div :key="index" class="text-lg mb-2">
                    <label class="flex items-center">
                      <input type="checkbox" v-model="selectedTemplatesUuids" :value="template.uuid"
                        :checked="selectedTemplatesUuids.includes(template.uuid)"
                        class="form-checkbox mr-2 h-5 w-5 text-spanishOrange">
                      <span :class="{ 'font-semibold': selectedTemplatesUuids.includes(template.uuid) }">{{
                        template.name }}</span>
                    </label>
                  </div>
                </template>
              </div>
            </div>
          </div>



          <!-- Premises Row -->
          <div class="mb-4 col-span-2" >
            <div class="card pt-4">
              <h3 class="text-2xl font-semibold mb-4">Premises</h3>
              <div class="m-4 justify-center w-96 items-center">
                <label class="text-lg font-semibold">Search</label>
                <input type="text" v-model="premisesSearch" class="border border-gray-300 px-4 py-2 rounded w-full"
                  placeholder="Search premises">
              </div>

              <div class="grid grid-cols-5 gap-4  px-4">
                <template v-for="(premise, index) in filteringPremises">
                  <div :key="index" class="text-lg mb-2">
                    <label class="flex items-center">
                      <input type="checkbox" v-model="selectedPremisesUuids" :value="premise.uuid"
                        :checked="selectedPremisesUuids.includes(premise.uuid)"
                        class="form-checkbox bg-PrimaryDark mr-2 h-5 w-5">
                      <span :class="{ 'font-semibold': selectedPremisesUuids.includes(premise.uuid) }">
                        {{ premise.name }}
                      </span>
                    </label>
                  </div>
                </template>
              </div>
            </div>
          </div>


          <!-- Groups and Organizations Row -->
          <div class="mb-8 col-span-1" >
            <div class="card">
              <h3 class="text-2xl font-semibold pt-4 mt-4  mb-4">Groups</h3>
              <select v-model="userGroups" @change="handleGroupSelectChange"
                class="border rounded-md bg-white py-2 w-11/12 mb-4 pl-3 pr-8  text-gray-700">
                <option v-for="option in filteredGroups" :key="option.uuid" :value="option">{{
                  option.name }}</option>
              </select>
            </div>
          </div>


          <div class=" col-span-1" v-if="role.name != 'ROLE_ROOT'">
            <div class="card">
              <h3 class="text-2xl font-semibold pt-4 mt-4  mb-4">Organizations</h3>
              <select v-model="userOrganizations" @change="handleOrganizationSelectChange"
                class="border rounded-md bg-white py-2 w-11/12 mb-4 pl-3 pr-8  text-gray-700">
                <option v-for="option in organizations" :key="option.uuid" :value="option">{{
                  option.name }}</option>
              </select>
            </div>
          </div>

        </div>
      </div>
    </div>

  </AppLayout>
</template>

<script>

import router from "@/routes";
import AppLayout from "@/layouts/AppLayout";
import API from "@/services/API";
import { sync } from "vuex-pathify";
import ImageLogo from "@/assets/images/respro-logo.svg";
export default {
  name: "CreateUser",
  components: {
    AppLayout
  },
  data() {
    return {
      defaultImage: ImageLogo,
      user: {
        premises: []
      },
      premises: [],
      templates: [],
      userGroups: [],
      userOrganizations: [],
      name: "",
      email: "",
      role: {
        name: ''
      },
      editMode: false,
      password: "",
      showPassword: false,
      premisesSearch: "",
      filteredTemplates: [],
      filteredGroups: [],
      filteredPremises: [],
    };
  },
  computed: {
    users: sync("users/users"),
    activeUserRole: sync("app/activeUserRole"),
    organizations: sync("premises/organizations"),
    groups: sync("premises/groups"),
    allPremises: sync("premises/premises"),
    allTemplates: sync("templates/templates"),
    token: sync("app/session"),
    roles: sync("roles/roles"),
    currentUserIndex: sync("users/currentUserIndex"),
    filteringPremises() {
      if (!this.premisesSearch) {
        return this.filteredPremises;
      }

      const searchTerm = this.premisesSearch.toLowerCase();

      return this.filteredPremises.filter((premise) =>
        premise.name.toLowerCase().includes(searchTerm)
      );
    },
    selectedPremisesUuids: {
      get() { return this.user.premises.map(premise => premise.uuid) },
      set(value) {
        this.user.premises = this.filteredPremises.filter((premise) =>
          value.includes(premise.uuid)
        );
      }
    },
    selectedTemplatesUuids: {
      get() { return this.templates.map(temp => temp.uuid); },
      set(value) {
        this.templates = this.allTemplates.filter((premise) =>
          value.includes(premise.uuid)
        );
      }
    },
    selectedGroupUuids: {
      get() { return this.userGroups.map(group => group.uuid) },
      set(value) {
        this.userGroups = this.groups.filter((premise) =>
          value.includes(premise.uuid)
        );
      }
    },
  },
  methods: {
    handleOrganizationSelectChange() {
      const Cuuid = this.userOrganizations.uuid;
      this.filteredTemplates = this.allTemplates.filter(x => (x.organization.uuid === Cuuid))
      this.filteredGroups = this.groups.filter(x => x.organization.uuid === Cuuid)
      const groupUUIDs = this.filteredGroups.map(x => x.uuid)
      this.filteredPremises = this.allPremises.filter(x => groupUUIDs.includes(x.group.uuid))
    },
    handleGroupSelectChange() {
      this.filteredPremises = this.allPremises.filter(x => this.userGroups.uuid === x.group.uuid)
    },
    cancelUser() {
      router.push({ name: "users" });
    },

    buildUserUpdateObject() {

      let userData = {}

      if (this.password)
        userData.password = this.password

      if (this.templates)
        userData.templates = this.selectedTemplatesUuids

      if (this.premises)
        userData.premises = this.selectedPremisesUuids

      if (this.name)
        userData.name = this.name

      if (this.role)
        userData.role = this.role.uuid

      if (this.email)
        userData.email = this.email

      userData.premises_group = this.userGroups ? this.userGroups.uuid : ''

      if (this.userOrganizations)
        userData.premises_organization = this.userOrganizations.uuid

      return userData
    },

    saveUser() {

      let userData = this.buildUserUpdateObject()

      const loadingComponent = this.$buefy.loading.open({ container: null });

      API.create_user(this.token, userData)
        .then((responses) => {
          console.log(responses);

          loadingComponent.close();

          if (responses)
            this.$buefy.toast.open({
              message: "User has been created successfully",
              type: "is-success",
            });

          router.push({ name: "users" });

        })
        .catch((error) => {
          loadingComponent.close();
          API.APILog(error);
        });

    },


    deleteUser() {

      const uuid = this.user.uuid

      if (uuid) {
        this.$buefy.dialog.confirm({
          title: "Deleting a user",
          message:
            "Are you sure you want to <b>delete</b> this user? This action cannot be undone.",
          confirmText: "Delete",
          type: "is-danger",
          hasIcon: true,
          onConfirm: () => {
            API.delete_user(this.token, uuid)
              .then(() => {

                this.$buefy.toast.open({
                  message: "A user has been deleted successfully",
                  type: "is-success",
                });

                this.$router.push({ name: "users" });
              })
              .catch((error) => {
                API.APILog(error);
              });
          },
        });
      } else {
        this.$buefy.dialog.alert(
          "The User not found."
        );
      }
    },

    onBack() {
      this.currentAuditIndex = -1;
      this.$router.push({ name: "users" });
      console.log("User voluntarily stopped location selection");
    },

    fetUserDetails() {

      const loadingComponent = this.$buefy.loading.open({ container: null });

      const uuid = this.$route.params.uuid;

      API.fetch_user_details(this.token, uuid)
        .then((responses) => {


          this.user = responses.data

          loadingComponent.close();
        })
        .catch((error) => {
          API.APILog(error);
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        });
    },

    fetchRoles() {

      API.fetch_roles(this.token)
        .then((responses) => {
          this.roles = responses.data["roles"];

          console.log(this.roles)
        })
        .catch((error) => {
          API.APILog(error);
          this.$buefy.dialog.alert("Error fetching account information.");
        });
    }
  },

  created() {
    this.fetchRoles();
    this.filteredTemplates = this.allTemplates;
    this.filteredGroups = this.groups;
    this.filteredPremises = this.allPremises;
  },
};
</script>

<style scoped>
.card-wrapper {
  display: flex;
}

.card {
  flex: 1;
}
</style>
