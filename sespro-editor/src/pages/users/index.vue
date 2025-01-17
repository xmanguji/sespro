<template>
  <AppLayout :imageLogo="defaultImage" headerTitle="Users" :userRole="activeUserRole">
    <div class="px-4 w-full flex flex-row justify-center gap-x-12 bg-white text-PrimaryText">
      <div class="w-full pt-6 text-onyx">
        <b-table :data="users" :key-field="'uuid'" :paginated="true" :sortable="true" :backend-pagination="true"
          :backend-sorting="true" :total="totalRows" :per-page="perPage" :pagination-simple="true"
          :pagination-rounded="true" aria-next-label="Next page" aria-previous-label="Previous page"
          aria-page-label="Page" aria-current-label="Current page" :current-page.sync="currentPage" :sort-by.sync="sortBy"
          :sort-desc.sync="sortDesc" :sort-direction.sync="sortDirection" @sort="onSortChanged"
          @page-change="onPageChanged" @per-page-change="onPerPageChanged">
          <template #default="{ index, row }">
            <b-table-column field="password" :visible="false">{{ row.password }}</b-table-column>
            <b-table-column field="name" label="Name">{{ row.name }}</b-table-column>
            <b-table-column field="email" label="Email">{{ row.email }}</b-table-column>
            <b-table-column field="role" label="Role">{{ row.role }}</b-table-column>
            <b-table-column field="templates" label="Templates">
              <template>
                <div class="flex flex-wrap gap-x-2 gap-1">
                  <div v-for="template in row.templates" :key="template.uuid" class="bg-white rounded-lg shadow p-1">
                    {{ template.name }}
                  </div>
                </div>
              </template>
            </b-table-column>
            <b-table-column field="organizations" label="Organizations">
              <template>
                <div class="flex flex-wrap gap-x-2 gap-1">
                  <div v-for="organize in row.organizations" :key="organize.uuid" class="bg-white rounded-lg shadow p-1">
                    {{ organize.name }}
                  </div>
                </div>
              </template>
            </b-table-column>
            <b-table-column label="Actions">
              <template>
                <b-button class="mr-1" size="is-small is-orange" @click="showUserDetails(row)">Details</b-button>
                <b-button size="is-small" type="is-danger" @click="deleteUser(index, row.uuid)">Delete </b-button>
              </template>
            </b-table-column>
            
          </template>
        </b-table>
        
        <div class="flex items-center justify-end gap-4">
          <div class="flex flex-row justify-between gap-4">

            <div class="flex justify-center items-center">
              <b-button class="bg-PrimaryDark text-white hover:text-PrimaryDark hover:bg-primary" variant="is-primary" size="is-small" @click="addUser()">Add User</b-button>
            </div>
            <div class="place-items-end">
            <b-select v-model="perPage" @input="onPerPageChanged">
              <option value="5">5 per page</option>
              <option value="10">10 per page</option>
              <option value="15">15 per page</option>
              <option value="20">20 per page</option>
            </b-select>

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
  name: "Users",
  components: {
    AppLayout
  },
  data() {
    return {
      defaultImage: ImageLogo,
      premisesSelecte: false,
      pageSizes: ['10', '15', '25', 'all'],
      perPage: 15,
      totalRows: 0,
      gridRefName: 'grid',
      sortBy: 'name',
      sortDesc: true,
      sortDirection: 'desc',
    };
  },
  computed: {
    users: sync("users/users"),
    currentPage: sync("users/page"),
    activeUserRole: sync("app/activeUserRole"),
    activeOrganization: sync("app/activeOrganization"),
    organizations: sync("premises/organizations"),
    groups: sync("premises/groups"),
    allPremises: sync("premises/premises"),
    allTemplates: sync("templates/templates"),
    token: sync("app/session"),
    roles: sync("roles/roles"),
    currentUserIndex: sync("users/currentUserIndex"),
    audits: sync("audit/audits"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
    selectedAuditUuid: sync("audit/selectedAuditUuid")
  },
  methods: {

    onSortChanged(newSortBy, newSortDesc) {
      this.sortBy = newSortBy;
      this.sortDesc = newSortDesc;
      this.fetchUsers();
    },
    onPageChanged(newPage) {
      this.currentPage = newPage;
      this.fetchUsers();
    },
    onPerPageChanged(newPerPage) {
      this.perPage = newPerPage;
      this.fetchUsers();
    },

    showUserDetails(row) {
      console.log(row.uuid)
      this.$router.push({ name: 'user-details', params: { uuid: row.uuid } });
    },

    saveUser(e) {

      if (e.changes.length > 0) {
        let uuid = e.changes[0].key;
        let data = e.changes[0].data;

        API.update_user(uuid, this.token, data)
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
      }

    },
    addNewUser(e) {
      API.create_user(this.token, e.data)
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
    addRow() {
      this.grid.addRow();
      this.grid.deselectAll();
    },
    sort_user() {
      this.sort_key = this.sort_key == 'asc' ? 'desc' : 'asc'

      const loadingComponent = this.$buefy.loading.open({ container: null });
      API.fetch_users_sort(this.token, this.sort_key)
        .then((responses) => {
          this.users = responses.data["users"];
          loadingComponent.close();
        })
        .catch((error) => {
          API.APILog(error);
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        });
    },

    select(premise, index) {
      if (premise) {
        this.currentUserIndex = index;
        this.selectedAuditUuid = premise.uuid;
        router.push({ name: "update-user" });
      } else {
        this.$buefy.dialog.alert(
          "No users found. If you expect to see a new location, try logging out first."
        );
      }
    },

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
    addUser() {
      router.push({ name: "create-user" });
    },
    details() {
      router.push({ name: "update-user" });
    },
    deleteUser(index, uuid) {
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
                this.users.splice(index, 1);
                this.$buefy.toast.open({
                  message: "A user has been deleted successfully",
                  type: "is-success",
                });
              })
              .catch((error) => {
                API.APILog(error);
              });
          },
        });
      } else {
        this.$buefy.dialog.alert(
          "No audit found. If you expect to see a new audit, try logging out first."
        );
      }
    },
    onBack() {
      this.currentAuditIndex = -1;
      this.$router.push({ name: "home" });
      console.log("User voluntarily stopped location selection");
    },

    fetchUsers() {
      
      const loadingComponent = this.$buefy.loading.open({ container: null });
      const myOrganization = this.activeUserRole == 'ROLE_ROOT' ? null : this.activeOrganization.uuid;

      API.fetch_users_sort(this.token, myOrganization, this.currentPage, this.perPage, "name", this.sortDesc)
        .then((responses) => {
          // const myOrganization = this.activeOrganization.name;
          if(this.activeUserRole == 'ROLE_OWNER'){
            this.users = responses.data.users
            this.totalRows = responses.data.total_results
            // this.users = responses.data.users.filter(user => user.organizations.some(org => org.name == myOrganization));
            // this.totalRows = responses.data.users.filter(user => user.organizations.some(org => org.name == myOrganization)).length;
          }else{
            this.users = responses.data.users
            this.totalRows = responses.data.total_results
          }
          console.log(this.users)
          loadingComponent.close();
        })
        .catch((error) => {
          API.APILog(error);
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        });
    }
  },

  created() {
    this.fetchUsers()
  },
};
</script>
