<template>
  <!-- <div class="hint-page">
    <div class="hint-container"> -->
  <div class="challenge-questions">
    <div
      class="challenge-question"
      v-for="question in questions"
      :key="question.uuid"
      @click="$emit('onSelectChallengeQuestion', $event, question)"
    >
      <p>{{ question.text }}</p>
    </div>
  </div>
  <!-- </div>
  </div> -->
</template>


<script>
export default {
  name: "AuditChallengeQuestions",
  props: {
    questions: {
      type: Array,
    },
  },
};
</script>

<style lang="scss" scoped>
.challenge-questions {
  height: 100%;
  width: 100%;
  background-color: #ffffff;
  border-radius: 0.25rem;
  padding: 0;
  margin: auto;
  overflow-y: scroll;
  display: flex;
  flex-direction: column;
  .challenge-question {
    padding: 1rem;
    border-bottom: 1px solid;
  }
}
</style>
