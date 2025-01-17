<template>
    <div class="login-page">
        <div class="login-container">
            <div class="logo-container">
                <img src="../assets/logins.png" />
            </div>
            <div class="login-text">
                <span>Activate Account</span>
            </div>
            <div class="button-container">
                <b-input :disabled="true" v-bind:value="$props.token"></b-input>
            </div>
            <div class="button-container">
                <b-button @click="activate" type="is-success">Activate</b-button>
            </div>
            <b-loading :is-full-page="true" :active="loading" :can-cancel="false"></b-loading>
        </div>
    </div>
</template>

<script>
    import API from "../services/API";

    export default {
        props: {
            token: {
                type: String
            }
        },
        data() {
            return {
                loading: false,
            }
        },
        methods: {
            activate() {
                const that = this;
                if (this.token !== '' && this.token != null) {
                    API.activate(this.token)
                        .then((r) => {
                            if (r) {
                                this.loading = false;
                                this.$buefy.dialog.alert({
                                    message: "Account activated! You can now login on your respective device.",
                                    type: "is-success",
                                    hasIcon: true
                                });
                            }
                        })
                        .catch(e => {
                            this.loading = false;
                            console.log(e);
                            that.$buefy.dialog.alert("Error activating account.");
                        });
                    this.loading = true;
                }
            }
        },
    }
</script>

<style lang="scss" scoped>
    .login-page {
        width: 100%;
        height: 100%;
        padding: 0;
        background-color: #ffffff;
        user-select: none;
    }
    .login-container {
        overflow-y: auto;
        height: 100%;
        width: 50%;
        margin: auto;
    }
    .logo-container {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-top: 8%;
    }

    .login-text {
        text-align: center;
        font-size: 28px;
        font-weight: 500;
        cursor: pointer;
    }

    .button-container {
        align-content: center;
        margin-bottom: 20px;
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
            width: 80%;
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
