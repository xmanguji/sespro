import Buefy from "buefy";
import "./assets/css/bulma.scss"
import "./assets/css/global.scss"

import VueSimpleMarkdown from "vue-simple-markdown";

import Vue from "vue";
import App from "./App.vue";
import VueRouter from "vue-router";
import VueSignaturePad from "vue-signature-pad";

import router from "./routes";
import store from "./stores";
import './registerServiceWorker'
import './assets/css/tailwind.css'

Vue.config.productionTip = false;

Vue.use(Buefy, {
    defaultIconPack: 'fas',
    defaultContainerElement: '#content',
    // ...
});

Vue.use(VueRouter);

Vue.use(VueSimpleMarkdown);
Vue.use(VueSignaturePad);

new Vue({
    render: h => h(App),
    router: router,
    store: store
}).$mount('#app');
