<template>
  <NoHeaderLayout :userRole="activeUserRole" :imageLogo="defaultImage" headerTitle="Dashboard">
    <div class="
          px-4
          w-full
          flex flex-col
          justify-center
          gap-x-12
          bg-white
          text-PrimaryText
        ">
      <div class="flex flex-row w-full justify-end bg-white mt-2">
        <div class="flex flex-row items-center justify-evenly mx-3 my-4">
          <div class="flex flex-row items-center">
            <label for="template" class="text-gray-700 font-semibold mr-2">Template</label>
            <div class="dx-field-value">
              <DxSelectBox :data-source="templateFilterOptions" v-model:value="selectedTemplate" display-expr="name"
                class="dx-texteditor-input border-b-2 border-gray-400 pb-1 w-full" id="template" />
            </div>
          </div>
          <div class="flex flex-row ml-4 items-center">
            <label for="location" class="text-gray-700 font-semibold mr-2">Location</label>
            <div class="dx-field-value">
              <DxSelectBox :data-source="locationFilterOptions" v-model:value="selectedLocation" display-expr="name"
                class="dx-texteditor-input border-b border-gray-400 w-full" id="location" />
            </div>
          </div>
          <div class="flex flex-row ml-4 items-center">
            <label for="fromDate" class="text-gray-700 font-semibold mr-2">From</label>
            <div class="dx-field-value">
              <DxDateBox v-model:value="fromDate" picker-type="rollers"
                class="dx-texteditor-input border-b border-gray-400 w-full" id="fromDate" />
            </div>
          </div>
          <div class="flex flex-row ml-4 items-center">
            <label for="toDate" class="text-gray-700 font-semibold mr-2">To</label>
            <div class="dx-field-value">
              <DxDateBox v-model:value="toDate" picker-type="rollers"
                class="dx-texteditor-input border-b border-gray-400 w-full" id="toDate" />
            </div>
          </div>
          <div class="flex flex-row ml-4 items-center">
            <label class="invisible">Run</label>
            <div class="dx-field-value">
              <DxButton class="h-full" :width="120" text="Run" type="default" styling-mode="contained"
                @click="runReport" />
            </div>
          </div>
        </div>
      </div>
      <div class="flex-2 w-full mt-4">

        <DxDataGrid :allow-column-reordering="true" :data-source="dataSource" key-expr="parsed_question_uuid"
          :show-borders="true">

          <DxColumnChooser :enabled="true" />
          <DxColumnFixing :enabled="true" />
          <DxFilterRow :visible="true" />
          <DxGrouping :context-menu-enabled="true" expand-mode="rowClick" 
          :texts="{groupContinuedMessage: '' }" />
          <DxGroupPanel :visible="true" empty-panel-text="Use the context menu of header columns to group data" />
          <DxColumn :allow-grouping="true" data-field="template_name" caption="Template" />
          <DxColumn :visible="false" data-field="parsed_question_uuid" caption="Audit Id" />
          <DxColumn :allow-grouping="true" data-field="location_name" caption="Location" />
          <DxColumn :visible="false" data-field="location_uuid" />
          <DxColumn :allow-grouping="true" data-field="category_text" caption="Section" />
          <DxColumn :visible="false" data-field="category_uuid" />
          <DxColumn :allow-grouping="true" data-field="date_submitted" data-type="date" caption="Submitted Date" />
          <DxColumn :allow-grouping="true" data-field="question_text" caption="Question" />
          <DxColumn :visible="false" data-field="question_uuid" />
          <DxColumn data-field="final_comments" caption="Final comments" />
          <DxColumn data-field="worth" data-type="number" />
          <DxColumn :allow-filtering="true" data-field="is_passed" caption="Passed" />
          <DxColumn data-field="score" data-type="number" />
          <DxColumn data-field="score_percentage" data-type="number" format="percent" />
          <DxColumn data-field="answer_notes" />
          <DxPaging :page-size="18" />
          <DxSearchPanel :visible="true" />
          <DxExport :enabled="true" :allow-export-selected-data="true" />
          <DxSummary>
            <DxGroupItem :show-in-group-footer="false" :align-by-column="true" column="worth" summary-type="sum"
              display-format="{0}" />
            <DxGroupItem :show-in-group-footer="false" :align-by-column="true" column="score" summary-type="sum"
              display-format="{0}" />
          </DxSummary>
        </DxDataGrid>

      </div>
    </div>
  </NoHeaderLayout>
</template>
  
<script>

// import AppLayout from "@/layouts/AppLayout";
import API from "@/services/API";
import { sync } from "vuex-pathify";
import ImageLogo from "@/assets/images/respro-logo.svg";
import DxSelectBox from 'devextreme-vue/select-box';
import DxDateBox from 'devextreme-vue/date-box';
import DxButton from 'devextreme-vue/button';

