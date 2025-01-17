<template>  
  <AppLayout :userRole="activeUserRole" :back="false" headerTitle="Failures Report" :activeUserRole="activeUserRole">
    <template v-if="isData()">
      <div class="flex flex-row justify-evenly mt-12">
        <Donut
          type="pie"
          :data="failuresData"
          class="mt-4"
          :options="options"
        ></Donut>
        <div class="section-lists">
          <div v-for="(label, index) in failuresData.labels" :key="index">
            <div
              v-if="
                getFailurePercent(failuresData.datasets[0].data[index]) !== 0
              "
              class="section-list-view border-b"
            >
              <div class="list-first-column">
                <img
                  class="logo"
                  :src="getIconPath(failuresData.icons[index])"
                />
                <label>{{ label }}</label>
              </div>
              <div class="list-second-column">
                <span class="text-xl text-Secondary font-bold"
                  >{{
                    getFailurePercent(failuresData.datasets[0].data[index])
                  }}%</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <h1 v-else class="alt-title">No failures!</h1>
    <div class="button-audit-action">
      <b-button type="button" class="is-large is-info" @click="onFinish"
        >Done</b-button
      >
    </div>
  </AppLayout>
</template>

<script>
import { sync } from "vuex-pathify";
import Donut from "../Donut";
import AppLayout from "@/layouts/AppLayout";

export default {
  name: "AuditGraph",
  components: { Donut, AppLayout },
  computed: {
    activeUserRole: sync("app/activeUserRole"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    body: sync("audit/audits[:currentAuditIndex]@body"),
    audit: sync("audit/audits[:currentAuditIndex]"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
  },
  data() {
    return {
      options: {
        segmentShowStroke: false,
        legend: {
          display: false,
        },
      },
      failuresData: null,
      totalFailures: 0,
    };
  },
  methods: {
    isData() {
      return this.failuresData && this.failuresData.labels.length !== 0;
    },
    getData() {
      let fmap = [];

      for (const category of this.body) {
        let failures = 0;

        if ("challenge" in category) {
          for (const question of category.questions) {
            if ("pass" in question && "picked" in question && question.picked) {
              if (!question.pass) {
                failures += 1;
              }
            }
          }
        } else {
          for (const question of category.questions) {
            if ("pass" in question) {
              if (!question.pass) {
                failures += 1;
              }
            } else if ("skipped" in question) {
              continue;
            } else {
              failures += 1;
            }
          }
        }

        const obj = {
          uuid: category.uuid,
          text: category.text,
          fc: failures,
          color: category.color,
          qc: category.questions.length,
          icon: category.icon,
        };

        if ("parent" in category) {
          obj.parent = category.parent;
        }

        fmap.push(obj);
      }

      let counts = [];
      let labels = [];
      let colors = [];
      let qcounts = [];
      let icons = [];

      for (const obj of fmap) {
        if ("parent" in obj) {
          const p = fmap.find((e) => e.uuid === obj.parent);
          const pi = labels.findIndex((e) => e === p.text);

          if (pi !== -1) {
            counts[pi] += obj.fc;
          } else {
            counts.push(obj.fc);
            labels.push(p.text);
            colors.push(p.color);
            icons.push(p.icon);
          }
        } else {
          const ci = labels.findIndex((e) => e === obj.text);

          if (ci !== -1) {
            counts[ci] += obj.fc;
          } else {
            counts.push(obj.fc);
            labels.push(obj.text);
            colors.push(obj.color);
            icons.push(obj.icon);
          }
        }
      }

      return {
        datasets: [
          {
            label: "# of Failures",
            data: counts,
            backgroundColor: colors,
            qdata: qcounts,
          },
        ],
        labels: labels,
        icons: icons,
      };
    },
    onFinish() {
      this.audit.location = null;
      this.audit.body = [];
      this.$router.push({ name: "home" });
    },
    getTotal() {
      if (this.failuresData.datasets && this.failuresData.datasets[0].data) {
        return this.failuresData.datasets[0].data.reduce((a, b) => a + b);
      } else {
        return 0;
      }
    },
    getIconPath(icon) {
      let images = require.context(
        "../../assets/images/category/",
        false,
        /\.png$/
      );
      return images("./" + icon + ".png");
    },
    getFailurePercent(failureCnt) {
      this.totalFailures = this.getTotal();
      if (this.totalFailures == 0) {
        return 0;
      } else {
        return Number(((failureCnt / this.totalFailures) * 100).toFixed(1));
      }
    },
  },
  mounted() {
    this.failuresData = this.getData();
  },
};
</script>

<style lang="scss" scoped>
.alt-title {
  padding-top: 50%;
  font-size: 52px;
}
Donut {
  width: 100%;
  height: 100%;
}

.main-container {
  background: white;
}
.content-header .title {
  justify-content: center;
  margin-bottom: 1rem;
}
.section-list-view {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin: 0 -1rem;
  line-height: 1;
  &:not(:last-child) {
    border-bottom: 1px solid rgb(150, 150, 150);
  }
  .list-first-column {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding-right: 0.5rem;
    .logo {
      max-width: 2rem;
      max-height: 2rem;
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
    width: 4rem;
    span.failure-badge {
      border-radius: 5rem;
      background: #d00e4e;
      display: inline-block;
      padding: 0.375rem 0.5rem;
      width: 60px;
      color: white;
      text-align: right;
    }
  }
}

.button-audit-action {
  padding: 1rem;
}
</style>
