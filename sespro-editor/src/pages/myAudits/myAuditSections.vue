<template>
  <AppLayout 
    :back="true" 
    :userRole="activeUserRole" 
    :imageLogo="defaultImage" 
    headerTitle="Back to Templates" 
    :isButtonAllowed="true"
    @click-event="updateCategory(category.uuid)"
  >
    <div class="
        px-4
        w-full
        flex flex-row
        justify-center
        gap-x-12
        bg-white
        text-PrimaryText
      ">
      <div class="w-full pt-6">
        <div class="premise-list rounded-md">
          <div class="text-onyx">
            <div class="w-full flex justify-start">
              <div v-if="!indexCreateCategoryAllowed && isEditable" class="button is-small ml-1" @click="onAllowCreateCategory(1)">
                <b-icon icon="plus" class="text-xs"></b-icon>
                &nbsp;&nbsp;Create New Section
              </div>
              <textarea v-if="indexCreateCategoryAllowed" id="question" v-model="category.text" type="text"
                placeholder="Enter Category Text" class="border rounded-xs text-gray-700 px-2 py-0 w-3/6" />
              <div v-if="indexCreateCategoryAllowed" class="button is-small ml-2" @click="onAllowCreateCategory(0)">
                <b-icon icon="times" class="text-xs"></b-icon>
              </div>
              <div v-if="indexCreateCategoryAllowed && category.text" class="button is-small ml-1" @click="createCategory">
                <b-icon icon="check" class="text-xs"></b-icon>
              </div>
            </div>

            <table class="w-full px-6 bg-lightBg border-none">
              <thead class="text-white bg-white border-b">
                <tr class="border-b-1">
                  <th class="px-4 py-4 text-xl font-thin text-indigoDark">
                    ID
                  </th>
                  <th class="px-4 py-4 text-xl font-thin text-indigoDark w-2/6">
                    Section
                  </th>
                  <th class="px-4 py-4 text-xl font-thin text-indigoDark w-full">
                    Questions
                  </th>
                  <th v-if="isEditable" class="px-4 py-4 text-xl font-thin text-indigoDark">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr class="
                    justify-evenly
                    bg-white
                    w-full
                    border-b
                    align-bottom
                    border-darkBg
                    flex-wrap	
                  " v-for="au, index in this.categories" :key="au.uuid">
                  <td class="px-4 py-4 ">{{ index + 1 }}</td>
                  <td class="px-4 py-4 ">
                    <div v-if="category.uuid != au.uuid">{{ au.text }}</div>
                    <textarea v-if="category.uuid == au.uuid" id="question" v-model="category.text"
                      type="text" placeholder="Enter Text" class="border rounded-xs text-gray-700 px-2 py-0 w-full" />
                  </td>
                  <td class="px-4 py-4 flex-wrap	">
                    <div v-for="q, index in au.questions" :key="index" class="flex flex-row items-center mt-1">
                      <div>{{ index + 1 }}. &nbsp;</div>
                      <div v-if="indexUpdateQuestionAllowed != q.uuid">{{ q.text }}</div>
                      <div v-if="indexUpdateQuestionAllowed != q.uuid" class="border-2 rounded-md px-2 ml-2 bg-gray-600 text-white">{{ q.worth }}</div>
                      <textarea v-if="indexUpdateQuestionAllowed == q.uuid" id="question" v-model="question.text"
                        type="text" placeholder="Enter Text" class="border rounded-xs text-gray-700 px-2 py-0 w-3/6" />
                      <div v-if="indexUpdateQuestionAllowed != q.uuid && isEditable" class="button is-small ml-2"
                        @click="onShowModal(au.id, q)">
                        <b-icon icon="edit" class="text-xs"></b-icon>
                      </div>
                      <div class="button is-small ml-1" v-if="isEditable"
                        @click="indexUpdateQuestionAllowed == q.uuid ? onAllowUpdateQuestion(-1, '') : deleteQuestion(q.uuid)">
                        <b-icon icon="times" class="text-xs"></b-icon>
                      </div>
                      <div v-if="indexUpdateQuestionAllowed == q.uuid" class="button is-small ml-1"
                        @click="updateQuestion(q.uuid)">
                        <b-icon icon="check" class="text-xs"></b-icon>
                      </div>
                    </div>
                    <div class="flex flex-row items-center mt-1" v-if="isEditable">
                      <div v-if="indexCreateQuestionAllowed != au.uuid" class="button is-small"
                        @click="onShowModal(au.id)">
                        <b-icon icon="plus" class="text-xs"></b-icon>
                      </div>
                      <textarea v-if="indexCreateQuestionAllowed == au.uuid" id="name" v-model="question.text" type="text"
                        placeholder="Enter Text" class="border rounded-xs text-gray-700 px-2 py-0 w-3/6" />

                      <div v-if="indexCreateQuestionAllowed == au.uuid" class="button is-small ml-2"
                        @click="onAllowCreateQuestion(-1)">
                        <b-icon icon="times" class="text-xs"></b-icon>
                      </div>

                      <div v-if="indexCreateQuestionAllowed == au.uuid && question.text" class="button is-small ml-2"
                        @click="createQuestion(au.id)">
                        <b-icon icon="check" class="text-xs"></b-icon>
                      </div>
                    </div>

                  </td>
                  <td v-if="isEditable" class="px-4 py-4 flex flex-row">
                    <div v-if="category.uuid != au.uuid" class="button is-small ml-2"
                      @click="onAllowUpdateCategory(au.uuid, au.text)">
                      <b-icon icon="edit" class="text-xs"></b-icon>
                    </div>
                    <div class="button is-small ml-2"
                      @click="category.uuid == au.uuid ? onAllowUpdateCategory('', '') : deleteCategory(au.uuid)">
                      <b-icon icon="times" class="text-xs"></b-icon>
                    </div>
                    <!-- <div v-if="indexUpdateCategoryAllowed == au.uuid" class="button is-small ml-1"
                      @click="updateCategory(au.uuid)">
                      <b-icon icon="check" class="text-xs"></b-icon>
                    </div> -->
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- modal -->
          <div class="fixed mt-10 z-50 inset-0 overflow-y-auto" v-if="isShowModal">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
              <div class="fixed inset-0 transition-opacity">
                <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
              </div>

              <div
                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                  <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                    {{ question.uuid ? 'Update Question' : 'New Question' }} 
                  </h3>

                  <div class="mt-3 sm:mt-0">
                    <div class="mt-2">
                      <div class="flex flex-col">
                        <label for="name" class="mb-2 font-semibold text-gray-700">Title</label>
                        <input id="name" v-model="question.text" type="text" placeholder="Enter Title"
                          class="border rounded-md text-gray-700 px-3 py-2 w-full">
                          <span v-if="!question.text && submited" class="text-red-600">Name is required</span>
                      </div>
                      <div class="flex flex-col mt-4">
                        <label for="prem_group" class="mb-2 font-semibold text-gray-700">Point Value</label>
                        <input id="name" v-model="question.worth" type="number" placeholder="Enter Point Value"
                          class="border rounded-md text-gray-700 px-3 py-2 w-full">
                          <span v-if="!question.worth && submited" class="text-red-600">Point value is required</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                  <button type="button" @click="question.uuid ? updateQuestion() : createQuestion()"
                    class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-PrimaryDark text-base font-medium text-white hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm">
                    {{ question.uuid ? 'Update' : 'Create' }}
                  </button>
                  <button type="button" @click="onCloseModal()"
                    class="mt-3 w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
