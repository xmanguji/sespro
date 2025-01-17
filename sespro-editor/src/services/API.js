import network from "../network";
import settings from "../network/settings";

const routes = {
  login: "/auth/login/admin",
  logout: "/auth/logout",
  activate: "/auth/activate",
  reset: "/auth/reset",

  checkToken: "/user/session",
  availableAudits: "/edit/audits",
  audit: "/edit/audit",
  premises: "/user/premises",
  render: "/edit/render/",
  sections: '/categories',

  progress: "/audit/progress",

  submitAudit: "/edit/audit",
  submitImage: "/audit/image",
  submitEditImage: "/edit/image",
  deleteParsedAudit: "/edit/audit/",
  question: '/questions',
  category: '/categories',
  template: '/templates',

  log: "/user/clientlog",

  BASE_PREMISES: "/premises",
  GROUPS: "/premises/groups",
  ORGANIZATIONS: "/premises/organizations",
  USERS: "/user/users",
  USERAUDITS: "/user/audits",
  MANAGERS: "/user/managers",
  USER: "/user",
  TEMPLATES: "/templates",
  ROLES: "/roles",
  REPORTS: "/reports",

};

const makeAuthConf = function (token) {
  return {
    headers: {
      Authorization: "Bearer " + token,
    },
  };
};

const APILog = (message) => console.log("[API] " + message);
const APINetLog = (message) => APILog("[NETCHK] " + message);

// Checks response status and fetches error messages
const APINetCheck = function (r) {
  return new Promise(function (resolve, reject) {
    r.status >= 500
      ? reject(new Error("Server Error")) || APINetLog("Server error...")
      : r.status >= 400
        ? reject(new Error(r.data.message)) || APINetLog("API error...")
        : r.status >= 200
          ? resolve(r) || APINetLog("OK...")
          : reject(new Error("Unknown Error (?)")) || APINetLog("Unknown error...");
  });
};

APILog("Service loaded - base URL: " + settings.API_URL);

