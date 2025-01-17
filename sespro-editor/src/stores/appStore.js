import {make} from "vuex-pathify";

const state = {
    session: "invalid",
    activeUserRole: "ROOT",
    activeOrganization: null,
    activeTemplates: [],
    activeUserUUID: '',
    premises: [],
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
