import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
import pathify from "./pathify";

import app from "./appStore";
import audit from "./auditStore";
import template from "./templateStore"

Vue.use(Vuex);

const persist = createPersistedState({
    key: "mqm",
});

const store = new Vuex.Store({
    modules: {
        app: app,
        audit: audit,
        template: template
    },
    plugins: [pathify.plugin, persist]
});

export default store;