export default {
  makeAuthConf,
  APILog,
  login: function (username, password) {
    const params = new URLSearchParams();
    params.append("username", username);
    params.append("password", password);

    return network.post(routes.login, params, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
  },
  // login: function(username, password) {
  //   APILog("Attempting login as [" + username + "]...");
  //   return network
  //     .post(routes.login, { username, password })
  //     .then(APINetCheck);
  // },
  checkToken: function (token) {
    APILog("Validating previous session token...");
    return network
      .get(routes.checkToken, makeAuthConf(token))
      .then(APINetCheck);
  },
  logout: function (token) {
    APILog("Attempting logout...");
    return network.get(routes.logout, makeAuthConf(token)).then(APINetCheck);
  },
  getPremises: function (token) {
    APILog("Fetching user premises...");
    return network.get(routes.premises, makeAuthConf(token)).then(APINetCheck);
  },
  getAudits: function (token, currentPage, perPage, sortBy, sortDirection) {
    APILog("Fetching available audit templates...");
    return network
      .get(`${routes.availableAudits}?currentPage=${currentPage}&perPage=${perPage}&sortBy=${sortBy}&sortDirection=${sortDirection}`, makeAuthConf(token))
      .then(APINetCheck);
  },
  getAudit: function (token, templateId) {
    APILog(`Fetching audit template [${templateId}]...`);
    return network
      .get(routes.audit + "/" + templateId, makeAuthConf(token))
      .then(APINetCheck);
  },
  getSections: function (token, templateId) {
    APILog(`Fetching audit template [${templateId}]...`);
    return network
      .get(`${routes.sections}/${templateId}`, makeAuthConf(token))
      .then(APINetCheck);
  },
  renderReport: function (token, auditUuid) {
    APILog(`Render audit report with audit uuid [${auditUuid}]...`);
    return network
      .get(routes.render + auditUuid, makeAuthConf(token))
      .then(APINetCheck);
  },
  submitAudit: function (token, auditUuid, auditBody) {
    APILog(
      `Submitting audit "${auditBody.name}" for [${auditBody.location}]...`
    );
    return network
      .post(
        `${routes.submitAudit}/${auditUuid}`,
        auditBody,
        makeAuthConf(token)
      )
      .then(APINetCheck);
  },
  submitImage: function (token, parsed_audit, location, question, image) {
    APILog(`Submitting audit image...`);
    let conf = makeAuthConf(token);

    return network
      .post(
        `${routes.submitEditImage}/${parsed_audit}/${location}/${question}`,
        { data: image },
        conf
      )
      .then(APINetCheck);
  },
  activate: function (token) {
    APILog("Activating account...");
    return network.get(`${routes.activate}/${token}`).then(APINetCheck);
  },
  reset: function (token, password, confirm) {
    APILog("Resetting password...");
    return network
      .post(routes.reset, { token, password, confirm })
      .then(APINetCheck);
  },
  log: function (token, data) {
    APILog("Logging a state...");
    console.log(data);
    return network
      .post(routes.log, data, makeAuthConf(token))
      .then(APINetCheck);
  },
  deleteParsedAudit: function (token, parsedUuid) {
    APILog("Deleting parsed audit");
    return network.delete(`${routes.deleteParsedAudit}${parsedUuid}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_premises: function (token) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.BASE_PREMISES, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_premises_sort: function (token, sort) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.BASE_PREMISES + "/" + sort, makeAuthConf(token))
      .then(APINetCheck);
  },

  create_premises: function (token, data) {
    APILog("Fetching all available locations...");
    return network
      .post(routes.BASE_PREMISES, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  delete_premises: function (token, uuid) {
    APILog("Deleting parsed audit");
    return network.delete(`${routes.BASE_PREMISES}/${uuid}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  update_premises(token, uuid, data) {
    APILog("Deleting parsed audit");
    return network.put(`${routes.BASE_PREMISES}/${uuid}`, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  create_premises_group: function (token, data) {
    APILog("Fetching all available locations...");
    return network
      .post(routes.GROUPS, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  delete_premises_group: function (token, uuid) {
    APILog("Deleting parsed audit");
    return network.delete(`${routes.GROUPS}/${uuid}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  update_premises_group(token, uuid, data) {
    APILog("Deleting parsed audit");
    return network.put(`${routes.GROUPS}/${uuid}`, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  create_premises_organization: function (token, data) {
    APILog("Fetching all available locations...");
    return network
      .post(routes.ORGANIZATIONS, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  delete_premises_organization: function (token, uuid) {
    APILog("Deleting parsed audit");
    return network.delete(`${routes.ORGANIZATIONS}/${uuid}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  update_premises_organization(token, uuid, data) {
    APILog("Deleting parsed audit");
    return network.put(`${routes.ORGANIZATIONS}/${uuid}`, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_groups: function (token) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.GROUPS, makeAuthConf(token))
      .then(APINetCheck);
  },


  fetch_groups_sort: function (token, sort) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.GROUPS + "/" + sort, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_organizations: function (token) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.ORGANIZATIONS, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_organizations_sort: function (token, sort) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.ORGANIZATIONS + "/" + sort, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_users: function (token) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.USERS, makeAuthConf(token))
      .then(APINetCheck);
  },


  fetch_managers: function (token) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.MANAGERS, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_users_sort: function(token, organization, currentPage, perPage, sortBy, sortDirection) {
    APILog("Fetching all available locations...");
    return network
      .get(`${routes.USERS}?currentPage=${currentPage}&perPage=${perPage}&sortBy=${sortBy}&sortDirection=${sortDirection}&organization=${organization}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_templates: function (token) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.TEMPLATES, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_audits: function (token) {
    APILog("Fetching all available audits...");
    return network
      .get(routes.USERAUDITS, makeAuthConf(token))
      .then(APINetCheck);
  },

  create_user: function (token, data) {
    APILog("Fetching all available locations...");
    return network
      .post(routes.USER, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  create_question: function (token, data) {
    APILog("Fetching all available questions...");
    return network
      .post(routes.question, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  update_question: function (token, uuid, data) {
    APILog("Updating a question");
    return network
      .put(`${routes.question}/${uuid} `, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  delete_question: function(token, uuid) {
    APILog("Deleting a question");
    return network.delete(`${routes.question}/${uuid}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  create_category: function (token, uuid, data) {
    APILog("Creating a category");
    return network
      .post(`${routes.category}/${uuid}`, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  update_category: function (token, uuid, data) {
    APILog("Updating a category");
    return network
      .put(`${routes.category}/${uuid} `, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  delete_category: function(token, uuid) {
    APILog("Deleting a category");
    return network.delete(`${routes.category}/${uuid}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  create_template: function (token, data) {
    APILog("Creating a template");
    return network
      .post(routes.template, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  update_template: function (token, uuid, data) {
    APILog("Updating a template");
    return network
      .put(`${routes.template}/${uuid} `, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  delete_template: function(token, uuid) {
    APILog("Deleting a template");
    return network.delete(`${routes.template}/${uuid}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  update_user: function (uuid, token, data) {
    APILog("Fetching all available locations...");
    return network
      .post(`${routes.USER}/${uuid} `, data, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_roles: function (token) {
    APILog("Fetching all available locations...");
    return network
      .get(routes.ROLES, makeAuthConf(token))
      .then(APINetCheck);
  },

  delete_user: function(token, uuid) {
    APILog("Deleting a user");
    return network.delete(`${routes.USER}/${uuid}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_user_details(token, uuid) {

    APILog("Fetching a user details with uuid " + uuid)

    return network.get(`${routes.USER}/details/${uuid}`, makeAuthConf(token))
      .then(APINetCheck);

  },

  fetch_generic_report_data(token, params) {
    APILog("Fetching a generic reports data")

    return network.get(`${routes.DASHBOARD_MONTHLY}ic?${params}`, makeAuthConf(token))
      .then(APINetCheck);

  },
  fetch_dashboard_location_monthly_data(token, params) {
    APILog("Fetching a location monthly data in dashboard")

    return network.get(`${routes.REPORTS}/dashboard/location_monthly_scores?${params}`, makeAuthConf(token))
      .then(APINetCheck);

  },
  fetch_dashboard_number_of_audits_submitted(token, params) {
    APILog("Fetching a total audits data")

    return network.get(`${routes.REPORTS}/dashboard/totalaudits?${params}`, makeAuthConf(token))
      .then(APINetCheck);
  },

  fetch_dashboard_average_score(token, params) {
    APILog("Fetching a average score data")

    return network.get(`${routes.REPORTS}/dashboard/averagescore?${params}`, makeAuthConf(token))
      .then(APINetCheck);
  },
  fetch_dashboard_location_performance(token, params) {
    APILog("Fetching a location performance data")

    return network.get(`${routes.REPORTS}/dashboard/location_performance?${params}`, makeAuthConf(token))
      .then(APINetCheck);
  },
  fetch_dashboard_section_performance_aggregated(token, params) {
    APILog("Fetching a section performance aggregated data")

    return network.get(`${routes.REPORTS}/dashboard/section_performance_aggregated?${params}`, makeAuthConf(token))
      .then(APINetCheck);
  },
  fetch_dashboard_question_performance_aggregated(token, params) {
    APILog("Fetching a question performance aggregated data")

    return network.get(`${routes.REPORTS}/dashboard/question_performance_aggregated?${params}`, makeAuthConf(token))
      .then(APINetCheck);
  },
  generate_pdf_and_send(token, uuid) {
    APILog("Fetching a generic reports data")

    return network.get(`${routes.render}${uuid}`, makeAuthConf(token))
      .then(APINetCheck);
  }

};
