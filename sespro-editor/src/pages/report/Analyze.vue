<template>
  <NoHeaderLayout :userRole="activeUserRole" :imageLogo="defaultImage" headerTitle="Analyze">

    <div class="p-3 w-full h-screen overflow-auto" style="background-color: #eef2f6;">
      <div>
        <div class="p-3 flex flex-row w-full justify-between items-center mt-2 card">
          <div class="text-xl font-semibold">
            Location Scores
          </div>
          <div class="flex flex-row items-center">
            <label for="audit" class="text-gray-700 mr-2">Audit</label>
            <div class="dx-field-value">
              <DxSelectBox :data-source="templateFilterOptions" v-model:value="selectedTemplate" display-expr="name"
                class="border-b border-gray-400" id="template" />
            </div>
          </div>
          <div class="flex flex-row items-center">
            <label for="fromDate" class="text-gray-700 mr-2">From</label>
            <div class="dx-field-value">
              <DxDateBox v-model:value="fromDateSection" picker-type="rollers" class="border-b border-gray-400"
                id="fromDateSection" />
            </div>
          </div>
          <div class="flex flex-row items-center">
            <label for="toDate" class="text-gray-700 mr-2">To</label>
            <div class="dx-field-value">
              <DxDateBox v-model:value="toDateSection" picker-type="rollers" class="border-b border-gray-400"
                id="toDateSection" />
            </div>
          </div>
          <div class="flex flex-row items-center">
            <label class="invisible">Run</label>
            <div class="dx-field-value">
              <DxButton class="h-full" :width="90" text="Run" type="default" styling-mode="contained"
                @click="onRunReportLocationScores" />
            </div>
          </div>
        </div>

        <div class="grid gap-3 mt-3 grid-cols-4">
          <div class="card p-3 col-span-3">
            <DxChart id="chart" :data-source="performanceLocationData" palette="Bright">
              <DxCommonSeriesSettings argument-field="month" />
              <DxCommonAxisSettings>
                <DxGrid :visible="true" />
              </DxCommonAxisSettings>
              <DxValueAxis>
                <DxTitle text="Average Location Score %" />
              </DxValueAxis>
              <DxSeries v-for="architecture in locationIndicatorSources" :key="architecture.value"
                :value-field="architecture.value" :name="architecture.name" />
              <DxMargin :bottom="20" />
              <DxArgumentAxis :allow-decimals="true" :axis-division-factor="60">
                <DxLabel>
                  <DxFormat type="decimal" />
                </DxLabel>
              </DxArgumentAxis>
              <DxLegend vertical-alignment="top" horizontal-alignment="right" />
              <DxExport :enabled="true" />
              <DxTooltip :enabled="true" />
            </DxChart>
          </div>

          <div class="grid grid-cols-2 gap-4 card p-3 col-span-1" style="max-height: 420px; overflow: auto">
            
            <div v-for="location in locationFilterOptions" :key="location.uuid">
              <label class="flex items-center">
                <input type="checkbox" v-model="selectedLocationUuids" :value="location.uuid"
                  :checked="selectedLocationUuids.includes(location.uuid)"
                  class="form-checkbox bg-PrimaryDark mr-2 h-5 w-5">
                <span style="font-size: 15px;" class="text-left">
                  {{ location.name }}
                </span>
              </label>
            </div>
          </div>
        </div>

      </div>

      <div class="flex flex-row w-full mt-3 card">
        <div class="flex mx-3 my-3 justify-between items-center w-full">

          <div class="text-xl font-semibold">
            Audit Scores
          </div>

          <div class="flex flex-row items-center">
            <label for="audit" class="text-gray-700 mr-2">Audit</label>
            <div class="dx-field-value">
              <DxSelectBox :data-source="templateFilterOptions" v-model:value="selectedTemplate" display-expr="name"
                class="border-b border-gray-400" id="template" />
            </div>
          </div>

          <div class="flex flex-row items-center">
            <div class="flex flex-row ml-4 items-center">
              <label for="location" class="text-gray-700 mr-2">Brand</label>
              <div class="dx-field-value">
                <DxSelectBox :data-source="groups" v-model:value="selectedGroup" display-expr="name"
                  class="border-b border-gray-400" id="location" />
              </div>
            </div>
            <div class="flex flex-row items-center">
              <label for="fromDate" class="text-gray-700 mr-2">From</label>
              <div class="dx-field-value">
                <DxDateBox v-model:value="fromDateSection" picker-type="rollers" class="border-b border-gray-400"
                  id="fromDateSection" />
              </div>
            </div>
            <div class="flex flex-row items-center">
              <label for="toDate" class="text-gray-700 mr-2">To</label>
              <div class="dx-field-value">
                <DxDateBox v-model:value="toDateSection" picker-type="rollers" class="border-b border-gray-400"
                  id="toDateSection" />
              </div>
            </div>
            <div class="flex flex-row items-center">
              <label class="invisible">Run</label>
              <div class="dx-field-value">
                <DxButton class="h-full" :width="90" text="Run" type="default" styling-mode="contained"
                  @click="onRunReportComplianceByLocation" />
              </div>
            </div>
          </div>

        </div>
      </div>

      <div class="w-full grid gap-2 grid-cols-4 pt-3">
        <div class="w-full col-span-4 grid grid-cols-5 flex-row justify-between">

          <div
            class="card justify-evenly col-span-1 flex-2 flex mr-2 h-100 gap-x-2 items-center flex-col border border-PrimaryText rounded">
            <div class="text-6xl text-PrimaryDark">{{ totalNumberOfAuditsSubmitted }}</div>
            <div class="text-2xl text-primary">Audits Submitted</div>
          </div>

          <div
            class="card justify-evenly col-span-1 flex-2 flex mr-2 h-100 gap-x-2 items-center flex-col border-2">
            <div class="text-6xl text-PrimaryDark">{{
              new Intl.NumberFormat('en-IN', {
                maximumSignificantDigits: 1
              }).format(averageScore) * 100
            }}</div>
            <div class="text-2xl text-primary">Average score</div>
          </div>

          <div class="col-span-3 card">
            <div class="border flex flex-row justify-between items-center">
              <div>Location Performance</div>
              <download-excel :data="complianceByLocationDataBest" :export-fields="{
                'Name': 'location_name',
                'Total': 'val',
                'Pass': 'score',
                'Fail': 'failed',
              }" :name="getDateExportName(fromDateSection, toDateSection, 'location_performance')">
                <button class="px-3 py-1 text-sm bg-yellow-600 text-white rounded-md">Download</button>
              </download-excel>
            </div>
            <div class="px-4 mt-4" v-for="(location, index) in complianceByLocationDataBest.slice(0, 10)" :key="index">
              <div class="justify-between w-full flex-row flex my-2"> 
                <div style="font-size: 13px;">{{ location.location_name }}</div>
                <div style="font-size: 13px;">{{ location.score }}/{{ location.val }}</div>
              </div>
              <div :class="`h-1 w-full -mt-2 mb-2`" :style="{ background: getGraphColor(index)[1] }">
                <div :class="`h-1`" :style="{ width: location.score / location.val * 100 + '%', background: getGraphColor(index)[0] }" />
              </div>
              <!-- <div class="flex-row flex justify-around pt-2">
                <div class="text-xs pt-2">Total <br/>{{ location.val }}</div>
                <div class="text-xs pt-2">Pass <br/>{{ location.score }}</div>
                <div class="text-xs pt-2">Failed <br/>{{location.failed}} </div>
              </div> -->
            </div>
          </div>

        </div>
      </div>

      <div class="flex flex-row w-full mt-3 bg-card">
        <div class="flex mx-3 my-3 items-center justify-between w-full">
          <div class="text-xl font-semibold">
            Compliance Detail
          </div>
            <div class="flex flex-row items-center">
              <label for="audit" class="text-gray-700 mr-2">Audit</label>
              <div class="dx-field-value">
                <DxSelectBox :data-source="templateFilterOptions" v-model:value="selectedTemplate" display-expr="name"
                  class="border-b border-gray-400" id="template" />
              </div>
            </div>
            <div class="flex flex-row items-center" style="position: relative;">
              <label for="audit" class="text-gray-700 mr-2">Location</label>
              <div class="dx-field-value">
                <div @click="toggleButtonClick">
                  <DxSelectBox 
                  style="opacity: 1;"
                  :disabled="true" 
                  v-model:value="selectedLocation" />
                </div>
                <div class="location-box" v-if="isAvailableLocationModal">
                  <div v-for="location in locationFilterOptions" :key="location.uuid">
                    <label class="flex items-center">
                      <input type="checkbox" v-model="selectedLocationUuids" :value="location.uuid"
                        :checked="selectedLocationUuids.includes(location.uuid)"
                        class="form-checkbox bg-PrimaryDark mr-2 h-5 w-5">
                      <span style="font-size: 15px;" class="text-left">
                        {{ location.name }}
                      </span>
                    </label>
                  </div>
                  <div @click="isAvailableLocationModal = false" class="cursor-pointer text-xs">close</div>
                </div>
              </div>
            </div>
            <div class="flex flex-row items-center">
              <label for="fromDate" class="text-gray-700 mr-2">From</label>
              <div class="dx-field-value">
                <DxDateBox v-model:value="fromDateQuestion" picker-type="rollers" class="border-b border-gray-400"
                  id="fromDateQuestion" />
              </div>
            </div>
            <div class="flex flex-row items-center">
              <label for="toDate" class="text-gray-700 mr-2">To</label>
              <div class="dx-field-value">
                <DxDateBox v-model:value="toDateQuestion" picker-type="rollers" class="border-b border-gray-400"
                  id="toDateQuestion" />
              </div>
            </div>
            <div class="flex flex-row items-center">
              <label class="invisible">Run</label>
              <div class="dx-field-value">
                <DxButton class="h-full" :width="90" text="Run" type="default" styling-mode="contained"
                  @click="onRunReportCompliance" />
              </div>
            </div>

        </div>
      </div>
      <div class="w-full pt-3">

        <div class="grid gap-3 grid-cols-2">
          <div class="pb-2 card">
            <div class="border flex flex-row justify-between items-center">
              <div>Section Performance</div>
              <download-excel :data="complianceSectionPerformace" :export-fields="{
                'Name': 'category_text',
                'Total': 'val',
                'Pass': 'score',
                'Fail': 'failed',
              }" :name="getDateExportName(fromDateQuestion, toDateQuestion, 'section_performance')">
                <button class="px-3 py-1 text-sm bg-yellow-600 text-white rounded-md">Download</button>
              </download-excel>
            </div>
            <div class="px-4 mt-4" v-for="(section, index) in complianceSectionPerformace.slice(0, 10)" :key="index">
              <div class="justify-between w-full flex-row flex my-2">
                <div style="font-size: 14px;">{{ section.category_text }} ({{parseInt(section.score / section.val * 100)}}%) </div>
                <div style="font-size: 13px;">{{ section.score }}/{{ section.val }}</div>
              </div>
              <div :class="`h-1 w-full -mt-1`" :style="{ background: getGraphColor(index)[1] }">
                <div :class="`h-1`"
                  :style="{ width: (section.score / section.val * 100) + '%', background: getGraphColor(index)[0] }" />
              </div>
              <div class="flex-row flex justify-around pt-2">
                <div class="text-xs pt-2">Total <br/>{{ section.val }}</div>
                <div class="text-xs pt-2">Pass <br/>{{ section.score }}</div>
                <div class="text-xs pt-2">Fail <br/>{{section.failed}} </div>
              </div>
            </div>
          </div>

          <div class="pb-2 card">
            <div class="border flex flex-row justify-between items-center">
              <div>Question Performance</div>
              <download-excel :data="complianceByQuestionDataWorst" :export-fields="{
                'Name': 'question_text',
                'Total': 'val',
                'Pass': 'score',
                'Fail': 'failed',
              }" :name="getDateExportName(fromDateQuestion, toDateQuestion, 'question_performance')">
                <button class="px-3 py-1 text-sm bg-yellow-600 text-white rounded-md">Download</button>
              </download-excel>
            </div>
            <div class="px-4 mt-4" v-for="(question, index) in complianceByQuestionDataWorst.slice(0, 10)" :key="index">
              <div class="justify-between w-full flex-row flex my-2">
                <div style="font-size: 14px;" class="text-left">{{ question.question_text }} ({{parseInt(question.score / question.val * 100)}}%)</div>
                <div style="font-size: 13px;">{{ question.score }}/{{ question.val }}</div>
              </div>
              <div :class="`h-1 w-full -mt-1`" :style="{ background: getGraphColor(index)[1] }">
                <div :class="`h-1`"
                  :style="{ width: (question.score / question.val * 100) + '%', background: getGraphColor(index)[0] }" />
              </div>
              <div class="flex-row flex justify-around pt-2">
                <div class="text-xs pt-2">Total <br/>{{ question.val }}</div>
                <div class="text-xs pt-2">Pass <br/>{{ question.score }}</div>
                <div class="text-xs pt-2">Fail <br/>{{question.failed}} </div>
              </div>
            </div>

          </div>

        </div>
      </div>
    </div>
  </NoHeaderLayout>
