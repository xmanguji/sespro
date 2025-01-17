import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import pathify from "./pathify";

import app from "./appStore";
import audit from "./auditStore";
import premises from "./premises";
import templates from "./templates";
import users from "./users";
import roles from "./roles";

Vue.use(Vuex);

const persist = createPersistedState({
    key: "mqm",
});

const store = new Vuex.Store({
    modules: {
        app: app,
        audit: audit,
        premises: premises,
        templates: templates,
        users: users,
        roles: roles
    },
    plugins: [pathify.plugin, persist]
});

export default store;
