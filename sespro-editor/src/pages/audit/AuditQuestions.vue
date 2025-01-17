<template>
  <AppLayout :userRole="activeUserRole"
    :back="true"
    :imageLogo="defaultImage"
    @back="onBack"
    headerTitle="Audit Questions"
    :loading="loading"
    :activeUserRole="activeUserRole"
  >
  <div class="m-6 bg-lightBg">

    <div class="px-12" v-if="isChallenge">
      <p
        class="subtitle text-left mt-3 text-onyx"
        v-if="pageQuestions.length < 5"
      >
        Answer {{ 5 - pageQuestions.length }} questions to complete this section
      </p>
    </div>
    <div class="px-12 text-onyx" v-if="isChallenge">
      <div
        class="questions-div"
        v-if="pageQuestions && pageQuestions.length > 0 && isChallenge"
      >
        <div
          v-for="question in pageQuestions"
          :class="[
            'question-container',
            question.pass != null && question.pass === true ? 'passed' : '',
            question.pass != null && question.pass === false ? 'failed' : '',
          ]"
          :key="question.resultUuid"
        >
          <p
            class="question-text text-onyx"
            @click="onTapQuestion(question.resultUuid)"
          >
            <span v-if="!challenge()">{{ question.order + 1 }}.</span>
            <vue-simple-markdown
              class="text-onyx"
              :source="question.text"
            ></vue-simple-markdown>
          </p>
          <div
            :class="['useraction-div', 'useraction-div-challenge']"
            class="text-onyx"
          >
            <div class="radio-btn-cnt">
              <b-radio
                native-value="info"
                type="is-success"
                :name="question.resultUuid"
                class="radio-btn-custom text-onyx"
                :value="getState(question)"
                @input="pass(question)"
                >Pass</b-radio
              >
              <b-radio
                native-value="danger"
                type="is-danger"
                :name="question.resultUuid"
                class="radio-btn-custom radio-btn-margin"
                :value="getState(question)"
                @input="fail(question)"
                >Fail</b-radio
              >
              <b-radio
                v-if="'optional' in question"
                native-value="skipped"
                type="is-black"
                class="radio-btn-custom radio-btn-margin"
                :value="getState(question)"
                @input="skip(question)"
                >N/A</b-radio
              >
              <img
                class="info-icon"
                src="../../assets/info_icon.png"
                @click="onShowHint(question)"
              />
            </div>
            <div
              v-if="
                (!hasPassed(question) &&
                  !hasSkipped(question) &&
                  hasAnswered(question)) ||
                  challenge()
              "
            >
              <input
                @keyup.enter="onKeyEnter(question, $event)"
                class="input-field input-nonconformity my-2 h-12 bg-black shadow-none border-l-0 border-r-0 border-t-0 border-gray-400 text-white font-sans rounded-none "
                @change="saveNote(question, $event)"
                :value="getNote(question)"
                :placeholder="challenge() ? 'Answer' : 'Enter Nonconformity'"
              />
              <div
                v-if="!challenge()"
                class="input-field"
                @click="onCamera(question)"
              >
                <div class="input-field-photo text-lg ">
                  <img
                    class="camera-icon logo"
                    src="../../assets/images/icons/icon_camera.png"
                  />
                  <label>{{
                    hasPhoto(question) ? "Retake Photo" : "Take a Photo"
                  }}</label>
                  <input
                    :ref="'camera' + question.order"
                    @change="onCapture(question)"
                    class="hidden-camera-input"
                    type="file"
                    capture="environment"
                    accept="image/jpeg;image/jpg"
                  />
                </div>
              </div>
              <div
                v-if="!challenge() && question.photo_url"
                style="text-align: center"
              >
                <img  style="width: 50%" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="px-12" v-else>
      <div
        class="questions-div"
        v-if="pageQuestions && pageQuestions.length > 0"
      >
        <div
          v-for="question in pageQuestions"
          :class="[
            'question-container',
            question.pass != null && question.pass === true ? 'passed' : '',
            question.pass != null && question.pass === false ? 'failed' : '',
          ]"
          :key="question.uuid"
          :data-id="question.order"
        >
          <p class="question-text w-full text-left inline-flex justify-start" @click="onTapQuestion(question.uuid)">
            <span v-if="!challenge()">{{ question.order + 1 }}.</span>
            <vue-simple-markdown :source="question.text"></vue-simple-markdown>
          </p>
          <div
            :class="[
              'useraction-div',
              isChallenge ? 'useraction-div-challenge' : '',
            ]"
          >
            <div class="radio-btn-cnt">
              <b-radio
                native-value="info"
                type="is-success"
                class="radio-btn-custom"
                :name="question.uuid"
                :value="getState(question)"
                @input="pass(question)"
                >Pass</b-radio
              >
              <b-radio
                native-value="danger"
                type="is-danger"
                :name="question.uuid"
                class="radio-btn-custom radio-btn-margin"
                :value="getState(question)"
                @input="fail(question)"
                >Fail</b-radio
              >
              <b-radio
                v-if="'optional' in question"
                native-value="skipped"
                type="is-black"
                class="radio-btn-custom radio-btn-margin"
                :value="getState(question)"
                @input="skip(question)"
                >N/A</b-radio
              >
              <img
                class="info-icon"
                src="../../assets/info_icon.png"
                @click="onShowHint(question)"
              />
            </div>
            <div
              v-if="
                (!hasSkipped(question) &&
                  hasAnswered(question)) ||
                  challenge()
              "
            >
              <input
                @keyup.enter="onKeyEnter(question, $event)"
                class="input-field input-nonconformity my-2 h-12 shadow-none border-l-0 border-r-0 border-t-0 border-gray-400 text-gray-600 font-sans rounded-none "
                @change="saveNote(question, $event)"
                :value="getNote(question)"
                :placeholder="challenge() ? 'Answer' : 'Enter Nonconformity'"
              />
              <div
                v-if="!challenge()"
                class="input-field"
                @click="onCamera(question)"
              >
                <div class="input-field-photo text-lg ">
                  <img
                    class="camera-icon logo"
                    src="../../assets/camera_icon.png"
                  />
                  <label>{{
                    hasPhoto(question) ? "Retake Photo" : "Take a Photo"
                  }}</label>
                  <input
                    :ref="'camera' + question.order"
                    @change="onCapture(question)"
                    class="hidden-camera-input"
                    type="file"
                    capture="environment"
                    accept="image/jpeg;image/jpg"
                  />
                </div>
              </div>
              <div
                v-if="!challenge() && question.photo_url"
                style="text-align: center"
              >
                <img :src="question.photo_url" style="width: 50%" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="px-12 button-pick-question" v-if="isChallenge">
      <b-button
        type="button"
        class="is-large is-info"
        @click="onPickQuestion"
        v-if="pageQuestions.length < 5"
        >{{
          pageQuestions.length > 0 ? "Pick Next Question" : "Pick A question"
        }}</b-button
      >
      <p
        class="is-size-7"
        style="padding: 1.5rem 0"
        v-if="pageQuestions.length > 0"
      >
        Tap three times on a question to remove it.
      </p>
    </div>
  </div>
  </AppLayout>
