import Vue from "vue";
import VueRouter from "vue-router";

import store from "./stores";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "login",
    component: () => import("./pages/Login.vue"),
  },
  {
    path: "/activate/:token?",
    name: "activate",
    props: true,
    component: () => import("./pages/Activate.vue"),
  },
  {
    path: "/reset/:token?",
    name: "reset",
    props: true,
    component: () => import("./pages/Reset.vue"),
  },
  {
    path: "/home",
    name: "home",
    component: () => import("./pages/home/Home.vue"),
  },
  {
    path: "/mytemplates",
    name: "mytemplates",
    component: () => import("./pages/myAudits/index.vue"),
  },
  {
    path: "/mytemplates/:uuid",
    name: "myaudit-details",
    component: () => import("./pages/myAudits/myAuditSections.vue"),
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("./pages/report/Dashboard.vue"),
  },
  {
    path: "/premises",
    name: "premises",
    component: () => import("./pages/premises/index.vue"),
  },
  {
    path: "/help",
    name: "help",
    component: () => import("./pages/Help.vue"),
  },
  // {
  //   path: "/premises",
  //   name: "premises",
  //   component: () => import("./pages/Locations.vue"),
  // },
  {
    path: "/users",
    name: "users",
    component: () => import("./pages/users/index.vue"),
  },
  { 
    path: "/users/:uuid",
    name: "user-details",
    props: true,
    component: () => import("./pages/users/Details.vue")
  },
  {
    path: "/roles",
    name: "roles",
    component: () => import("./pages/roles/index.vue"),
  },
  {
    path: "/reports",
    name: "reports",
    component: () => import("./pages/report/Reports.vue"),
  },
  {
    path: "/users/new",
    name: "create-user",
    component: () => import("./pages/users/Create.vue"),
  },
  {
    path: "/users/update",
    name: "update-user",
    component: () => import("./pages/users/Update.vue"),
  },
  {
    path: "/audit",
    name: "audit",
    props: true,
    component: () => import("./pages/audit/AuditSections.vue"),
  },
  {
    path: "/audit_sub/:abi",
    name: "audit_sub",
    props(route) {
      const p = {
        ...route.params,
      };
      p.abi = +p.abi;
      return p;
    },
    component: () => import("./pages/audit/AuditSections.vue"),
  },
  {
    path: "/audit/signature",
    name: "signature",
    props: true,
    component: () => import("./pages/audit/AuditSignature.vue"),
  },
  {
    path: "/audit/hint",
    name: "hint",
    props: true,
    component: () => import("./pages/audit/AuditHint.vue"),
  },
  {
    path: "/audit/:abi",
    name: "section",
    props(route) {
      const p = {
        ...route.params,
      };
      p.abi = +p.abi;
      return p;
    },
    component: () => import("./pages/audit/AuditQuestions.vue"),
  },
  {
    path: "/results",
    name: "results",
    props: true,
    component: () => import("./pages/audit/AuditGraph.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  const t = store.get("app/session");

  if (to.name !== "login" && to.name !== "help") {
    if (t === "invalid" || t == null) {
      console.log("User has no previous token - directing to login");
      return next({
        name: "login",
      });
    }
  }

  return next();
});

export default router;
