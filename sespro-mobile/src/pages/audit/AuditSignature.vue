<template>
  <AppLayout :back="true" :submit="true" :loading="loading">
    <template>
      <div v-if="submitSuccess" class="page-container">
        <div v-if="!mailSentSuccess" class="submit-success-div">
          <div class="center-div">
            <span>&#10004;</span>
          </div>
          <div class="bottom-div">Done</div>
        </div>
        <div v-else>
          <div class="center-div">
            <img class="logo" src="../../assets/images/icons/icon_email.png" />
            <p>Your report was sent by email</p>
          </div>
        </div>
      </div>
      <div v-else class="page-container">
        <div>
          <div class="signature-div center-div">
            <VueSignaturePad
              width="100%"
              height="100px"
              ref="pad"
              class="signature-pad"
            />
            <p>Sign here</p>
          </div>
        </div>
      </div>

      <button
          @click="onSubmit"
          class="
            text-white
            rounded-md
            px-6 py-2 mb-4
            bg-PrimaryDark
          "
        >
          Submit
        </button>

    </template>
  </AppLayout>
</template>

<script>
import AppLayout from "../../layouts/AppLayout";
import { get, sync } from "vuex-pathify";
import API from "../../services/API";
import CheckAll from "vue-material-design-icons/CheckAll.vue";
import Check from "vue-material-design-icons/Check.vue";

export default {
  name: "AuditSignature",
  components: { AppLayout, CheckAll, Check },
  props: {
    parent: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      loading: false,
      submitSuccess: false,
      mailSentSuccess: false,
    };
  },
  computed: {
    token: get("app/session"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    audit: sync("audit/audits[:currentAuditIndex]"),
    body: sync("audit/audits[:currentAuditIndex]@body"),
    template: get("audit/audits[:currentAuditIndex]@type"),
  },
  methods: {
    onSubmit() {
      try {
        let currentAuditIndex = this.currentAuditIndex;
        this.$store.commit("audit/MARK_END", { currentAuditIndex });
      } catch (error) {
        if (error.name == "QuotaExceededError") {
          this.$buefy.dialog.confirm({
            message:
              "Error: you exceeded storage limit please clear cache and try again",
            onConfirm: () => this.$router.push({ name: "home" }),
          });
        }
      }
      const loadingComponent = this.$buefy.loading.open({ container: null });

      let val = Object.assign({}, this.audit);
      val.comments = 'This is ios comments';
      delete val.uuid;
      delete val.auditIndex;

      API.submitAudit(this.token, val)
        .then((r) => {
          loadingComponent.close();
          this.submitSuccess = true;

          if ("pdf" in r.data && r.data.pdf) {
            setTimeout(() => {
              this.mailSentSuccess = true;
              this.$router.push({ name: "results" });
            }, 1 * 1000);
          } else {
            this.$buefy.dialog.alert({
              message:
                "We've processed your audit, but something went wrong when trying to generate a report.",
              type: "is-danger",
              hasIcon: true,
              onConfirm: () => this.$router.push({ name: "results" }),
            });
          }
        })
        .catch((error) => {
          loadingComponent.close();
          API.APILog(error);
          this.loading = false;
          this.$buefy.dialog.confirm({
            message: "Error submitting audit.",
            onConfirm: () => this.$router.push({ name: "home" }),
          });
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.main-container {
  background: white;
}

.content-header .title {
  justify-content: center;
}

.page-container {
  height: 70%;
  color: black;
  > div {
    height: 100%;
    position: relative;
    &.submit-success-div {
      font-size: 3rem;
      span {
        height: 240px;
        width: 240px;
        border-radius: 50%;
        border: 0.5rem solid #557ee7;
        display: inline-block;
        font-size: 180px;
        line-height: 1.3;
      }
    }
    .center-div {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
      min-width: 240px;
      width: 100%;
      &.signature-div {
        top: 40%;
        > p {
          padding: 1rem;
        }
        .signature-pad {
          border-bottom: 2px solid black;
        }
      }
    }
    .bottom-div {
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
    }
  }
}
</style>
