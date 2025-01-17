<template>
  <div class="login-page border max-w-screen-sm inline-flex justify-center">
    <div class="login-container flex flex-col">
      <div class="text-3xl text-black text-left font-black mt-8">
        {{ 'Welcome' }}
      </div>
      <div class="logo-container">
        <img
          src="@/assets/images/Respro_logo.png"
          class="w-32 md:w-40 lg:w-56 bg-contain"
        />
        <!-- <img
          src="@/assets/images/Respro_logo.png"
          class="w-32 md:w-40 lg:w-56 bg-contain"
          @mousedown="startLongClick"
        /> -->
      </div>
      <!-- <div v-if="this.atype === 'Google'" class="button-container">
        <GoogleLogin
          class="google-login-btn"
          :params="gparams"
          :renderParams="gRenderParams"
          :onSuccess="fullLogin"
        ></GoogleLogin>
      </div> -->
      
      <div class="button-container">
        <b-field class="my-1">
          <b-input
            v-model="i_email"
            type="email"
            placeholder="Email"
            class="hover:border-PrimaryLight border-0 border-red-900"
            @keyup.native.enter="onKeyEnter('email', $event)"
          ></b-input>
        </b-field>
        <b-field class="my-1">
          <b-input
            v-model="i_password"
            type="password"
            placeholder="Password"
            @keyup.native.enter="onKeyEnter('password', $event)"
            style="border-width: 0;"
          ></b-input>
        </b-field>
        </div>

        <div class="button-groups mt-4">
          <b-field>
            <button
              @click="regularLogin"
              class="
                bg-black
                text-xl text-white
                h-10
                rounded
                w-56
              "
            >
              Sign in
            </button>
          </b-field>
          </div>
          <div class="button-groups mt-4">

          <button
            @click="help"
            class="
              focus:text-PrimaryDark
              w-56
              font-medium
              text-Primary text-base
              hover:text-PrimaryDark
              outline-none
              bg-white
              border-none
              mb-12
            "
          >
            Don't have an account?
          </button>
          <div class="text-xs">v1.3</div>
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
      longClickTimer: null,
      longClickActive: localStorage.getItem('dev'),
      longClickDuration: 2000, // Set the duration for long click in milliseconds
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
    premises: sync("app/premises"),
    auditIndex: sync("audit/auditIndex"),
    audits: sync("audit/audits"),
    templates: sync("template/templates"),
    selectedTemplateIndex: sync("template/selectedTemplateIndex"),
  },
  methods: {
    load() {
      //this.$store.dispatch("app/loadToken");
    },
    help() {
      this.$router.push({ name: "help" });
    },
    fullLogin: function (googleUser) {
      let profile = googleUser.getBasicProfile();
      let id_token = googleUser.getAuthResponse().id_token;
      const loadingComponent = this.$buefy.loading.open({ container: null });
      API.login(profile.getEmail(), id_token, true)
        .then((response) => {
          let data = response.data;
          this.token = data.token;

          Promise.all([API.getPremises(data.token), API.getAudits(data.token)])
            .then((responses) => {
              let premises = responses[0].data["premises"];
              this.premises = premises;
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

          Promise.all([API.getPremises(data.token), API.getAudits(data.token)])
            .then((responses) => {
              let premises = responses[0].data["premises"];
              this.premises = premises;
              API.APILog(`Found ${premises.length} location(s)`);
              let templates = responses[1].data["audits"];
              if (templates.length > -1) this.selectedTemplateIndex = 0;
              else {
                loadingComponent.close();
                this.$buefy.dialog.alert("Error fetching account information.");
              }

              this.templates = templates;

              let arr = [];
              this.premises.forEach((item, index) => {
                arr.push({
                  auditIndex: index,
                  premiseUuid: item.uuid,
                  location: null,
                  name: templates[this.selectedTemplateIndex].name,
                  type: templates[this.selectedTemplateIndex].uuid,
                  body: [],
                  stime: null,
                  etime: null,
                });
              });
              this.audits = arr;
              let templateId = templates[this.selectedTemplateIndex].uuid
              this.template = templateId;
              API.APILog(`Set audit template [${templateId}]`);
              loadingComponent.close();
              this.$router.push({ name: "home" });
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
    startLongClick() {
      this.longClickTimer = setTimeout(() => {
        this.longClickActive = !this.longClickActive;
        localStorage.setItem('dev', !this.longClickActive);
        setTimeout(() => {
          window.close();
        }, 1000);
      }, this.longClickDuration);
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
  height: 100%;
  display: flex;
  justify-content: space-around;
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

.google-login-btn > div {
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
