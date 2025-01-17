<template>
  <AppLayout :back="true" @back="onBack">
    <div class="content-header">
      <div class="title ">
        <img class="logo" src="../../assets/images/icons/icon_howto.png" />
        <label>{{ tutorial }}</label>
      </div>
    </div>
    <div class="paragraph">
      <br />
      <p>{{ firstTutorialParagraph }}</p>
      <br />
      <p>{{ secondTutorialParagraph }}</p>
      <br />
      <p>{{ thirdTutorialParagraph }}</p>
      <br />
      <p>{{ fourthTutorialParagraph }}</p>
      <br />
      <p>{{ fifthTutorialParagraph }}</p>
      <br />
      <p>{{ sixthTutorialParagraph }}</p>
    </div>
    <div class="contact-btn-div">
      <div @click="onContact">
        <div>
          <img class="logo" src="../../assets/images/icons/icon_contact.png" />
          <label>Contact Us</label>
        </div>
        <span class="icon">
          <i class="fas fa-angle-right"></i>
        </span>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from "../../layouts/AppLayout";
import router from "../../routes";

export default {
  name: "Tutorial",
  components: { AppLayout },
  data() {
    return {
      tutorial: "HygieneCheck How To Use",
      firstTutorialParagraph:
        'This audit tool app is designed with two purposes in mind, both with the ultimate aim of helping you to achieve and maintain a Food Hygiene Rating of 5:',
      secondTutorialParagraph:
        "Firstly, it is a collection of all current UK based food safety and hygiene regulations, and best practice guidance for the workplace. We recommend that you go through and study each audit question first to understand the control required to be implemented. In all cases you will be able to click on the “i” mark and access further hints and tips to help you understand the control. In many cases the hints and tips section contains useful photographs of hygiene controls that have gone wrong, or are inadequate, to give you an idea of what to avoid! The UK regulations and guidance are comprehensive and will likely be equally applicable in other areas of the world, but we recommend that you consult any specific national guidance that may apply to you.",
      thirdTutorialParagraph:
        "Secondly, once your controls are set up, you can perform regular and spot check audits of your workplace to determine that your controls are fully implemented, understood and effective. This app will provide a simple percentage compliance score, audit reports and simple statistical analysis of where you might be going wrong. It's important that you fix any weaker areas, using the corrective action tables that come with your e-mailed audit report, so that when you next audit, you will get a higher score, which in turn will demonstrate that you are taking your workplace controls very seriously.",
      fourthTutorialParagraph:
        "We will be busy in the background keeping up to date with the changes in food safety and hygiene regulation and / or guidance, taking our lead from the UK government and supporting resources from the Food Standards Agency. From time to time the app will therefore be updated and as long as you have auto update set up then you will automatically receive this updated information.",
      fifthTutorialParagraph:
        "Have fun with our app and above all we hope you and your workplace stay hygienic and food safe!",
      sixthTutorialParagraph:
        "Contact us with any feedback - we'd love to hear from you with suggestions and comments!"
    };
  },
  methods: {
    onBack() {
      router.push({ name: "home" });
    },
    onContact() {
      router.push({ name: "contact" });
    },
  },
};
</script>

<style lang="scss" scoped>
.contact-btn-div {
  padding: 1rem;
  > .button {
    > span {
      border: 10px solid red !important;
    }
  }
}
.headings {
  width: 100%;
  text-align: center;
  font-weight: 600;
  font-size: 20px;
  margin-top: 4px;
}

.paragraph {
  width: 100%;
  text-align: left;
  margin: 2px;
}

@media (max-width: 850px) {
  .paragraph {
    font-size: 14px;
  }
}
</style>

<style lang="scss" >
.contact-btn-div {
  padding: 1rem;
  > div {
    background-color: white;
    margin: 0 -2rem;
    display: flex;
    justify-content: space-between;
    padding: 1rem;
    align-items: center;
    > div {
      align-items: center;
      display: flex;
      label {
        margin-left: 1rem;
      }
    }
  }
}
</style>