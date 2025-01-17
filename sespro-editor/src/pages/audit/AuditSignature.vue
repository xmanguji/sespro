<template>
  <AppLayout :userRole="activeUserRole"
    :back="true"
    :submit="true"
    :loading="loading"
    :imageLogo="imageLogo"
    headerTitle="Signature"
    :activeUserRole="activeUserRole"
  >
    <div class="mt-20 h-full w-full">
      <div v-if="submitSuccess" class="w-full h-full">
        <div v-if="!mailSentSuccess" class="flex flex-col justify-center items-center">
          <div class="center-div h-full">
            <span>&#10004;</span>
          </div>
          <div class="bottom-div h-full">Done</div>
        </div>
        <div v-else>
          <div class="center-div">
            <img class="logo" src="@/assets/images/icons/icon_email.png" />
            <p>Your report was sent by email</p>
          </div>
        </div>
      </div>
      <div v-else class="w-full h-full">
        <div class="h-full w-1/2 m-auto flex flex-col gap-4">
          <div class="flex-2">
            <VueSignaturePad
              ref="pad"
              class="signature-pad border-2 h-28"
            />
            <p class="flex text-Secondary">Sign here</p>
          </div>
          <div class="flex-1">
            <b-button
              type="button submit-btn"
              class="
                is-large
                bg-editIconColor
                text-white
                hover:text-white hover:bg-PrimaryDark hover:bg-opacity-50
              "
              @click="onSubmit"
              >Submit</b-button
            >
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from "@/layouts/AppLayout";
import { get, sync } from "vuex-pathify";
import API from "@/services/API";
// import AuditSignPad from "./AuditSignPad";
import ImageLogo from "@/assets/images/respro-logo.svg";

export default {
  name: "AuditSignature",
  components: { AppLayout },
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
      imageLogo: ImageLogo,
    };
  },
  computed: {
    token: get("app/session"),
    activeUserRole: sync("app/activeUserRole"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    audit: sync("audit/audits[:currentAuditIndex]"),
    audits: sync("audit/audits"),
    body: sync("audit/audits[:currentAuditIndex]@body"),
    template: get("audit/audits[:currentAuditIndex]@type"),
    selectedAuditUuid: sync("audit/selectedAuditUuid"),
  },
  methods: {
    onSubmit() {
      let currentAuditIndex = this.currentAuditIndex;
      this.$store.commit("audit/MARK_END", { currentAuditIndex });
      const loadingComponent = this.$buefy.loading.open({ container: null });

      let val = Object.assign({}, this.audit);

      delete val.auditIndex;

      let body = [];

      val.body.forEach((element) => {
        if (element["is_modified"] === true) {
          let el = element;

          el.questions = element.questions.filter((question) => {
             
            return question["is_modified"] === true;
          }).map(item =>  {

            item["passed"] = item.pass
            item["notes"] = item["note"]
            return item
          });

          body.push(el);
        } else {
          body.push(element)
        }
      });

      val["location"] = val.premises.uuid;

      val.body = body;

      // delete val.updated_time
      // delete val.submit_time
      // delete val.auditor
      // delete val.premises
      // delete val.selectedPremises
      delete val.extra

      API.submitAudit(this.token, val.uuid , val)
        .then(() => {
          API.renderReport(this.token, val.uuid)
            .then((res) => {
              console.log(res.data.status);
            })
            .catch((error) => {
              console.log(error);
            });

          loadingComponent.close();
          this.submitSuccess = true;
          this.audits = [];
          this.currentAuditIndex = 0;
          this.selectedAuditUuid = null;

          this.$buefy.dialog.alert({
            message: "You successfully updated an audit response.",
            type: "is-success",
            hasIcon: true,
            onConfirm: () => this.$router.push({ name: "home" }),
          });
        })
        .catch((error) => {
          loadingComponent.close();
          API.APILog(error);
          this.loading = false;
          this.$buefy.dialog.confirm({
            message: "Error submitting audit.",
            onConfirm: () => this.$router.push({ name: "audit" }),
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
  height: 100%;
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
          border-bottom: 2px solid #d96f18;
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
