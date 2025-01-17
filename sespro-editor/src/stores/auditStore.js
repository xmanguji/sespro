import { make } from "vuex-pathify";

import { v4 as uuidv4 } from "uuid";
const state = {
  audits: [],
  currentAuditIndex: 0,
  selectedAuditUuid: null,
};

const mutations = {
  ...make.mutations(state),
  SET_QUESTION(state, { currentAuditIndex, category, question, result }) {
    state.audits[currentAuditIndex].body[category]["questions"][
      question
    ].pass = result;
    state.audits[currentAuditIndex].body[category]["questions"][question][
      "is_modified"
    ] = true;
    state.audits[currentAuditIndex].body[category]["is_modified"] = true;
    delete state.audits[currentAuditIndex].body[category]["questions"][question]
      .skipped;
  },
  SET_NOTE(state, { currentAuditIndex, category, qIndex, value }) {
    state.audits[currentAuditIndex].body[category]["questions"][
      qIndex
    ].note = value;
    state.audits[currentAuditIndex].body[category]["questions"][qIndex][
      "is_modified"
    ] = true;
    state.audits[currentAuditIndex].body[category]["is_modified"] = true;
  },
  SET_PICKED(state, { currentAuditIndex, category, qIndex, value }) {
    if (value === true) {
      let question = Object.assign(
        {},
        state.audits[currentAuditIndex].body[category]["questions"][qIndex]
      );
      let resultUuid = uuidv4();
      question.picked = value;
      question.resultUuid = resultUuid;
      state.audits[currentAuditIndex].body[category]["questions"].push(
        question
      );
    } else {
      delete state.audits[currentAuditIndex].body[category]["questions"][
        qIndex
      ];
    }
  },
  SKIP_QUESTION(state, { currentAuditIndex, category, question }) {
    state.audits[currentAuditIndex].body[category]["questions"][
      question
    ].skipped = true;
    delete state.audits[currentAuditIndex].body[category]["questions"][question]
      .pass;
  },
  MARK_END(state, { currentAuditIndex }) {
    state.audits[currentAuditIndex]["updated_time"] = Math.round(
      +new Date() / 1000
    );
  },

  CHANGE_CURRENT_LOCATION(state, {currentAuditIndex, name, uuid}) {
    state.audits[currentAuditIndex]["selectedPremises"]["name"] = name;
    state.audits[currentAuditIndex]["selectedPremises"]["uuid"] = uuid;
  },
};

const actions = {
  ...make.actions(state),
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
