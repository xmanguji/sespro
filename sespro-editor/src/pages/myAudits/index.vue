<template>
  <AppLayout :imageLogo="defaultImage" headerTitle="My Templates" :userRole="activeUserRole">
    <div class="px-4 w-full flex flex-row justify-center gap-x-12 bg-white text-PrimaryText">
      <div class="w-full pt-6 text-onyx">

        <div class="w-full flex flex-col">

          <div v-if="!indexCreateAuditAllowed && (activeUserRole !== 'ROLE_AUDITOR')" class="button is-small ml-1 w-48"
            @click="onAllowCreateAudit(1)">
            <b-icon icon="plus" class="text-xs"></b-icon>
            &nbsp;&nbsp;Create New Template
          </div>

          <!-- {{ auditOrg }} -->

          <textarea v-if="indexCreateAuditAllowed" id="question" v-model="auditText" type="text"
            placeholder="Enter Template Name" class="border rounded-xs text-gray-700 px-2 py-0 w-80" />

          <select v-if="indexCreateAuditAllowed && activeUserRole === 'ROLE_ROOT'" v-model="auditOrg"
            class="border rounded-md bg-white py-2 mb-4 pl-3 text-gray-700 w-80 mt-3">
            <option v-for="option in organizations" :key="option.uuid" :value="option">{{
              option.name }}</option>
          </select>

          <div class="flex flex-row mt-3">
            <div v-if="indexCreateAuditAllowed"
              class="w-24 btn-edit bg-spanishOrange cursor-pointer text-white mr-2 font-bold py-2 px-4 rounded"
              @click="onAllowCreateAudit(0)">
              Cancel
            </div>
            <div v-if="indexCreateAuditAllowed && auditText"
              class="w-24 btn-edit bg-PrimaryDark cursor-pointer text-white font-bold py-2 px-4 rounded"
              @click="createAudit">
              Create
            </div>
          </div>


        </div>

        <b-table :data="allTemplates" :key-field="'uuid'">
          <template #default="{ row }">

            <b-table-column field="name" label="Name">
              <div v-if="indexUpdateAuditAllowed != row.uuid">{{ row.name }}</div>
              <textarea v-if="indexUpdateAuditAllowed == row.uuid" id="question" v-model="auditText" type="text"
                placeholder="Enter Audit Text" class="border rounded-xs text-gray-700 px-2 py-0 w-3/6" />
            </b-table-column>

            <b-table-column field="creator" label="Creator">{{ row.creator.name || '-' }}</b-table-column>

            <b-table-column field="org" label="Organization">
              <span v-if="indexUpdateAuditAllowed != row.uuid">{{ row.organization.name || '-' }}</span>
              <select v-if="indexUpdateAuditAllowed == row.uuid" v-model="auditOrg"
                class="border rounded-md bg-white py-2 mb-4 pl-3 text-gray-700">
                <option v-for="option in organizations" :key="option.uuid" :value="option">{{
                  option.name }}</option>
              </select>
            </b-table-column>

            <b-table-column label="Actions">
              <template>
                <div class="button is-small ml-2" @click="select(row)">
                  <b-icon icon="eye" class="text-xs"></b-icon>
                </div>
                <div
                  v-if="indexUpdateAuditAllowed != row.uuid && (activeUserUUID === row.creator.uuid || activeUserRole === 'ROLE_ROOT' || activeUserRole === 'ROLE_OWNER')"
                  class="button is-small ml-2" @click="onAllowUpdateAudit(row.uuid, row.name, row.organization)">
                  <b-icon icon="edit" class="text-xs"></b-icon>
                </div>
                <div v-if="indexUpdateAuditAllowed == row.uuid" class="button is-small ml-2"
                  @click="updateAudit(row.uuid)">
                  <b-icon icon="check" class="text-xs"></b-icon>
                </div>
                <div class="button is-small ml-2"
                  v-if="activeUserUUID === row.creator.uuid || activeUserRole === 'ROLE_ROOT' || activeUserRole === 'ROLE_OWNER'"
                  @click="indexUpdateAuditAllowed == row.uuid ? onAllowUpdateAudit(-1, '', { uuid: '', name: '' }) : deleteAudit(row.uuid)">
                  <b-icon icon="times" class="text-xs"></b-icon>
                </div>
              </template>
            </b-table-column>
          </template>
        </b-table>

      </div>
    </div>
  </AppLayout>
</template>

