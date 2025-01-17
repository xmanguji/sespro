import {make} from "vuex-pathify";

const state = {
    premises: [],
    groups: [],
    organizations: []
}

const mutations = {
    ...make.mutations(state),
}

const actions = {
    ...make.actions(state),
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}