</template>
  
<script>

import { chain } from 'lodash';
import API from "@/services/API";
import DxSelectBox from 'devextreme-vue/select-box';
import { sync } from "vuex-pathify";
import ImageLogo from "@/assets/images/respro-logo.svg";
import DxButton from 'devextreme-vue/button';
import {
  DxArgumentAxis,
  DxChart, DxSeries, DxCommonAxisSettings, DxMargin,
  DxCommonSeriesSettings, DxGrid, DxValueAxis
} from 'devextreme-vue/chart';
import DxDateBox from 'devextreme-vue/date-box';
import {
  DxLegend,
  DxTitle,
  DxTooltip,
  DxFormat,
  DxLabel,
  DxExport,
} from 'devextreme-vue/pie-chart';
import NoHeaderLayout from "../../layouts/NoHeaderLayout.vue";
import UtilService from "../../services/utilservice";

const chartIndicatorSources = [
  { value: 'score', name: 'Score' },
  { value: 'score_percentage', name: 'Score Percentage' },
];

let date = new Date()

date = date.setMonth(date.getMonth() - 1)

export default {
  name: "Home",
  components: {
    DxGrid,
    DxMargin,
    DxCommonAxisSettings,
    DxArgumentAxis,
    DxTitle,
    DxButton,
    DxChart,
    DxDateBox,
    DxLegend,
    DxSeries,
    DxTooltip,
    DxFormat,
    DxLabel,
    DxSelectBox,
    DxExport,
    DxCommonSeriesSettings,
    NoHeaderLayout,
    DxValueAxis
  },
  data() {
    return {
      defaultImage: ImageLogo,
      totalNumberOfAuditsSubmitted: 0,
      averageScore: 0,
      performanceOverTimeData: [],
      performanceLocationData: [],

      complianceSectionPerformace: [],
      complianceByQuestionDataWorst: [],
      complianceByLocationDataBest: [],
      locationFilterOptions: [],
      locationIndicatorSources: [
        // { value: '2176a280-4732-4f89-8790-fb3607be95b1', name: 'Adane' },
        // { value: 'ca939a63-10c9-4398-9bf5-313df4cf60d6', name: 'Brevard' },
        // { value: 'b6f96306-434c-4ec9-8a4d-47e774fd74b1', name: 'Brevard' },
        // { value: '68271baa-580b-4525-a773-5b05a0874008', name: 'emc245' },
        // { value: '3ec8c263-80b9-4742-be36-e08e3d353e08', name: 'Postsdam Restaurant' },
        // { value: '422ca54d-8baa-42be-8149-ea51d5ce38b1', name: 'Roadhouse' },
      ],

      selectedLoactions: [
        // { uuid: '2176a280-4732-4f89-8790-fb3607be95b1', name: 'Adane' },
        // { uuid: 'ca939a63-10c9-4398-9bf5-313df4cf60d6', name: 'Brevard' },
        // { uuid: 'b6f96306-434c-4ec9-8a4d-47e774fd74b1', name: 'Brevard' },
        // { uuid: '68271baa-580b-4525-a773-5b05a0874008', name: 'emc245' },
        // { uuid: '3ec8c263-80b9-4742-be36-e08e3d353e08', name: 'Postsdam Restaurant' },
        // { uuid: '422ca54d-8baa-42be-8149-ea51d5ce38b1', name: 'Roadhouse' },
      ],

      templateFilterOptions: [],
      brandFilterOptions: [],
      fromDateSection: date,
      toDateSection: new Date(),
      fromDateQuestion: date,
      toDateQuestion: new Date(),
      selectedLocation: null,
      selectedTemplate: null,
      selectedGroup: null,
      chartIndicatorSources,
      formattedDate: '',
      isAvailableLocationModal: false
    };
  },
  computed: {
    premises: sync("app/premises"),
    activeUserRole: sync("app/activeUserRole"),
    token: sync("app/session"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    audits: sync("audit/audits"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
    selectedAuditUuid: sync("audit/selectedAuditUuid"),
    allPremises: sync("premises/premises"),
    groups: sync("premises/groups"),
    selectedLocationUuids: {
      get() { return this.selectedLoactions.map(i => i.uuid) },
      set(value) {
        this.selectedLoactions = this.locationFilterOptions.filter((i) =>
          value.includes(i.uuid)
        );
        this.locationIndicatorSources = this.locationFilterOptions.filter((i) =>
          value.includes(i.uuid)
        ).map(x => {
          return {
            name: x.name,
            value: x.uuid
          }
        })
      }
    },
    getGraphColor() {
      return (value) => {
        switch (value) {
          case 0:
            return ['#2196f3', '#aad7fa'];
          case 1:
            return ['#673ab7', '#c5b4e3'];
          case 2:
            return ['#c6282e', '#f9d9d9'];
          case 3:
            return ['#ffc14d', '#fff8e1'];
          case 4:
            return ['#00e676', '#e5fceb'];
          case 5:
            return ['#bbff00', '#f0fad4'];
          case 6:
            return ['#5d0ceb', '#d3c2f0'];
          case 7:
            return ['#f2029a', '#ebb5d7'];
          case 8:
            return ['#05b1e6', '#d1e8f0'];
          case 9:
            return ['#1a8215', '#9db59c'];
          default:
            return ['#00e676', '#e5fceb'];
        }
      }
    },
    getDateExportName() {
      return (date1, date2, extraString) => {
        const fromDate = new Date(date1);
        const yearFrom = fromDate.getFullYear();
        const monthFrom = fromDate.getMonth() + 1;
        const dayFrom = fromDate.getDate();
        const formattedFromDate = `${yearFrom}_${monthFrom.toString().padStart(2, '0')}_${dayFrom.toString().padStart(2, '0')}`;

        const toDate = new Date(date2);
        const yearTo = toDate.getFullYear();
        const monthTo = toDate.getMonth() + 1;
        const dayTo = toDate.getDate();
        const formattedToDate = `${yearTo}_${monthTo.toString().padStart(2, '0')}_${dayTo.toString().padStart(2, '0')}`;

        return formattedFromDate + '-' + formattedToDate + '_' + extraString;
      }
    }
  },
  methods: {
    onBack() {
      this.currentAuditIndex = -1;
      this.$router.push({ name: "home" });
      console.log("User voluntarily stopped location selection");
    },
    toggleButtonClick() {
      console.log('===== I am clicking !!!=====')
      this.isAvailableLocationModal = !this.isAvailableLocationModal;
    },
    onInitial() {
      const loadingComponent = this.$buefy.loading.open({ container: null });

      Promise.all([
        API.fetch_templates(this.token),
        this.activeUserRole == 'ROLE_ROOT' ? API.fetch_premises_sort(this.token, 'asc') : API.getPremises(this.token, 'asc'),
      ])
        .then((responses) => {
          const [templates, locations] = responses;
          this.templateFilterOptions = templates.data.templates
          this.locationFilterOptions = locations.data.premises
          this.brandFilterOptions = [];
          loadingComponent.close();
        }).catch(error => {
          console.log(error)
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        })
    },
    onGetComplianceBySection(dataSource) {

      const filteringData = this.selectedTemplate
        ? dataSource.filter(x => x.template_name === this.selectedTemplate.name)
        : dataSource;

      const groupByCategory = chain(filteringData)
        .groupBy('category_text')
        .map((val, category_text) => ({ val, category_text }))
        .value();

      const formattedGrouping = groupByCategory.map(i => {
        const item = i["val"]
        const cat = i["category_text"]
        const score = item.reduce((p, n) => {
          return p + Number(n.is_passed ? 1 : 0)
        }, 0)
        i['score'] = parseInt(score);
        i["category_text"] = cat;
        i['failed'] = item.length - i['score'];
        return i
      })

      this.complianceSectionPerformace =
        formattedGrouping
          .slice()
          .sort((a, b) => b.failed - a.failed)
          // .slice(0, 10);

      this.complianceSectionPerformace.forEach(x => {
        x.val = x.val.length;
      });

    },
    onGetComplianceByQuestion(dataSource) {

      const filteringData = this.selectedTemplate
        ? dataSource.filter(x => x.template_name === this.selectedTemplate.name)
        : dataSource;

      const groupByCategory = chain(filteringData)
        .groupBy('question_text')
        .map((val, question_text) => ({ val, question_text }))
        .value();

      const formattedGrouping = groupByCategory.map(i => {
        const item = i["val"]
        const cat = i["question_text"]
        const score = item.reduce((p, n) => {
          return p + (n.is_passed === true ? 1 : 0)
        }, 0)
        i['score'] = parseInt(score);
        i["question_text"] = cat;
        i['failed'] = item.length - i['score'];
        return i
      })

      this.complianceByQuestionDataWorst =
        formattedGrouping
          .slice()
          .sort((a, b) => b.failed - a.failed)
          // .slice(0, 10);

      this.complianceByQuestionDataWorst.forEach(x => {
        x.val = x.val.length;
      });
    },
    onGetComplianceByLocation(dataSource) {
      const filteringData = this.selectedTemplate
        ? dataSource.filter(x => x.template_name === this.selectedTemplate.name)
        : dataSource;

      const groupByCategory = chain(filteringData)
        .groupBy('location_uuid')
        .map((val, location_uuid) => ({ val, location_uuid }))
        .value();

      const formattedGrouping = groupByCategory.map(i => {
        const item = i["val"]
        const cat = i["location_uuid"]
        const score = item.reduce((p, n) => {
          return p + (n.is_passed ? 1 : 0)
        }, 0)
        i['score'] = parseInt(score);
        i["location_uuid"] = cat;
        const locationObject = this.locationFilterOptions.find(x => x.uuid === i["location_uuid"]);
        i["location_name"] = locationObject ? locationObject.name : '-';
        i['failed'] = item.length - i['score'];
        return i
      })
      
      this.complianceByLocationDataBest = formattedGrouping
        .slice()
        .sort((a, b) => b.failed - a.failed)
        .filter(x => x.location_name !== '-')
        // .slice(0, 5)

      this.complianceByLocationDataBest.forEach(x => {
        x.val = x.val.length;
      });

    },
    onGetAuditSubmitted(dataSource) {

      const groupByDateSubmitted = chain(dataSource)
        .groupBy('date_submitted')
        .map((val, date_submitted) => ({ val, date_submitted }))
        .value();

      const formattedDateGrouping = groupByDateSubmitted.map(i => {

        const item = i["val"]
        const score = item.reduce((p, n) => {
          return p + Number(n.score)
        }, 0)
        const score_percentage = item.reduce((p, n) => {
          return p + Number(n.score_percentage)
        }, 0)

        i['score'] = score;
        i['score_percentage'] = parseInt(score_percentage);
        return i
      })
      this.performanceOverTimeData = formattedDateGrouping;
    },
    onGetLocationScores(dataSource) {
      const filteringData = this.selectedTemplate
        ? dataSource.filter(x => x.template_name === this.selectedTemplate.name)
        : dataSource;

      const groupByDateLocation = chain(filteringData)
        .groupBy(data => new Date(data.date_submitted).getMonth() + 1)
        .map((val, month) => ({ val, month: UtilService.getMonthName(month) }))
        .value();

      const performanceLocationData = groupByDateLocation.map(i => {

        const item = i["val"]
        const groupByDateLocation = chain(item)
          .groupBy('location_uuid')
          .map((val, location_uuid) => ({ val, location_uuid }))
          .value();
        groupByDateLocation.forEach(data => {
          i[data.location_uuid] = parseInt(data.val.reduce((p, n) => {
            return p + Number(n.score_percentage)
          }, 0))
        })

        return i
      })
      this.performanceLocationData = performanceLocationData;
    },
    onRunReportCompliance() {
      this.onRunReportComplianceByQuestion();
      this.onRunReportComplianceBySection();
    },
    onRunReportComplianceBySection() {

      const loadingComponent = this.$buefy.loading.open({ container: null });
      const fromDate = new Date(this.fromDateQuestion)
      const toDate = new Date(this.toDateQuestion)
      const fromDateString = `${fromDate.getFullYear()}-${fromDate.getMonth() + 1}-${fromDate.getDate()} 00:00:00.000-600`
      const toDateString = `${toDate.getFullYear()}-${toDate.getMonth() + 1}-${toDate.getDate()} 00:00:00.000-600`
      const locationUuid = this.selectedLocation == null ? '' : this.selectedLocation.uuid
      const templateUuid = this.selectedTemplate == null ? '' : this.selectedTemplate.uuid
      const params = `fromDate=${fromDateString}&toDate=${toDateString}&locationUuid=${locationUuid}&templateUuid=${templateUuid}`

      Promise.all([
        API.fetch_generic_report_data(this.token, params),
        API.fetch_dashboard_number_of_audits_submitted(this.token, params),
        API.fetch_dashboard_average_score(this.token, params)
      ])
        .then((responses) => {
          const [genericData] = responses
          this.dataSource = genericData.data
          this.onGetComplianceBySection(genericData.data);
          loadingComponent.close();
        }).catch(error => {
          console.log(error)
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        })
    },
    onRunReportComplianceByLocation() {
      const loadingComponent = this.$buefy.loading.open({ container: null });
      const fromDate = new Date(this.fromDateSection)
      const toDate = new Date(this.toDateSection)
      const fromDateString = `${fromDate.getFullYear()}-${fromDate.getMonth() + 1}-${fromDate.getDate()} 00:00:00.000-600`
      const toDateString = `${toDate.getFullYear()}-${toDate.getMonth() + 1}-${toDate.getDate()} 00:00:00.000-600`
      const locationUuid = this.selectedLocation == null ? '' : this.selectedLocation.uuid
      const templateUuid = this.selectedTemplate == null ? '' : this.selectedTemplate.uuid
      const params = `fromDate=${fromDateString}&toDate=${toDateString}&locationUuid=${locationUuid}&templateUuid=${templateUuid}`
      // console.log('xxx --- selectedLoactions: ', this.selectedLoactions.map(x => x.uuid))

      Promise.all([
        API.fetch_generic_report_data(this.token, params),
        API.fetch_dashboard_number_of_audits_submitted(this.token, params),
        API.fetch_dashboard_average_score(this.token, params)
      ])
        .then((responses) => {
          console.log("fetching reports data")
          const [genericData, numberOfAudits, averageScore] = responses
          this.totalNumberOfAuditsSubmitted = numberOfAudits.data[0]
          this.averageScore = averageScore.data[0]
          let dataSource = genericData.data
          this.dataSource = genericData.data
          this.onGetComplianceByLocation(dataSource); // audit scores
          loadingComponent.close();
        }).catch(error => {
          console.log(error)
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        })
    },
    onRunReportComplianceByQuestion() {

      const loadingComponent = this.$buefy.loading.open({ container: null });
      const fromDate = new Date(this.fromDateQuestion)
      const toDate = new Date(this.toDateQuestion)
      const fromDateString = `${fromDate.getFullYear()}-${fromDate.getMonth() + 1}-${fromDate.getDate()} 00:00:00.000-600`
      const toDateString = `${toDate.getFullYear()}-${toDate.getMonth() + 1}-${toDate.getDate()} 00:00:00.000-600`
      const locationUuid = this.selectedLocation == null ? '' : this.selectedLocation.uuid
      const templateUuid = this.selectedTemplate == null ? '' : this.selectedTemplate.uuid
      const params = `fromDate=${fromDateString}&toDate=${toDateString}&locationUuid=${locationUuid}&templateUuid=${templateUuid}`

      Promise.all([
        API.fetch_generic_report_data(this.token, params),
      ])
        .then((responses) => {
          const [genericData] = responses
          this.onGetComplianceByQuestion(genericData.data);
          loadingComponent.close();
        }).catch(error => {
          console.log(error)
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        })
    },
    onRunReportLocationScores() {

      const loadingComponent = this.$buefy.loading.open({ container: null });
      const fromDate = new Date(this.fromDateSection)
      const toDate = new Date(this.toDateSection)
      const fromDateString = `${fromDate.getFullYear()}-${fromDate.getMonth() + 1}-${fromDate.getDate()} 00:00:00.000-600`
      const toDateString = `${toDate.getFullYear()}-${toDate.getMonth() + 1}-${toDate.getDate()} 00:00:00.000-600`
      const params = `fromDate=${fromDateString}&toDate=${toDateString}&locationUuid=${''}&templateUuid=${''}`

      Promise.all([
        API.fetch_generic_report_data(this.token, params),
      ])
        .then((responses) => {
          const [genericData] = responses
          let dataSource = genericData.data
          this.onGetLocationScores(dataSource);
          loadingComponent.close();
        }).catch(error => {
          console.log(error)
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        })
    },
    formatLabel(arg) {
      return `<span class="label">${arg.item.argument} </span>`;
    },
  },

  created() {
    this.onInitial();
    this.onRunReportLocationScores(); // LocationScores
    this.onRunReportComplianceByLocation(); // Audit Scores - Location Performance
    this.onRunReportComplianceBySection(); // Section Performance
    this.onRunReportComplianceByQuestion(); // Question Performance
  },
};
</script>
  
<style scoped>
/* .pies-container {
  margin: auto;
  width: 800px;
  
} */

/* .pies-container>.pie {
  float: center;
  height: 90%;
} */

#funnel {
  /* height: 440px; */
  height: 100%;
}

#funnel .label {
  font-size: 28px;
}

