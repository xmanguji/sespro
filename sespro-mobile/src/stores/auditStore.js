import {
    make
} from "vuex-pathify";

import { v4 as uuidv4 } from 'uuid';
const state = {
    audits: [],
    currentAuditIndex: -1
};

const mutations = {
    ...make.mutations(state),
    SET_QUESTION(state, {
        currentAuditIndex,
        category,
        question,
        result
    }) {
        state.audits[currentAuditIndex].body[category]["questions"][question].pass = result;
        delete state.audits[currentAuditIndex].body[category]["questions"][question].skipped;
    },
    SET_NOTE(state, {
        currentAuditIndex,
        category,
        qIndex,
        value
    }) {
        state.audits[currentAuditIndex].body[category]["questions"][qIndex].note = value;  
    },
    SET_PICKED(state, {
        currentAuditIndex,
        category,
        qIndex,
        value
    }) {
        if(value === true) {
            let question = Object.assign({}, state.audits[currentAuditIndex].body[category]["questions"][qIndex]);
            let resultUuid = uuidv4();
            question.picked = value;
            question.resultUuid = resultUuid;
            state.audits[currentAuditIndex].body[category]["questions"].push(question);
        } else {
           delete state.audits[currentAuditIndex].body[category]["questions"][qIndex];
        }        
        
    },
    SKIP_QUESTION(state, {
        currentAuditIndex,
        category,
        question
    }) {
        state.audits[currentAuditIndex].body[category]["questions"][question].skipped = true;
        delete state.audits[currentAuditIndex].body[category]["questions"][question].pass;
    },

    MARK_START(state, {
        currentAuditIndex}) {
        state.audits[currentAuditIndex].stime = Math.round((+new Date()) / 1000);
    },
    MARK_END(state, {
        currentAuditIndex}) {
        state.audits[currentAuditIndex].etime = Math.round((+new Date()) / 1000);
    }
};

const actions = {
    ...make.actions(state),
};

export default {
    namespaced: true,
    state,
    mutations,
    actions
};