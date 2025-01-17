<template>
  <AppLayout :userRole="activeUserRole" :back="true" @back="confirmQuit" :submit="true" @submit="confirmSubmit"
    :loading="loading" :imageLogo="imageLogo" headerTitle="Audit Sections" :activeUserRole="activeUserRole">
    <div class="
            flex-1 flex flex-row
            button-audit-action
            bg-white
            text-onyx
            mt-6
          ">
      <div class="flex-1 flex-col justify-start mb-3">
        <label class="flex-1 text-onyx">Select Location</label>
        <select v-model="selected" @change="updateSelectedPremises(selected)"
          class="flex-2 p-2 mx-3 rounded border-none min-w-min">
          <option v-for="option in premises" :key="option.uuid" :value="option">
            {{ option.name }}
          </option>
        </select>
      </div>
      <b-button type="button" class="
              flex
              is-large
              bg-editIconColor
              text-onyx
              hover:text-onyx hover:bg-white hover:bg-opacity-50
            " @click="confirmSubmit">Submit Audit</b-button>
    </div>

    <div class="flex-2 section-lists px-8 bg-white text-onyx">
      <div v-for="(category, index) in this.context_cats" :key="category.uuid" class="
              section-list-view
              border-opacity-20 border-b border-SecondaryLight
            " @click="onEnterSection(index)">
        <div class="list-first-column flex flex-row items-start text-onyx">
          <img class="w-8" />
          <label class="text-onyx">{{ category.text }}</label>
        </div>
        <div class="list-second-column">
          <radial-progress-bar :diameter="50" :completed-steps="getProgress(category)" :total-steps="100"
            :stroke-width="3" :inner-stroke-width="3" inner-stroke-color="#E1E1E1" start-color="#1d3e57"
            stop-color="#1d3e57" :animate-speed="0">
            <label class="porgess-label" style="font-size: ">{{ getProgress(category) }}%</label>
          </radial-progress-bar>
        </div>
      </div>
    </div>

    <!-- <div class="mt-20">
      <div>Final Comments</div>
      <div>{{audit.final_comments || '-'}}</div>
    </div> -->
    
  </AppLayout>
</template>

<script>
import AppLayout from "@/layouts/AppLayout";

import { get, sync } from "vuex-pathify";
import API from "@/services/API";
import RadialProgressBar from "vue-radial-progress";
import ImageLogo from "@/assets/images/respro-logo.svg";

