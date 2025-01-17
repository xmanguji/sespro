import network from "../network";
import settings from "../network/settings";

const routes = {
    login: "/auth/login",
    logout: "/auth/logout",
    activate: "/auth/activate",
    reset: "/auth/reset",

    checkToken: "/user/session",
    availableAudits: "/user/audits",
    template: "/user/audit",
    premises: "/user/premises",

    progress: "/audit/progress",

    submitAudit: "/audit/submit",
    submitImage: "/audit/image",

    log: "/user/clientlog"
}

const makeAuthConf = function (token) {
    return {
        headers: {
            Authorization: "Bearer " + token
        }
    }
}

const APILog = message => console.log("[API] " + message);
const APINetLog = message => APILog("[NETCHK] " + message);

// Checks response status and fetches error messages
const APINetCheck = function (r) {
    return new Promise(function (resolve, reject) {
        r.status >= 500 ? reject(new Error("Server Error")) || APINetLog("Server error...")
            : r.status >= 400 ? reject(new Error(r.data.message)) || APINetLog("API error...")
            : r.status >= 200 ? resolve(r) || APINetLog("OK...")
                : reject(new Error("Unknown Error (?)")) || APINetLog("Unknown error...")
    });
};

// APILog("Service loaded - base URL: " + settings.API_URL);

export default {
    APILog,
    login: function(username, password) {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);
  
      return network.post(routes.login, params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",        
        },
      });
    },
    checkToken: function(token) {
        APILog("Validating previous session token...");
        return network.get(routes.checkToken, makeAuthConf(token)).then(APINetCheck);
    },
    logout: function (token) {
        APILog("Attempting logout...");
        return network.get(routes.logout, makeAuthConf(token)).then(APINetCheck);
    },
    getPremises: function (token) {
        APILog("Fetching user premises...");
        return network.get(routes.premises, makeAuthConf(token)).then(APINetCheck);
    },
    getAudits: function (token) {
        APILog("Fetching available audit templates...");
        return network.get(routes.availableAudits, makeAuthConf(token)).then(APINetCheck);
    },
    getTemplate: function (token, templateId) {
        APILog(`Fetching audit template [${templateId}]...`);
        return network.get(routes.template + "/" + templateId, makeAuthConf(token)).then(APINetCheck);
    },
    submitAudit: function (token, auditBody) {
        APILog(`Submitting audit "${auditBody.name}" for [${auditBody.location}]...`);
        return network.post(routes.submitAudit, auditBody, makeAuthConf(token)).then(APINetCheck);
    },
    submitImage: function (token, location, question, image) {
        APILog(`Submitting audit image...`);
        let conf = makeAuthConf(token);

        return network.post(`${routes.submitImage}/${location}/${question}`, {data: image}, conf).then(APINetCheck);
    },
    activate: function (token) {
        APILog("Activating account...");
        return network.get(`${routes.activate}/${token}`).then(APINetCheck);
    },
    reset: function (token, password, confirm) {
        APILog("Resetting password...");
        return network.post(routes.reset, {token, password, confirm}).then(APINetCheck);
    },
    log: function (token, data) {
        APILog("Logging a state...");
        console.log(data)
        return network.post(routes.log, data, makeAuthConf(token)).then(APINetCheck);
    }
}