.dx-texteditor-input {
  border-top: none;
  border-right: none;
  border-left: none;
  border-radius: 0;
  border-bottom: 1px solid gray;
  background-color: transparent;
}

.card {
  background-color: rgb(255, 255, 255);
  color: rgb(54, 65, 82);
  transition: box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
  box-shadow: none;
  background-image: none;
  border-radius: 8px;
  overflow: hidden;
  border: none rgba(224, 224, 224, 0.596);
}

.border {
  border-width: 0px 0px thin;
  border-style: solid;
  border-color: rgb(227, 232, 239);
  color: rgb(18, 25, 38);
  font-weight: 500;
  font-family: Roboto, sans-serif;
  line-height: 1.334;
  font-size: 1.125rem;
  padding: 16px;
  text-align: left;
}

.location-box {
  background-color: #fff;
  position: absolute;
  width: 200px;
  max-height: 400px;
  box-sizing: border-box;
  box-shadow: -1px 5px 15px -3px rgba(0,0,0,0.75);
  border-radius: 8px;
  padding: 8px;
  font-size: 17px;
  z-index: 999;
  overflow-y: auto;
}
.input-box {
  border: 11px solid #000!important;
  width: 10px;
  height: 30px;
}

.bg-card {
  background-color: #fff;
  border-radius: 8px;
}
</style>