import {
  DxDataGrid,
  DxColumn,
  DxGrouping,
  DxGroupPanel,
  DxPaging,
  DxSearchPanel,
  DxColumnChooser,
  DxExport,
  DxSummary,
  DxGroupItem,
  DxColumnFixing,
  DxFilterRow
} from 'devextreme-vue/data-grid';
import NoHeaderLayout from "../../layouts/NoHeaderLayout.vue";
import 'devextreme/data/odata/store';

// let collapsed = false;

export default {
  name: "Home",
  components: {
    DxDataGrid,
    DxExport,
    DxColumn,
    DxSummary,
    DxGroupItem,
    DxGrouping,
    DxGroupPanel,
    DxPaging,
    DxSearchPanel,
    DxDateBox,
    NoHeaderLayout,
    DxSelectBox,
    DxColumnChooser,
    DxColumnFixing,
    DxButton,
    DxFilterRow
  },
  data() {
    return {
      defaultImage: ImageLogo,
      premisesSelecte: false,
      down: true,
      dataSource: [],
      locationFilterOptions: [],
      templateFilterOptions: [],
      fromDate: new Date(),
      toDate: new Date(),
      selectedLocation: null,
      selectedTemplate: null,
    };
  },
  computed: {
    premises: sync("app/premises"),
    token: sync("app/session"),
    activeUserRole: sync("app/activeUserRole"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    audits: sync("audit/audits"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
    selectedAuditUuid: sync("audit/selectedAuditUuid"),
  },
  methods: {

    runReport() {


      const loadingComponent = this.$buefy.loading.open({ container: null });

      const fromDate = new Date(this.fromDate)
      const toDate = new Date(this.toDate)

      const fromDateString = `${fromDate.getFullYear()}-${fromDate.getMonth() + 1}-${fromDate.getDate()} 00:00:00.000-600`
      const toDateString = `${toDate.getFullYear()}-${toDate.getMonth() + 1}-${toDate.getDate()} 00:00:00.000-600`

      const locationUuid = this.selectedLocation == null ? '' : this.selectedLocation.uuid
      const templateUuid = this.selectedTemplate == null ? '' : this.selectedTemplate.uuid

      const params = `fromDate=${fromDateString}&toDate=${toDateString}&locationUuid=${locationUuid}&templateUuid=${templateUuid}`


      API.fetch_generic_report_data(this.token, params).then((responses) => {
        console.log("fetching reports data")

        const data = responses.data

        let dataSource = []

        data.forEach(item => {
          const [
            uuid,
            location_name,
            location_uuid,
            score,
            score_percentage,
            final_comments,
            parsed_question_uuid,
            question_text,
            question_uuid,
            category_text,
            category_uuid,
            worth,
            is_passed,
            answer_notes,
            template_uuid,
            template_name,
            date_submitted
          ] = [...item]

          dataSource.push({
            "uuid": uuid,
            "location_name": location_name,
            "location_uuid": location_uuid,
            "score": score,
            "score_percentage": score_percentage,
            "final_comments": final_comments,
            "parsed_question_uuid": parsed_question_uuid,
            "question_text": question_text,
            "question_uuid": question_uuid,
            "category_text": category_text,
            "category_uuid": category_uuid,
            "worth": worth,
            "is_passed": is_passed,
            "answer_notes": answer_notes,
            "template_uuid": template_uuid,
            "template_name": template_name,
            "date_submitted": date_submitted
          })

        })

        this.dataSource = dataSource


        loadingComponent.close();
      }).catch(error => {
        console.log(error)
        loadingComponent.close();
        this.$buefy.dialog.alert("Error fetching account information.");
      })
    },
    onBack() {
      this.currentAuditIndex = -1;
      this.$router.push({ name: "home" });
      console.log("User voluntarily stopped location selection");
    },
  },

  created() {
    const loadingComponent = this.$buefy.loading.open({ container: null });

    Promise.all([
      API.fetch_templates(this.token),
      this.activeUserRole == 'ROLE_ROOT' ? API.fetch_premises_sort(this.token, 'asc') : API.getPremises(this.token, 'asc')
    ]).then(responses => {

      const [templates, locations] = responses
      this.templateFilterOptions = templates.data.templates
      this.locationFilterOptions = locations.data.premises
      loadingComponent.close()
    }).catch(error => {
      console.log(error)
      loadingComponent.close();
      this.$buefy.dialog.alert("Error fetching account information.");
    })
  },
};
</script>
<style scoped>
.dx-texteditor-input {
  border-top: none;
  border-right: none;
  border-left: none;
  border-radius: 0;
  border-bottom: 1px solid gray;
  background-color: transparent;
}
</style>
  