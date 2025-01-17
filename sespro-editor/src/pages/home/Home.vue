<template>
  <AppLayout :userRole="activeUserRole" :image-logo="defaultImage" header-title="Submitted Audits">
    <div class="px-4 w-full flex flex-row justify-center gap-x-12 bg-white text-PrimaryText">
      <div class="w-full pt-6">
        <div class="premise-list rounded-md">
          <div class="text-onyx">
            <b-table :data="audits" :paginated="true" :sortable="true" :backend-pagination="true" :backend-sorting="true"
              :total="totalRows" :per-page="perPage" :pagination-simple="true" :pagination-rounded="true"
              aria-next-label="Next page" aria-previous-label="Previous page" aria-page-label="Page"
              aria-current-label="Current page" :current-page.sync="currentPage" :sort-by.sync="sortBy"
              :sort-desc.sync="sortDesc" :sort-direction.sync="sortDirection" @sort="onSortChanged"
              @page-change="onPageChanged" @per-page-change="onPerPageChanged">
              <template slot-scope="props">
                <b-table-column field="submit_time" label="Completed Date" width="20%" :sortable="true" centered>
                    {{
                      new Intl.DateTimeFormat("en-US", {
                        timeZone: 'America/Denver',
                        timeStyle: "medium",
                        dateStyle: "short"
                      }).format(
                        new Date( props.row.submit_time))
                    }}
                </b-table-column>
                <b-table-column field="premises.name" label="Premise" width="20%" :sortable="false">
                  {{ props.row.premises.name }}
                </b-table-column>
                <b-table-column field="template" label="Template Name" width="20%" :sortable="false">
                  {{ props.row.template }}
                </b-table-column>
                <b-table-column field="auditor" label="Auditor" width="20%" :sortable="false">
                  {{ props.row.auditor }}
                </b-table-column>
                <b-table-column label="Actions" >
                  <button class="button is-small is-orange" @click="select(props.row)">
                    <b-icon icon="edit"></b-icon>
                  </button>
                  <button class="button is-small is-orange" @click="generatePdf(props.index, props.row.uuid)">
                    <b-icon icon="file-pdf"></b-icon>
                  </button>
                  <button class="button is-small is-orange" @click="deleteParsedAudit(props.index, props.row.uuid)">
                    <b-icon icon="delete"></b-icon>Delete
                  </button>
                </b-table-column>
              </template>
            </b-table>

            <div class="flex items-center justify-end gap-4">
              <div>
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
      down: true,
      displayMode: 'compact',
      pageSizes: ['10', '15', '25', 'all'],
      showPageSizeSelector: true,
      showInfo: true,
      showNavButtons: true,
      totalRows: 0,
      perPage: 10,
      currentPage: 1,
      sortBy: 'submit_time',
      sortDesc: true,
      sortDirection: 'desc',
    };
  },
  filters: {
    formatDate(value) {
      if (!value) return "";
      return new Intl.DateTimeFormat("en-US", {
        timeZone: 'America/Denver',
        timeStyle: "medium",
        dateStyle: "short"
      }).format(new Date(value))
    }
  },
  computed: {
    premises: sync("app/premises"),
    activeUserRole: sync("app/activeUserRole"),
    token: sync("app/session"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    audits: sync("audit/audits"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
    selectedAuditUuid: sync("audit/selectedAuditUuid"),
  },
  methods: {
    loadAudits() {
      // Make an API request to get the audits with pagination parameters
      // page: this.currentPage, pageSize: this.perPage, sortBy: this.sortBy, sortDirection: this.sortDirection
      // Update the audits data with the response from the server
      // Update the totalRows with the total number of records returned by the server
      const loadingComponent = this.$buefy.loading.open({ container: null });

      API.getAudits(this.token, this.currentPage, this.perPage, "date_submitted", this.sortDirection)
        .then((responses) => {
          let data = responses.data;

          let audits = data.audits;
          // console.log('audits ==========> ', audits)
          this.totalRows = data.total_results

          let parsedAudits = [];

          audits.forEach((item, index) => {
            parsedAudits.push({
              ...item,
              auditIndex: index,
              selectedPremises: item["premises"],
              body: [],
            });
          });

          this.audits = parsedAudits;

          loadingComponent.close();
        })
        .catch((error) => {
          API.APILog(error);
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        });
    },
    onSortChanged(newSortBy, sortDirection) {
      this.sortBy = newSortBy;
      this.sortDirection = sortDirection;
      this.loadAudits();
    },
    onPageChanged(newPage) {
      this.currentPage = newPage;
      this.loadAudits();
    },
    onPerPageChanged(newPerPage) {
      this.perPage = newPerPage;
      this.loadAudits();
    },
    formatDateTime(datetime) {
      return new Intl.DateTimeFormat("en-US", {
        timeZone: "America/Denver",
        timeStyle: "medium",
        dateStyle: "short",
      }).format(new Date(datetime));
    },
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
    editRow(e) {
      this.currentAuditIndex = e.row.rowIndex;
      this.selectedAuditUuid = e.row.key;
      router.push({ name: "audit" });
    },
    deleteRow(e) {
      this.deleteParsedAudit(e.row.data.dataIndex, e.row.key)
    },
    generatePdf(index, uuid) {
      console.log(index)
      const loadingComponent = this.$buefy.loading.open({ container: null });
      API.generate_pdf_and_send(this.token, uuid)
        .then((responses) => {

          console.log(responses)

          this.$buefy.toast.open({
            message: "Pdf has been generated and sent successfully",
            type: "is-success",
          });

          loadingComponent.close();
        })
        .catch((error) => {
          API.APILog(error);
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        });
    },
    generatePdfDevextreme(e) {

      this.generatePdf(e.row.data.dataIndex, e.row.key)

    },
    deleteParsedAudit(index, parsedUuid) {
      if (parsedUuid) {

        this.$buefy.dialog.confirm({
          title: 'Deleting audit',
          message: 'Are you sure you want to <b>delete</b> an audit? This action cannot be undone.',
          confirmText: 'Delete',
          type: 'is-danger',
          hasIcon: true,
          onConfirm: () => {

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
          }
        })
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
    this.loadAudits()
  },
};
</script>