<script>
import ImageLogo from "@/assets/images/respro-logo.svg";
import API from "@/services/API";
import router from "@/routes";
import AppLayout from "@/layouts/AppLayout";
import { sync } from "vuex-pathify";
export default {
  name: "my-audits",
  components: {
    AppLayout
  },
  data() {
    return {
      defaultImage: ImageLogo,
      indexCreateAuditAllowed: 0,
      indexUpdateAuditAllowed: -1,
      auditText: '',
      auditOrg: {
        uuid: '',
        name: '',
      },
    };
  },
  computed: {
    activeUserRole: sync("app/activeUserRole"),
    activeTemplates: sync("app/activeTemplates"),
    activeUserUUID: sync("app/activeUserUUID"),
    activeOrganization: sync("app/activeOrganization"),
    premises: sync("app/premises"),
    allTemplates: sync("templates/templates"),
    token: sync("app/session"),
    organizations: sync("premises/organizations"),
  },
  methods: {
    fetchPremises() {
      API.fetch_organizations_sort(this.token, 'asc')
        .then((response) => {
          this.organizations = response.data["organizations"].map(x => { return { name: x.name, uuid: x.uuid } });
        })
        .catch((error) => {
          API.APILog(error);
          this.$buefy.dialog.alert("Error fetching premises information.");
        });
    },
    fetchTemplates() {
      const loadingComponent = this.$buefy.loading.open({ container: null });
      API.fetch_templates(this.token)
        .then((responses) => {
          this.allTemplates = responses.data["templates"];
          loadingComponent.close();
        })
        .catch((error) => {
          API.APILog(error);
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        });
    },
    select(e) {
      if (e) {
        router.push({ name: 'myaudit-details', params: { uuid: e.id } });
      } else {
        this.$buefy.dialog.alert(
          "No locations found. If you expect to see a new location, try logging out first."
        );
      }
    },
    onAllowCreateAudit(d) {
      this.auditText = '';
      this.indexCreateAuditAllowed = d;
      this.indexUpdateAuditAllowed = false;
    },
    onAllowUpdateAudit(d, text, org) {
      this.indexCreateAuditAllowed = false;
      this.indexUpdateAuditAllowed = d;
      this.auditText = text;
      this.auditOrg = org
    },
    createAudit() {
      let json_data = {
        name: this.auditText,
        creator: this.activeUserUUID,
        enabled: true,
        organization: this.auditOrg.uuid || this.activeOrganization.uuid
      };

      const loadingComponent = this.$buefy.loading.open({ container: null });

      API.create_template(this.token, json_data)
        .then((responses) => {
          loadingComponent.close();
          if (responses)
            this.$buefy.toast.open({
              message: "Template has been created successfully!",
              type: "is-success",
            });
          this.auditText = '';
          this.auditOrg = {
            uuid: '',
            name: '',
          }
          this.indexCreateAuditAllowed = 0;
          this.updateUserTemplate(responses.data.data);
          setTimeout(() => {this.fetchTemplates()}, 2000)
        })
        .catch((error) => {
          loadingComponent.close();
          API.APILog(error);
          this.indexCreateAuditAllowed = 0;
        });
    },
    updateUserTemplate(x) {
      this.activeTemplates = [...this.activeTemplates, x];
      const templeUUIDs = this.activeTemplates.map(x => x.uuid)

      let userData = {}
      userData.templates = templeUUIDs

      const loadingComponent = this.$buefy.loading.open({ container: null });

      API.update_user(this.activeUserUUID, this.token, userData)
        .then((responses) => {
          console.log(responses);

          loadingComponent.close();

          if (responses)
            this.$buefy.toast.open({
              message: "User has been updated successfully",
              type: "is-success",
            });

        })
        .catch((error) => {
          loadingComponent.close();
          API.APILog(error);
        });
    },
    updateAudit(uuid) {

      const loadingComponent = this.$buefy.loading.open({ container: null });
      API.update_template(this.token, uuid, {
        name: this.auditText,
        // creator: this.auditOrg.uuid,
        organization: this.auditOrg.uuid,
      }).then((response) => {
        this.fetchTemplates()
        loadingComponent.close();
        if (response)
          this.$buefy.toast.open({
            message: "Template has been updated successfully",
            type: "is-success",
          });
        this.indexUpdateAuditAllowed = -1;
        this.auditText = '';
        this.auditOrg = {
          uuid: '', name: ''
        }
      }).catch((error) => {
        loadingComponent.close();
        API.APILog(error);
      });
    },
    deleteAudit(uuid) {
      this.$buefy.dialog.confirm({
        title: "Deleting a template",
        message:
          "Are you sure you want to <b>delete</b> a template? This action cannot be undone.",
        confirmText: "Delete",
        type: "is-danger",
        hasIcon: true,
        onConfirm: () => {

          const loadingComponent = this.$buefy.loading.open({ container: null });
          API.delete_template(this.token, uuid)
            .then(() => {

              this.fetchTemplates()

              loadingComponent.close();

              this.$buefy.toast.open({
                message: "A template has been deleted successfully",
                type: "is-success",
              });
            })
            .catch((error) => {
              loadingComponent.close();
              API.APILog(error);
              this.$buefy.toast.open({
                message: "This template can't delete",
                type: "is-danger",
              });
            });
        },
      });
    },
  },
  created() {
    this.fetchTemplates();
    this.fetchPremises();
  },
};
</script>
