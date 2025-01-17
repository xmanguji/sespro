<template>
  <AppLayout :back="true" @back="onBack">
    <div class="content-header">
      <div class="title ">
          <img class="logo" src="../../assets/images/icons/icon_legal.png" />
          <label>{{ legalDisclaimer }}</label>
      </div>
    </div>
    <div class="paragraph">
      <br />
      <p>{{ disclaimerFirstParagraph }}</p>
      <br />
      <p>{{ disclaimerSecondParagraph }}</p>
    </div>
  </AppLayout>
</template>


<script>
import router from "../../routes";
import AppLayout from "../../layouts/AppLayout";

export default {
  name: "Legal",
  components: { AppLayout },
  data() {
    return {
      legalDisclaimer: "Legal Disclaimer",
      disclaimerFirstParagraph:
        "This app is solely for the use of conducting a food safety and hygiene inspection. Such inspections are based on a sampling exercise, considering the facilities, operations, practices, records and systems viewed at the food business site during the time of the inspection. Given that it is a sampling exercise it naturally follows that not every case of poor condition, bad practice, bad record keeping, or procedural non-conformance will necessarily have been identified and picked up as part of any single particular inspection. This is because, on a day to day basis, food facility staff present, operations conducted, habits practiced, equipment used and even premises used can change. Skill in identifying areas of poor condition or procedural nonconformity is also wholly dependent on the training and experience of the operator of the app in the field of food safety and hygiene inspection. It therefore does not follow that no nonconformances exist where none have been picked up by the use of this app. The use of the Hygiene Check app is provided without liability in its application. The maintenance of conditions, practices and records to support good food safety management remains solely the responsibility of the food business.",
      disclaimerSecondParagraph:
        "The content of the app, or the way in which the app is used, does not supersede any legal obligations relating to food safety or food information provision law pertaining at the time, or current specific national food safety guidance or legislation that may be released from time to time, within the geographical location in which it is used. The app should be considered as non statutory guidance and a means of working towards food safety management best practice. It does not guarantee that no person visiting your establishment will suffer food poisoning, food borne disease, or other injury or illness from food you have prepared and served, for the reasons outlined above.",
    };
  },
  methods: {
    onBack() {
      router.push({ name: "home" });
    },
  },
};
</script>

<style lang="scss" scoped>
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