</template>

<script>
import AppLayout from "@/layouts/AppLayout";
import { get, sync } from "vuex-pathify";
import API from "@/services/API";
import AuditQuestionsChallenge from "./AuditChallengeQuestions.vue";
import ImageLogo from "@/assets/images/respro-logo.svg";

export default {
  name: "AuditQuestions",
  components: { AppLayout },
  props: {
    abi: Number, // The category index
    parent: String, // if defined use on back
  },
  data() {
    return {
      defaultImage: ImageLogo,
      loading: false,
      isChallenge: false,
      tapHistory: {
        uuid: null,
        count: 0,
      },
      pageQuestions: [],
    };
  },
  computed: {
    token: get("app/session"),
    activeUserRole: sync("app/activeUserRole"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    selectedAuditUuid: sync("audit/selectedAuditUuid"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
    category: sync("audit/audits[:currentAuditIndex]@body[:abi]"),
    audit: sync("audit/audits[:currentAuditIndex]"),
  },
  methods: {
    challengesAnswered: function() {
      return this.category.questions.filter((q) => "notes" in q).length;
    },
    challenge: function() {
      return "challenge" in this.category;
    },
    setQuestion(currentAuditIndex, category, question, result) {
      this.$store.commit("audit/SET_QUESTION", {
        currentAuditIndex,
        category,
        question,
        result,
      });
    },
    setNote(currentAuditIndex, category, qIndex, value) {
      this.$store.commit("audit/SET_NOTE", {
        currentAuditIndex,
        category,
        qIndex,
        value,
      });
    },
    skipQuestion(currentAuditIndex, category, question) {
      this.$store.commit("audit/SKIP_QUESTION", {
        currentAuditIndex,
        category,
        question,
      });
    },
    setPicked(currentAuditIndex, category, qIndex, value) {
      this.$store.commit("audit/SET_PICKED", {
        currentAuditIndex,
        category,
        qIndex,
        value,
      });
      this.updatePageQuestions();
    },
    updatePageQuestions() {
      if (this.isChallenge) {
        this.pageQuestions = this.category.questions.filter(
          (item) => item && item.picked != null && item.picked === true
        );
      } else this.pageQuestions = this.category.questions;
    },
    onBack() {
      if (this.parent !== undefined) {
        this.$router.push({ name: "audit", params: { parent: this.parent } });
      } else {
        this.$router.push({ name: "audit" });
      }
    },
    onShowHint(question) {
      let q = this.category.questions.find(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        q = this.category.questions.find(
          (item) => item && item.resultUuid == question["resultUuid"]
        );
      }
      this.$router.push({ name: "hint", params: { hint: q.hint } });
    },
    hasPassed(question) {
      let q = this.category.questions.find(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        q = this.category.questions.find(
          (item) => item && item.resultUuid == question["resultUuid"]
        );
      }

      return Object.prototype.hasOwnProperty.call(q, "pass") && q.pass;
    },
    pass(question) {
      let qindex = this.category.questions.findIndex(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        qindex = this.category.questions.findIndex(
          (item) => item && item.resultUuid == question["resultUuid"]
        );
      }

      this.setQuestion(
        this.currentAuditIndex,
        this.category.order,
        qindex,
        true
      );
      this.$forceUpdate();
    },
    fail(question) {
      let qindex = this.category.questions.findIndex(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        qindex = this.category.questions.findIndex(
          (item) => item && item.resultUuid == question["resultUuid"]
        );
      }

      this.setQuestion(
        this.currentAuditIndex,
        this.category.order,
        qindex,
        false
      );
      this.$forceUpdate();
    },
    hasSkipped(question) {
      let q = this.category.questions.find(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        q = this.category.questions.find(
          (item) => item && item.resultUuid == question["resultUuid"]
        );
      }

      return Object.prototype.hasOwnProperty.call(q, "skipped") && q.skipped;
    },
    skip(qindex) {
      this.skipQuestion(this.currentAuditIndex, this.category.order, qindex);
      this.$forceUpdate();
    },
    hasAnswered(question) {
      let q = this.category.questions.find(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        q = this.category.questions.find(
          (item) => item && item.resultUuid == question["resultUuid"]
        );
      }

      return (
        Object.prototype.hasOwnProperty.call(q, "pass") ||
        this.hasSkipped(question)
      );
    },
    getState(question) {
      if (!this.hasAnswered(question)) {
        return "nothing";
      } else if (this.hasPassed(question)) {
        return "info";
      } else if (this.hasSkipped(question)) {
        return "skipped";
      } else {
        return "danger";
      }
    },

    // question peripherals
    saveNote(question, event) {
      let notes = event.target.value;

      if (notes !== "") {
        let qindex = this.category.questions.findIndex(
          (item) => item && item.uuid == question.uuid
        );

        if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
          qindex = this.category.questions.findIndex(
            (item) => item && item.resultUuid == question["resultUuid"]
          );
        }

        this.category.questions[qindex]["notes"] = notes;
        this.setNote(this.currentAuditIndex, this.category.order, qindex, notes);
        this.$forceUpdate();
      }
    },
    onKeyEnter(question, event) {
      event.target.blur();
      this.saveNote(question, event);
    },
    getNote(question) {
      let q = this.category.questions.find(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        q = this.category.questions.find(
          (item) => item && item.resultUuid == question["resultUuid"]
        );
      }

      if (Object.prototype.hasOwnProperty.call(q, "notes")) {
        return q.notes;
      } else if(Object.prototype.hasOwnProperty.call(q, "note")) {
        return q.note
      }
      else {
        return null;
      }
    },
    hasPhoto(question) {
      let q = this.category.questions.find(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        q = this.category.questions.find(
          (item) => item && item.resultUuid == question["resultUuid"]
        );
      }

      return Object.prototype.hasOwnProperty.call(q, "photo");
    },
    onCamera(question) {
      let q = this.category.questions.find(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        q = this.category.questions.find(
          (item) => item && item.uuid == question["resultUuid"]
        );
      }

      const camera = this.$refs["camera" + q.order];
      camera[0].click();
    },
    onCapture(question) {
      let qindex = this.category.questions.findIndex(
        (item) => item && item.uuid == question.uuid
      );

      if (Object.prototype.hasOwnProperty.call(question, "resultUuid")) {
        qindex = this.category.questions.findIndex(
          (item) => item && item.resultUuid == question["resultUuid"]
        );
      }

      const q = this.category.questions[qindex];

      const f = this.$refs["camera" + q.order][0].files[0];
      let reader = new FileReader();
      reader.readAsDataURL(f);

      const that = this;
      this.loading = true;
      reader.onload = function() {
        API.submitImage(
          that.token,
          that.selectedAuditUuid,
          that.location,
          q.uuid,
          reader.result.replace(/^data:image\/[a-z]+;base64,/, "")
        )
          .then((r) => {
            if (r.data.upload === true) {
              API.APILog("API saved photo");
            }
            that.$forceUpdate();
            that.category.questions[qindex]["photo"] = true;
            that.category.questions[qindex]["photo_url"] = r.data.uri;
            that.loading = false;
          })
          .catch((error) => {
            API.APILog("Error submitting photo");
            API.APILog(error);
            that.loading = false;
            that.$buefy.dialog.alert("Error processing photo");
          });
      };

      reader.onerror = function(error) {
        console.log(error);
        that.$buefy.dialog.alert("Error processing photo");
      };
    },
    onPickQuestion() {
      const seletableQuestions = this.category.questions.filter((item) => {
        return (
          item && !Object.prototype.hasOwnProperty.call(item, "resultUuid")
        );
      });
      const dialog = this.$buefy.modal.open({
        parent: this,
        component: AuditQuestionsChallenge,
        hasModalCard: false,
        customClass: "challenge-questions-dialog",
        trapFocus: true,
        props: {
          questions: seletableQuestions,
        },
        events: {
          onSelectChallengeQuestion: (event, question) => {
            const qIndex = this.category.questions.findIndex(
              (item) => item && item.uuid == question.uuid
            );
            this.setPicked(
              this.currentAuditIndex,
              this.category.order,
              qIndex,
              true
            );
            dialog.close();
          },
        },
      });
    },
    onTapQuestion(questionUuid) {
      if (this.tapHistory.uuid == questionUuid) {
        this.tapHistory.count++;
        if (this.tapHistory.count == 3) {
          let qIndex = this.category.questions.findIndex(
            (item) => item && item.resultUuid == questionUuid
          );

          this.setPicked(
            this.currentAuditIndex,
            this.category.order,
            qIndex,
            false
          );
          this.tapHistory = { uuid: null, count: 0 };
        }
      } else {
        this.tapHistory.uuid = questionUuid;
        this.tapHistory.count = 1;
      }
    },
  },
  mounted() {
    this.isChallenge = this.challenge();
    this.updatePageQuestions();
  },
};
</script>

<style lang="scss" scoped>
.main-container {
  .questions-div {
    margin: 1rem -1rem;
    .question-container {
      margin-top: 5px;
      text-align: left;
      padding: 5px 10px;
      border-bottom: 0.8px solid rgb(150, 150, 150);
      &:last-child {
        border: none;
      }
      &.passed {
        border-left: 0.25rem solid lightgreen;
      }
      &.failed {
        border-left: 0.25rem solid lightcoral;
      }
      .question-text {
        > span {
          float: left;
          font-weight: bold;
          margin-right: 0.5rem;
        }
      }
      .useraction-div {
        display: flex;
        flex-direction: column;
        // > div:not(:last-child) {
        //   border-bottom: 1px solid rgb(150, 150, 150);
        // }
        &.useraction-div-challenge {
          flex-direction: column-reverse;
          // > div:not(:first-child) {
          //   border-bottom: 1px solid rgb(150, 150, 150);
          // }
        }
      }
    }
  }
}

.radio-btn-cnt {
  width: 100%;
  display: flex;
  justify-content: left;
  align-items: center;
  padding-left: 8px;
  height: 50px;
}

.b-radio.radio input[type="radio"]:checked + .check {
  border-color: black;
}

.b-radio.radio input[type="radio"]:checked + .check:before {
  transform: scale(1) !important;
}

.radio-btn-margin {
  margin: 0 20px !important;
}

.info-icon {
  height: 21px;
}

.input-field {
  border-width: 0 0 1px 0 !important;
  border-color: rgb(150, 150, 150);
  border-radius: 0 !important;
  box-shadow: none;
  padding-left: 8px;
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  height: 50px;
  border: none !important;
}
.input-field label {
  padding-left: 8px;
  font-size: 13px;
  color: rgb(95, 94, 94);
  // font-weight: bold;
  margin-left: 10px;
}

div.input-field {
  display: flex;
  align-items: center;
  justify-content: space-between;
  > div {
    display: flex;
    align-items: center;
    label {
      margin-left: 0.5rem;
    }
  }
}

.hidden-camera-input {
  display: none;
}
</style>

<style lang="scss">
.button-pick-question {
  padding: 1rem 0;
}

.input-field-photo > label,
.questions-div,
.vue-simple-markdown.markdown-body,
.input-field {
  color: black !important;
}
</style>
