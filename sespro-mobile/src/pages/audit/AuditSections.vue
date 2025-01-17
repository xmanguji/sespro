<template>
  <AppLayout :back="true" @back="confirmQuit" :submit="true" @submit="confirmSubmit" :loading="loading"
    :imageLogo="imageLogo" headerTitle="">

    <template>
      <div class="content-header max-w-4xl lg:mx-auto" v-if="!completeAudit">
        <p class="text-center mt-4 text-base">Please complete all sections</p>
      </div>
      <div class="flex justify-center">
        <button @click="confirmSubmit" class="
        my-8
        text-white
        h-12
        px-6
        flex
        justify-center
        items-center
        rounded-md
        bg-PrimaryDark
      ">
          Submit Audit
        </button>
      </div>

      <div class="section-lists max-w-4xl lg:mx-auto">
        <div v-for="(category, index) in this.context_cats" :key="category.uuid" class="section-list-view"
          @click="onEnterSection(index)">
          <div class="list-first-column flex flex-row items-start">
            <img class="w-8" :src="getIconPath(category.icon)" />
            <label>{{ category.text }}</label>
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
      <div class="flex justify-center">
        <button v-if="abi == null" @click="confirmQuit" class="
            text-white
            h-12
            px-6
            flex
            justify-center
            items-center
            rounded-md
            bg-gray-500
            mb-40
          ">
          Reset Audit
        </button>
      </div>
    </template>
  </AppLayout>
</template>

<script>
import AppLayout from "../../layouts/AppLayout";
import { get, sync } from "vuex-pathify";
import API from "../../services/API";
import RadialProgressBar from "vue-radial-progress";
import ImageLogo from "@/assets/images/Respro_health_and_safety_blue_bg.png";
import Undo from "vue-material-design-icons/Undo.vue";
import CheckAll from "vue-material-design-icons/CheckAll.vue";

export default {
  name: "AuditSections",
  components: { AppLayout, RadialProgressBar, Undo, CheckAll },
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
    currentAuditIndex: sync("audit/currentAuditIndex"),
    templates: sync("template/templates"),
    selectedTemplateIndex: sync("template/selectedTemplateIndex"),
    audit: sync("audit/audits[:currentAuditIndex]"),
    body: sync("audit/audits[:currentAuditIndex]@body"),
    template: sync("audit/audits[:currentAuditIndex]@type"),
    name: sync("audit/audits[:currentAuditIndex]@name"),
    root_cats: function () {
      return this.body.filter((c) => !Object.hasOwnProperty.call(c, "parent"));
    },

    context_cats: function () {
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
      this.audit.body = [];
      this.$router.push({ name: "home" });
      console.log("User voluntarily quit audit - target location wiped");
    },
    onEnterSection(index) {

      if (Object.hasOwnProperty.call(this.body[index], "children")) {
        console.log('pass.index.index ===> ', index)
        this.$router.push({
          name: "audit_sub",
          params: { abi: String(index) },
        });
      } else if (this.abi != null) {
        const si = this.context_cats[index].order;
        console.log('si.index.si ===> ', si)

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

      if (this.body.length == 0) return false;

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
      if (this.completeAudit) {
        this.$router.push({ name: "signature" });
      } else {
        this.$buefy.dialog.alert({
          message: "Please complete all question before submitting",
        });
      }
    },
    getIconPath(icon) {
      // TODO: figure out why this works
      let images = require.context(
        "../../assets/images/category/",
        false,
        /\.png$/
      );

      try {
        return images("./" + icon + ".png");
      } catch (error) {
        console.log(error);
      }
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
  },
  created() {
    document.addEventListener("backbutton", this.confirmQuit, false);
    if (this.body.length < 1) {
      this.loading = true;
      const tmp = this.templates[this.selectedTemplateIndex];
      let templateId = tmp.uuid
      this.audit.name = tmp.name
      this.audit.type = tmp.uuid

      API.getTemplate(this.token, templateId)
        .then((response) => {
          API.APILog(
            `Successfully fetched built audit template [${templateId}]`
          );
          this.audit.body = response.data.body;
          this.loading = false;
          // set start time and save audit

          try {
            let currentAuditIndex = this.currentAuditIndex;
            this.$store.commit("audit/MARK_START", { currentAuditIndex });
          } catch (error) {
            if (error.name == "QuotaExceededError") {
              this.$buefy.dialog.confirm({
                message:
                  "Error: you exceeded storage limit please clear cache and try again",
                onConfirm: () => this.$router.push({ name: "home" }),
              });
            }
          }
        })
        .catch((error) => {
          API.APILog(error);
          this.loading = false;
          this.$buefy.dialog.alert({
            message: "Error fetching audit data.",
            onConfirm: () => this.$router.push({ name: "home" }),
          });
        });
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
.main-container {
  background: white;
}

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

  &:not(:last-child) {
    border-bottom: 1px solid lightgray;
  }

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
      color: #4a4d4a;
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
