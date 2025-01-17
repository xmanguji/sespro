<template>
  <div class="main-container w-full h-full">
    <div class="login-page max-w-screen-sm inline-flex justify-center">
      <div class="login-container flex flex-col justify-center">
        <div class="
            logo-container
            flex flex-row flex-1
            justify-end
            items-end
            mb-10
          ">
          <img src="@/assets/images/respro-logo.svg" class="w-64 bg-contain" />
        </div>
        <div v-if="this.atype === 'Google'" class="button-container flex-1">
          <GoogleLogin class="google-login-btn" :params="gparams" :renderParams="gRenderParams" :onSuccess="fullLogin">
          </GoogleLogin>
        </div>
        <div v-else class="button-container flex-1">
          <input v-model="i_email" type="email" placeholder="Email" class="w-full p-2 rounded border my-2" />
          <input v-model="i_password" class="w-full border p-2 rounded my-2" type="password" placeholder="Password" />
          <div class="flex flex-col items-center justify-center mt-2">
            <button @click="regularLogin" class="
                bg-editIconColor
                flex
                text-xl text-white
                hover:text-onyx
                rounded
                px-3 py-1 mb-2
              ">
              Sign In
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { GoogleLogin } from "vue-google-login";
import settings from "../network/settings";
import API from "../services/API";
import { sync } from "vuex-pathify";

export default {
  name: "Login",
  components: { GoogleLogin },
  data() {
    return {
      gparams: {
        client_id: settings.GOOGLE_CLIENT_ID,
      },
      gRenderParams: {
        width: 537,
        height: 50,
        longtitle: true,
        theme: "dark",
      },
      loading: false,
      atype: settings.ACCOUNT_TYPE,

      i_email: null,
      i_password: null,
    };
  },
  computed: {
    token: sync("app/session"),
    activeUserRole: sync("app/activeUserRole"),
    activeTemplates: sync("app/activeTemplates"),
    activeOrganization: sync("app/activeOrganization"),
    activeUserUUID: sync("app/activeUserUUID"),
    premises: sync("app/premises"),
    templates: sync("templates/templates"),
    auditIndex: sync("audit/auditIndex"),
    audits: sync("audit/audits"),
    groups: sync("premises/groups"),
  },
  methods: {
    load() {
      //this.$store.dispatch("app/loadToken");
    },
    help() {
      this.$router.push({ name: "help" });
    },
    mapGroups(results) {
      this.groups = results.map(({ uuid, name, organization, organization_uuid, render_enabled, manager_name, manager_uuid }) => ({
        uuid,
        name,
        render_enabled,
        organization: {
          uuid: organization_uuid,
          name: organization
        },
        manager: {
          name: manager_name,
          uuid: manager_uuid
        }
      }));
    },
    fullLogin: function (googleUser) {
      let profile = googleUser.getBasicProfile();
      let id_token = googleUser.getAuthResponse().id_token;
      const loadingComponent = this.$buefy.loading.open({ container: null });
      API.login(profile.getEmail(), id_token, true)
        .then((response) => {
          let data = response.data;
          this.token = data.token;

          API.getPremises(data.token)
            .then((responses) => {
              let premises = responses[0].data["premises"];
              // this.premises = premises;
              API.APILog(`Found ${premises.length} location(s)`);
              console.log(responses);
              let templates = responses[1].data["audits"];
              if (templates.length < 2) {
                let templateId = templates[0]["uuid"];
                this.template = templateId;
                API.APILog(`Set audit template [${templateId}]`);
                loadingComponent.close();
                this.$router.push({ name: "home" });
              } else {
                // Should be unreachable as we are only using a singular audit template as of now
                loadingComponent.close();
                this.$buefy.dialog.alert("Error 9001 - contact developer.");
              }
            })
            .catch((error) => {
              API.APILog(error);
              loadingComponent.close();
              this.$buefy.dialog.alert("Error fetching account information.");
            });
        })
        .catch((error) => {
          loadingComponent.close();
          API.APILog(error);
          this.$buefy.dialog.alert("Error authenticating with Google.");
        });
    },
    regularLogin() {
      // this.loading = true;
      const loadingComponent = this.$buefy.loading.open({ container: null });
      API.login(this.i_email, this.i_password)
        .then((response) => {
          let data = response.data;
          this.token = data.token;
          this.activeUserRole = data.userRole;
          this.activeOrganization = data.organizations[0];
          this.activeTemplates = data.templates;
          this.activeUserUUID = data.userId;
          console.log(data)
          Promise.all([
            API.fetch_templates(this.token),
            API.getPremises(this.token),
            API.fetch_groups_sort(this.token, 'asc'),
          ]).then((responses) => {
            let premises = responses[1].data["premises"];
            let templates = responses[0].data["templates"]
            this.mapGroups(responses[2].data["groups"])

            this.premises = premises;
            this.templates = templates;
            loadingComponent.close();
            this.$router.push({ name: "dashboard" });
          })
            .catch((error) => {
              API.APILog(error);
            });

        })
        .catch((error) => {
          loadingComponent.close();
          API.APILog(error);
          this.$buefy.dialog.alert(
            "Error authenticating. Please ensure you are connected to the internet."
          );
        });
    },
    onKeyEnter(field, event) {
      const divs = Array.from(
        event.target.ownerDocument.querySelectorAll(
          ".button-container div.field"
        )
      );
      if (field == "email") {
        divs[1].querySelector('[type="password"]').focus();
      } else if (field == "password") {
        divs[2].querySelector("button").focus();
      }
    },
  },

};
</script>

<style lang="scss" scoped>
.login-page {
  width: 100%;
  height: 100%;
  padding: 0;
  user-select: none;
}

.login-container {
  overflow-y: auto;
  height: 100%;
  width: 50%;
  margin: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.login-text {
  text-align: center;
  font-size: 28px;
  font-weight: 500;
  cursor: pointer;
}

.button-container {
  align-content: center;
}

.button-container div.field {
  margin: 1rem auto;
}

.google-login-btn {
  height: 50px;
  display: flex !important;
  color: #ffffff;
  font-size: 24px;
  font-weight: 600;
  text-align: center;
  align-content: center;
}

.google-login-btn>div {
  margin: 0 auto;
}

.google {
  background-color: #ffffff;
  border-radius: 4px;
  height: 60px;
  width: 60px !important;
  position: absolute;
  left: 4px;
  top: 4px;
}

@media (max-width: 850px) {
  .login-container {
    width: 90%;
  }

  .logo-container {
    margin-top: 15%;
  }

  .login-text {
    font-size: 24px;
    font-weight: 500;
  }

  .google-login-btn {
    height: 50px;
    margin-top: 20%;
    font-size: 22px;
    align-content: center;
  }
}

@media (max-width: 600px) {
  .google-login-btn {
    height: 50px;
    margin-top: 25%;
    font-size: 20px;
  }

  .login-text {
    margin-top: 5%;
  }
}
</style>