export default {
  name: "AuditSections",
  components: { AppLayout, RadialProgressBar },
  props: {
    parent: {
      type: String,
      default: null,
    },
    abi: {
      type: Number,
    },
  },
  data() {
    return {
      loading: false,
      completeAudit: false,
      parentSection: null,
      imageLogo: ImageLogo,
    };
  },
  computed: {
    token: get("app/session"),
    activeUserRole: sync("app/activeUserRole"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    audit: sync("audit/audits[:currentAuditIndex]"),
    audits: sync("audit/audits"),
    body: get("audit/audits[:currentAuditIndex]@body"),
    template: get("audit/audits[:currentAuditIndex]@type"),
    selectedAuditUuid: get("audit/selectedAuditUuid"),
    premises: get("app/premises"),
    selectedPremises: get("audit/audits[:currentAuditIndex]@selectedPremises"),
    root_cats: function () {
      return this.body.filter((c) => !Object.hasOwnProperty.call(c, "parent"));
    },

    context_cats: function () {
      // console.log('this.audit ===========>', this.audit)
      if (this.abi != null) {
        return this.body.filter(
          (c) =>
            Object.hasOwnProperty.call(c, "parent") &&
            c.parent === this.body[this.abi].uuid
        );
      } else {
        return this.root_cats;
      }
    },
  },
  methods: {
    onBack() {
      this.audit.location = null;
      this.currentAuditIndex = -1;
      this.body = [];
      this.$router.push({ name: "home" });
      console.log("User voluntarily quit audit - target location wiped");
    },
    onEnterSection(index) {
      if (Object.hasOwnProperty.call(this.body[index], "children")) {
        this.$router.push({
          name: "audit_sub",
          params: { abi: String(index) },
        });
      } else if (this.abi != null) {
        const si = this.context_cats[index].order;
        this.$router.push({
          name: "section",
          params: { abi: si },
        });
      } else {
        this.$router.push({ name: "section", params: { abi: index } });
      }
    },
    confirmQuit() {
      if (this.parent != null) {
        this.parent = null;
      } else {
        this.$buefy.dialog.confirm({
          message: "Are you sure you want to reset this audit?",
          onConfirm: () => this.onBack(),
        });
      }
    },
    checkQuestions() {
      let challenge = 0;
      let cs = 0;

      if (!this.body || this.body.length == 0) return false;

      for (const category of this.body) {
        if (Object.prototype.hasOwnProperty.call(category, "challenge")) {
          challenge = true;
          for (const question of category.questions) {
            if (
              question &&
              Object.prototype.hasOwnProperty.call(question, "note") &&
              Object.prototype.hasOwnProperty.call(question, "pass")
            ) {
              cs += 1;
            }
          }
        } else {
          for (const question of category.questions) {
            if (
              question &&
              !Object.prototype.hasOwnProperty.call(question, "pass")
            ) {
              if (!Object.prototype.hasOwnProperty.call(question, "skipped")) {
                return false;
              }
            }
          }
        }
      }

      if (challenge > 0) {
        return cs === challenge * 5;
      }

      return true;
    },
    confirmSubmit() {
      this.$router.push({ name: "signature" });
    },
    getIconPath(icon) {
      // TODO: figure out why this works
      // let images = require.context(
      //   "../../assets/images/category/",
      //   false,
      //   /\.png$/
      // );
      // return images("./" + icon + ".png");
      return icon == "" ? null : null;
    },
    getCompleteCount(category) {
      if ("challenge" in category) {
        return category.questions.filter(
          (q) =>
            q &&
            ((Object.prototype.hasOwnProperty.call(q, "pass") &&
              Object.prototype.hasOwnProperty.call(q, "note") &&
              q.note) ||
              Object.prototype.hasOwnProperty.call(q, "skipped"))
        ).length;
      } else {
        return category.questions.filter(
          (q) =>
            q &&
            (Object.prototype.hasOwnProperty.call(q, "pass") ||
              Object.prototype.hasOwnProperty.call(q, "skipped"))
        ).length;
      }
    },
    getProgress(category) {
      if ("children" in category) {
        let children = this.body.filter(
          (c) => "parent" in c && c.parent === category.uuid
        );
        let cprog = [];

        for (const c of children) {
          cprog.push(
            Math.ceil((this.getCompleteCount(c) / c.questions.length) * 100)
          );
        }

        return cprog.reduce((a, b) => a + b, 0) / cprog.length;
      } else if ("challenge" in category) {
        return Math.min(
          100,
          Math.ceil((this.getCompleteCount(category) / 5) * 100)
        );
      } else {
        return Math.ceil(
          (this.getCompleteCount(category) / category.questions.length) * 100
        );
      }
    },
    updateSelectedPremises(selected) {
      let currentAuditIndex = this.currentAuditIndex;
      let name = selected["name"];
      let uuid = selected["uuid"];
      this.$store.commit("audit/CHANGE_CURRENT_LOCATION", {
        currentAuditIndex,
        name,
        uuid,
      });
    },
  },
  created() {
    document.addEventListener("backbutton", this.confirmQuit, false);
    if (!this.body || this.body.length < 1) {
      const loadingComponent = this.$buefy.loading.open({ container: null });
      const templateId = this.selectedAuditUuid;
      this.loading = true;
      API.getAudit(this.token, templateId)
        .then((response) => {
          API.APILog(
            `Successfully fetched built audit template [${templateId}]`
          );
          this.audits[this.currentAuditIndex] = {
            ...this.audit,
            ...response.data,
          };

          let sorted_body = response.data.body

          sorted_body.sort((a, b) => a.order - b.order);

          sorted_body.forEach((category) => {
            if (category.questions) {

              category.questions.map(item => {

                if (item.images) {
                  item["photo_url"] = item.images;
                }

                return item;
              })

              category.questions.sort((a, b) => a.order - b.order);
            }
          });

          this.audit["body"] = sorted_body;

          console.log(response.data.body)

          this.loading = false;
          loadingComponent.close();
          // set start time and save audit
        })
        .catch((error) => {
          API.APILog(error);
          this.$buefy.dialog.alert({
            message: "Error fetching audit data.",
            onConfirm: () => this.$router.push({ name: "home" }),
          });
          this.loading = false;
          loadingComponent.close();
        });
    }

    if (null == this.selected) {
      this.selected = this.selectedPremises;
    }
  },
  beforeDestroy() {
    document.removeEventListener("backbutton", this.confirmQuit, false);
  },
  mounted() {
    this.completeAudit = this.checkQuestions();
  },
};
</script>

<style lang="scss" scoped>
// .main-container {
//   background: black;
// }

.section-lists {
  &:last-child {
    padding-bottom: 1rem;
  }
}

.section-list-view {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0.5rem;
  margin: 0 2px;
  line-height: 1;

  .list-first-column {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;

    .logo {
      max-width: 3rem;
      max-height: 3rem;
      border-radius: 0.7rem;
    }

    label {
      color: black;
      cursor: pointer;
      text-align: left;
      font-weight: 500;
      margin-left: 0.5rem;
    }
  }

  .list-second-column {
    .porgess-label {
      font-size: 10pt;
    }
  }
}

.button-audit-action {
  padding: 1rem;
}
</style>
