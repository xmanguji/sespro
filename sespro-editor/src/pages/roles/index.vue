<template>
  <AppLayout :userRole="activeUserRole" :imageLogo="defaultImage" headerTitle="Users">
    <div
      class="
        px-4
        w-full
        flex flex-row
        justify-center
        gap-x-12
        bg-white
        text-PrimaryText
      "
    >
      <div class="w-full pt-6">
        <div class="premise-list rounded-md">
          <div class="text-onyx">
            <table
              class="table-auto min-w-max w-full px-6 bg-lightBg border-none"
            >
              <thead class="text-white bg-white border-b">
                <tr class="border-b-1">
                  <!-- <th
                    class="
                      px-4
                      pl-12
                      py-4
                      flex-1
                      text-xl
                      font-thin
                      text-indigoDark
                    "
                  >
                   Order
                  </th> -->
                  <th
                    class="px-4 py-4 flex-1 text-xl font-thin text-indigoDark"
                  >
                    ID
                  </th>
                  <th
                    class="px-4 py-4 flex-1 text-xl font-thin text-indigoDark"
                  >
                    Display name
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  class="
                    justify-evenly
                    bg-white
                    w-full
                    border-b
                    align-bottom
                    border-darkBg
                    hover:bg-indigoVeryLight hover:text-white
                  "
                  v-for="au in this.roles"
                  :key="au.uuid"
                  @click="details"
                >
                  <!-- <td class="px-4 pl-12 py-4 flex-1">
                    {{ au.order }}
                  </td> -->
                  <td class="px-4 py-4 flex-1">{{ au.name }}</td>
                  <td class="px-4 py-4 flex-1">{{ au.displayName }}</td>
                </tr>
              </tbody>
            </table>
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
  name: "Home",
  components: {
    AppLayout
  },
  data() {
    return {
      defaultImage: ImageLogo,
      premisesSelecte: false,
    };
  },
  computed: {
    roles: sync("roles/roles"),
    activeUserRole: sync("app/activeUserRole"),
    token: sync("app/session"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    audits: sync("audit/audits"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
    selectedAuditUuid: sync("audit/selectedAuditUuid"),
  },
  methods: {
    select(premise) {
      if (premise) {
        this.currentAuditIndex = premise.auditIndex;
        this.selectedAuditUuid = premise.uuid;
        router.push({ name: "audit" });
      } else {
        this.$buefy.dialog.alert(
          "No locations found. If you expect to see a new location, try logging out first."
        );
      }
    },
    addUser() {
      router.push({ name: "create-user" });
    },
    details() {
      this.$buefy.toast.open({
        message: "Show details page",
        type: "is-success",
      });
    },
    deleteParsedAudit(index, parsedUuid) {
      if (parsedUuid) {
        API.deleteParsedAudit(this.token, parsedUuid)
          .then((responses) => {
            if (responses.status == "202") {
              this.audits.splice(index, 1);
              this.$buefy.toast.open({
                message: "An audit has been deleted successfully",
                type: "is-success",
              });
            }
          })
          .catch((error) => {
            API.APILog(error);
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
    getPremisesName: function (premiseUuid) {
      console.log(premiseUuid);
      let val = this.premises.find((item) => item.uuid === premiseUuid);

      return val ? val["name"] : "";
    },
  },

  created() {
    const loadingComponent = this.$buefy.loading.open({ container: null });
    API.fetch_roles(this.token)
      .then((responses) => {
        this.roles = responses.data["roles"];

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