// import router from "@/routes";
import AppLayout from "@/layouts/AppLayout";
import API from "@/services/API";
import { sync } from "vuex-pathify";
import ImageLogo from "@/assets/images/respro-logo.svg";

export default {
  name: "Home",
  components: {
    AppLayout
  },
  data() {
    return {
      defaultImage: ImageLogo,
      premisesSelecte: false,
      categories: [],
      indexCreateQuestionAllowed: -1,
      indexUpdateQuestionAllowed: -1,
      indexCreateCategoryAllowed: 0,
      isShowModal: false,
      submited: false,
      question: {
        text: '',
        worth: '',
        categoryId: '',
        uuid: ''
      },
      category: {
        text: '',
        uuid: ''
      },
      isEditable: false,
    };
  },
  computed: {
    roles: sync("roles/roles"),
    activeUserRole: sync("app/activeUserRole"),
    activeUserUUID: sync("app/activeUserUUID"),
    token: sync("app/session"),
    currentAuditIndex: sync("audit/currentAuditIndex"),
    audits: sync("audit/audits"),
    location: sync("audit/audits[:currentAuditIndex]@location"),
    selectedAuditUuid: sync("audit/selectedAuditUuid"),
    allTemplates: sync("templates/templates"),
  },
  methods: {
    handleClickEvent(data){
      console.log('============= data =============> ', data);
    },
    onCheckEditable(){
      const myAudit = this.allTemplates.find(item => item.id === this.$route.params.uuid);
      if(this.activeUserUUID === myAudit.creator.uuid || this.activeUserRole === 'ROLE_ROOT' || this.activeUserRole === 'ROLE_OWNER'){
        this.isEditable = true;
      }
    },
    fetchCategories() {
      const loadingComponent = this.$buefy.loading.open({ container: null });
      const uuid = this.$route.params.uuid;
      API.getSections(this.token, uuid)
        .then((responses) => {
          this.categories = responses.data["categories"];
          loadingComponent.close();
        })
        .catch((error) => {
          API.APILog(error);
          loadingComponent.close();
          this.$buefy.dialog.alert("Error fetching account information.");
        });
    },
    onAllowCreateQuestion(d) {
      this.question.text = '';
      this.indexCreateQuestionAllowed = d;
      this.indexUpdateQuestionAllowed = -1;
    },
    onAllowUpdateQuestion(d, text) {
      this.indexCreateQuestionAllowed = -1;
      this.indexUpdateQuestionAllowed = d;
      this.question.text = text;
    },
    onAllowUpdateCategory(uuid, text) {
      this.category.text = text;
      this.category.uuid = uuid
    },
    onAllowCreateCategory(d) {
      this.indexCreateCategoryAllowed = d;
      if (!d) {
        this.category.text = '';
      }
    },
    onShowModal(id, data){
      // this.onAllowCreateQuestion(id);
      this.isShowModal = true;
      this.question.categoryId = id;
      if(data){
        this.question.text = data.text;
        this.question.uuid = data.uuid;
        this.question.worth = data.worth;
      }else{
        this.question.text = '';
        this.question.uuid = '';
      }
      this.submited = false;
    },
    onCloseModal(){
      this.isShowModal = false;
      this.question.text = '';
      this.question.uuid = '';
      this.question.worth = '';
      this.question.id = '';
    },
    updateQuestion() {
      this.submited = true;
      if(!this.question.text || !this.question.worth){
        return false;
      }
      const loadingComponent = this.$buefy.loading.open({ container: null });
      API.update_question(this.token, this.question.uuid, { 
        text: this.question.text,
        worth: this.question.worth,
      }).then((response) => {
        this.fetchCategories()
        loadingComponent.close();
        if (response)
          this.$buefy.toast.open({
            message: "Question has been updated successfully",
            type: "is-success",
          });
        this.indexUpdateQuestionAllowed = -1;
        this.onCloseModal();
      }).catch((error) => {
        loadingComponent.close();
        API.APILog(error);
        this.onCloseModal();
      });
    },
    deleteQuestion(uuid) {
      if (uuid) {

        this.$buefy.dialog.confirm({
          title: "Deleting a question",
          message:
            "Are you sure you want to <b>delete</b> a question? This action cannot be undone.",
          confirmText: "Delete",
          type: "is-danger",
          hasIcon: true,
          onConfirm: () => {

            const loadingComponent = this.$buefy.loading.open({ container: null });
            API.delete_question(this.token, uuid)
              .then(() => {

                this.fetchCategories()

                loadingComponent.close();

                this.$buefy.toast.open({
                  message: "A question has been deleted successfully",
                  type: "is-success",
                });
              })
              .catch((error) => {
                loadingComponent.close();
                API.APILog(error);
                this.$buefy.toast.open({
                  message: "This question can't delete",
                  type: "is-danger",
                });
              });
          },
        });
      } else {

        this.$buefy.dialog.alert(
          "No premises found."
        );
      }
    },
    createQuestion() {
      this.submited = true;
      const template_id = this.$route.params.uuid;

      if(!this.question.text || !this.question.worth){
        return false;
      }
      let json_data = {
        text: this.question.text,
        category: this.question.categoryId,
        type: 1,
        weight: 1,
        worth: this.question.worth,
        attachments: { "non_applicable": true },
        template_id: template_id
      };

      const loadingComponent = this.$buefy.loading.open({ container: null });

      API.create_question(this.token, json_data)
        .then((responses) => {
          loadingComponent.close();
          if (responses)
            this.$buefy.toast.open({
              message: "Audit Question has been created successfully!",
              type: "is-success",
            });
            this.onCloseModal();

          this.indexCreateQuestionAllowed = -1;
          this.fetchCategories()
        })
        .catch((error) => {
          loadingComponent.close();
          API.APILog(error);
          this.indexCreateQuestionAllowed = -1;
          this.onCloseModal();
        });
    },
    createCategory() {
      const uuid = this.$route.params.uuid;

      let json_data = {
        text: this.category.text,
        color: '#ff0000',
        children: {},
        challenge: false,
        icon: 'Critical_items'
      };

      const loadingComponent = this.$buefy.loading.open({ container: null });

      API.create_category(this.token, uuid, json_data)
        .then((responses) => {
          loadingComponent.close();
          if (responses)
            this.$buefy.toast.open({
              message: "Audit Section has been created successfully!",
              type: "is-success",
            });
          this.category.text = '';
          this.indexCreateCategoryAllowed = 0;
          this.fetchCategories()
        })
        .catch((error) => {
          loadingComponent.close();
          API.APILog(error);
          this.indexCreateCategoryAllowed = 0;
        });
    },
    updateCategory(uuid) {
      if(!this.category.text){
        this.$buefy.toast.open({
            message: "Audit has been saved!",
            type: "is-success",
          });
        return false;
      }
      const loadingComponent = this.$buefy.loading.open({ container: null });
      API.update_category(this.token, uuid, { text: this.category.text }).then((response) => {
        this.fetchCategories()
        loadingComponent.close();
        if (response)
          this.$buefy.toast.open({
            message: "Audit Section has been updated successfully",
            type: "is-success",
          });
        this.category.uuid = '';
        this.category.text = '';
      }).catch((error) => {
        loadingComponent.close();
        API.APILog(error);
      });
    },
    deleteCategory(uuid) {
      if (uuid) {

        this.$buefy.dialog.confirm({
          title: "Deleting a Section",
          message:
            "Are you sure you want to <b>delete</b> a Section? This action cannot be undone.",
          confirmText: "Delete",
          type: "is-danger",
          hasIcon: true,
          onConfirm: () => {

            const loadingComponent = this.$buefy.loading.open({ container: null });
            API.delete_category(this.token, uuid)
              .then(() => {

                this.fetchCategories()

                loadingComponent.close();

                this.$buefy.toast.open({
                  message: "Audit Section has been deleted successfully",
                  type: "is-success",
                });
              })
              .catch((error) => {
                loadingComponent.close();
                API.APILog(error);
                this.$buefy.toast.open({
                  message: "This Audit Section can't delete",
                  type: "is-danger",
                });
              });
          },
        });
      } else {

        this.$buefy.dialog.alert(
          "No setions found."
        );
      }
    }
  },
  created() {
    this.fetchCategories();
    this.onCheckEditable();
  },
};
</script>
