<template>
    <AppLayout :userRole="activeUserRole" :imageLogo="defaultImage" headerTitle="Premises">
        <div class="mt-6 px-4 w-full bg-white text-PrimaryText h-full">
            <!-- Premises  tab -->
            <b-tabs v-model="activeTab">
                <b-tab-item label="Premises">
                    <div class="columns">
                        <div class="column">
                            <table class="table is-fullwidth">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Group</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="prem in paginatedPremises" :key="prem.uuid">
                                        <td>{{ prem.name }}</td>
                                        <td>{{ prem.group.name }}</td>
                                        <td>
                                            <button class="button is-small" @click="editPremises(prem)">Edit</button>
                                            <button class="button is-small is-danger"
                                                @click="deletePremises(prem.uuid)">Delete</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="mt-4">
                                <nav class="flex justify-center">
                                    <ul class="pagination">
                                        <li v-if="currentPage > 1">
                                            <button class="pagination-previous" @click="prevPage()">Previous</button>
                                        </li>
                                        <li v-for="page in pages" :key="page">
                                            <button class="pagination-link" :class="{ 'is-current': currentPage === page }"
                                                @click="changePage(page)">{{ page }}</button>
                                        </li>
                                        <li v-if="currentPage < totalPages">
                                            <button class="pagination-next" @click="nextPage()">Next</button>
                                        </li>
                                    </ul>
                                </nav>
                            </div>
                        </div>
                    </div>
                    <div class="add-button">
                        <b-button @click="showPremisesModal('New')" type="is-primary">Add Premises</b-button>
                    </div>


                    <div class="fixed mt-10 z-50 inset-0 overflow-y-auto" v-if="showPremises">
                        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                            <div class="fixed inset-0 transition-opacity">
                                <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
                            </div>

                            <div
                                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                                        {{ openForUpdate ? 'Update Premises' : 'New Premises' }}
                                    </h3>

                                    <div class="mt-3 sm:mt-0">
                                        <div class="mt-2">
                                            <div class="flex flex-col">
                                                <label for="name" class="mb-2 font-semibold text-gray-700">Name</label>
                                                <input id="name" v-model="newPremises.name" type="text"
                                                    placeholder="Enter Name"
                                                    class="border rounded-md text-gray-700 px-3 py-2 w-full">
                                            </div>
                                            <div class="flex flex-col mt-4">
                                                <label for="prem_group"
                                                    class="mb-2 font-semibold text-gray-700">Group</label>
                                                <div class="relative">
                                                    <select id="prem_group" v-model="newPremises.group"
                                                        class="border rounded-md appearance-none py-2 pl-3 pr-8 w-full text-gray-700">
                                                        <option v-for="option in groupOptions" :key="option.uuid"
                                                            :value="option">{{ option.name }}</option>
                                                    </select>
                                                    <div
                                                        class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                                                        <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg"
                                                            viewBox="0 0 20 20">
                                                            <path d="M10 12l-6-6h12z" />
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                                    <button type="button" @click="addPremises"
                                        class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-PrimaryDark text-base font-medium text-white hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm">
                                        {{ openForUpdate ? 'Update' : 'Create' }}
                                    </button>
                                    <button type="button" @click="hidePremisesModal"
                                        class="mt-3 w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </b-tab-item>

                <!-- Premises Group tab -->
                <b-tab-item label="Premises Group">
                    <div class="columns">
                        <div class="column">
                            <table class="table is-fullwidth">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Organization</th>
                                        <th>Email report</th>
                                        <th>Manager</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="group in groups" :key="group.uuid">
                                        <td>{{ group.name }}</td>
                                        <td>{{ group.organization.name }}</td>
                                        <td class="capitalize">{{ group.render_enabled }}</td>
                                        <td>{{ group.manager.name }}</td>
                                        <td>
                                            <button class="button is-small" @click="editGroup(group)">Edit</button>
                                            <button class="button is-small is-danger"
                                                @click="deleteGroup(group.uuid)">Delete</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="add-button">
                        <b-button @click="showPremisesGroupModal('New')" type="is-primary">Add Group</b-button>
                    </div>


                    <div class="fixed mt-10 z-50 inset-0 overflow-y-auto" v-if="showGroup">
                        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                            <div class="fixed inset-0 transition-opacity">
                                <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
                            </div>

                            <div
                                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                                        {{ openForUpdate ? 'Update Group' : 'New Group' }}
                                    </h3>

                                    <div class="mt-3 sm:mt-0">
                                        <div class="mt-2">
                                            <div class="flex flex-col">
                                                <label for="group_name"
                                                    class="mb-2 font-semibold text-gray-700">Name</label>
                                                <input id="group_name" v-model="newGroup.name" type="text"
                                                    placeholder="Enter Name"
                                                    class="border rounded-md text-gray-700 px-3 py-2 w-full">
                                            </div>
                                            <div class="flex flex-col mt-4">
                                                <label for="group_org"
                                                    class="mb-2 font-semibold text-gray-700">Organization</label>
                                                <div class="relative">
                                                    <select id="group_org" v-model="newGroup.organization" @change="onChangeOrganization"
                                                        class="border rounded-md appearance-none py-2 pl-3 pr-8 w-full text-gray-700">
                                                        <option v-for="option in organizationOptions" :key="option.uuid"
                                                            :value="option">{{ option.name }}</option>
                                                    </select>
                                                    <div
                                                        class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                                                        <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg"
                                                            viewBox="0 0 20 20">
                                                            <path d="M10 12l-6-6h12z" />
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-if="newGroup.organization.uuid" class="flex flex-col mt-4">
                                                <label for="group_manager"
                                                    class="mb-2 font-semibold text-gray-700">Manager</label>
                                                <div class="relative">
                                                    
                                                  <select id="group_manager" v-model="newGroup.manager"
                                                        class="border rounded-md appearance-none py-2 pl-3 pr-8 w-full text-gray-700">
                                                        <option v-for="option in filterManagers" :key="option.uuid"
                                                            :value="option">{{ option.name }}</option>
                                                    </select>
<!-- 
                                                    <div class="location-box" v-if="isAvailableLocationModal">
                                                      <div v-for="location in filterManagers" :key="location.uuid">
                                                        <label class="flex items-center">
                                                          <input type="checkbox" v-model="selectedLocationUuids" :value="location.uuid"
                                                            :checked="selectedLocationUuids.includes(location.uuid)"
                                                            class="form-checkbox bg-PrimaryDark mr-2 h-5 w-5">
                                                          <span style="font-size: 15px;" class="text-left">
                                                            {{ location.name }}
                                                          </span>
                                                        </label>
                                                      </div>
                                                      <div @click="isAvailableLocationModal = false" class="cursor-pointer text-xs">close</div>
                                                    </div> -->


                                                    <div
                                                        class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                                                        <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg"
                                                            viewBox="0 0 20 20">
                                                            <path d="M10 12l-6-6h12z" />
                                                        </svg>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="flex flex-col mt-4">
                                                <label class="mb-2 font-semibold text-gray-700" for="group_render_enabled">
                                                    Email Report?
                                                </label>
                                                <div class="flex items-center">
                                                    <span class="mr-2">No</span>
                                                    <label for="group_render_enabled"
                                                        class="flex items-center cursor-pointer">
                                                        <div class="relative">
                                                            <input id="group_render_enabled"
                                                                v-model="newGroup.render_enabled" type="checkbox"
                                                                @click="newGroup.render_enabled = !newGroup.render_enabled"
                                                                class="hidden" :true-value="true" :false-value="false">
                                                            <div
                                                                class="toggle__line w-12 h-6 bg-PrimaryDark rounded-full shadow-inner">
                                                            </div>
                                                            <div class="toggle__dot absolute w-6 h-6 bg-white rounded-full shadow inset-y-0"
                                                                :class="newGroup.render_enabled ? 'right-0' : 'left-0'">
                                                            </div>
                                                        </div>
                                                    </label>
                                                    <span class="ml-2">Yes</span>
                                                </div>
                                            </div>


                                        </div>
                                    </div>
                                </div>

                                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                                    <button type="button" @click="addGroup"
                                        class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-PrimaryDark text-base font-medium text-white hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm">
                                        {{ openForUpdate ? 'Update' : 'Create' }}
                                    </button>
                                    <button type="button" @click="hidePremisesGroupModal"
                                        class="mt-3 w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </b-tab-item>

                <!-- Premises Organization tab -->
                <b-tab-item label="Premises Organization">
                    <div class="columns">
                        <div class="column">
                            <table class="table is-fullwidth">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Email report</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="organization in organizations" :key="organization.uuid">
                                        <td>{{ organization.name }}</td>
                                        <td class="capitalize">{{ organization.render_enabled }}</td>
                                        <td>
                                            <button class="button is-small"
                                                @click="editOrganization(organization)">Edit</button>
                                            <button class="button is-small is-danger"
                                                @click="deleteOrganization(organization.uuid)">Delete</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <button v-if="activeUserRole === 'ROLE_ROOT'" class="button is-primary" @click="showOrganizationModal('New')">Add Organization</button>

                    <!-- Add Premises Organization Modal -->
                    <div class="fixed mt-10 z-50 inset-0 overflow-y-auto" v-if="showOrgnization">
                        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                            <div class="fixed inset-0 transition-opacity">
                                <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
                            </div>

                            <div
                                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                                        {{ openForUpdate ? 'Update Organization' : 'New Organization' }}
                                    </h3>

                                    <div class="mt-3 sm:mt-0">
                                        <div class="mt-2">
                                            <div class="flex flex-col">
                                                <label for="org_name" class="mb-2 font-semibold text-gray-700">Name</label>
                                                <input id="org_name" v-model="newOrganization.name" type="text"
                                                    placeholder="Enter Name"
                                                    class="border rounded-md text-gray-700 px-3 py-2 w-full">
                                            </div>
                                            <div class="flex flex-col mt-4">
                                                <label class="mb-2 font-semibold text-gray-700"
                                                    for="organization_render_enabled">
                                                    Email Report?
                                                </label>
                                                <div class="flex items-center">
                                                    <span class="mr-2">No</span>
                                                    <label for="organization_render_enabled"
                                                        class="flex items-center cursor-pointer">
                                                        <div class="relative">
                                                            <input id="organization_render_enabled"
                                                                v-model="newOrganization.render_enabled" type="checkbox"
                                                                @click="newOrganization.render_enabled = !newOrganization.render_enabled"
                                                                class="hidden" :true-value="true" :false-value="false">
                                                            <div
                                                                class="toggle__line w-12 h-6 bg-PrimaryDark rounded-full shadow-inner">
                                                            </div>
                                                            <div class="toggle__dot absolute w-6 h-6 bg-white rounded-full shadow inset-y-0"
                                                                :class="newOrganization.render_enabled ? 'right-0' : 'left-0'">
                                                            </div>
                                                        </div>
                                                    </label>
                                                    <span class="ml-2">Yes</span>
                                                </div>
                                            </div>


                                        </div>
                                    </div>
                                </div>

                                <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                                    <button type="button" @click="addOrganization"
                                        class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-PrimaryDark text-base font-medium text-white hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm">
                                        {{ openForUpdate ? 'Update' : 'Create' }}
                                    </button>
                                    <button type="button" @click="hideOrganizationModal"
                                        class="mt-3 w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </b-tab-item>
            </b-tabs>
        </div>
    </AppLayout>
</template>
  
<script>
import AppLayout from "@/layouts/AppLayout";
import API from "@/services/API";
import { sync } from "vuex-pathify";
import ImageLogo from "@/assets/images/respro-logo.svg";
const _ = require('lodash');

export default {
    name: "premises",
    components: {
        AppLayout,
    },
    data() {
        return {
            defaultImage: ImageLogo,

            activeTab: 0,
            showPremises: false,
            showGroup: false,
            showOrgnization: false,
            currentPage: 1,
            itemsPerPage: 20,
            newPremises: {
                uuid: '',
                name: '',
                group: {
                    name: '',
                    uuid: ''
                },
            },
            newGroup: {
                name: '',
                render_enabled: false,
                organization: {
                    name: '',
                    uuid: ''
                },
                manager: {
                    name: '',
                    uuid: ''
                }
            },
            newOrganization: {
                name: '',
                render_enabled: false,
            },
            groupOptions: [],
            organizationOptions: [],
            openForUpdate: false,
            filterManagers: [],
            isAvailableLocationModal: false

        };
    },
    computed: {
        premises: sync("premises/premises"),
        activeUserRole: sync("app/activeUserRole"),
        groups: sync("premises/groups"),
        managers: sync("users/managers"),
        organizations: sync("premises/organizations"),
        token: sync("app/session"),
        currentAuditIndex: sync("audit/currentAuditIndex"),
        totalPages() {
            return Math.ceil(this.premises.length / this.itemsPerPage);
        },
        paginatedPremises() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.premises.slice(start, end);
        },
        pages() {
            const pages = [];
            for (let i = 1; i <= this.totalPages; i++) {
                pages.push(i);
            }
            return pages;
        }
    },
    methods: {
        onChangeOrganization() {
            this.filterManagers = this.managers.filter(x => {
                const orgUUID = x.organizations.length > 0 ? x.organizations[0].uuid : ''
                return orgUUID === this.newGroup.organization.uuid
            })
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        changePage(page) {
            this.currentPage = page;
        },


        showPremisesModal(isNew) {
            this.hidePremisesGroupModal()
            this.hideOrganizationModal()
            if (isNew == "New") {
                this.newPremises = {
                    name: '',
                    group: null
                }
                this.openForUpdate = false;
            } else this.openForUpdate = true
            this.showPremises = true
        },

        hidePremisesModal() {
            this.newPremises = {
                name: '',
                group: null
            }
            this.showPremises = false
        },

        showPremisesGroupModal(isNew) {
            this.hidePremisesModal()
            this.hideOrganizationModal()
            if (isNew == "New") {
                this.newGroup = {
                    name: '',
                    render_enabled: false,
                    organization: {
                        name: '',
                        uuid: ''
                    },
                manager: {
                    name: '',
                    uuid: ''
                }
                }
                this.openForUpdate = false;
            } else this.openForUpdate = true
            this.showGroup = true
        },

        hidePremisesGroupModal() {
            this.newGroup = {
                name: '',
                render_enabled: false,
                organization: {
                    name: '',
                    uuid: ''
                }
            }
            this.showGroup = false
        },

        showOrganizationModal(isNew) {
            this.hidePremisesGroupModal()
            this.hidePremisesModal()
            if (isNew == "New") {
                this.newOrganization = {
                    name: '',
                    render_enabled: false
                }
                this.openForUpdate = false;
            } else this.openForUpdate = true
            this.showOrgnization = true
        },

        hideOrganizationModal() {
            this.newOrganization = {
                name: '',
                render_enabled: false
            }
            this.showOrgnization = false
        },

        addPremises() {

            const loadingComponent = this.$buefy.loading.open({ container: null });

            const data = {
                name: this.newPremises.name,
                group: this.newPremises.group.uuid
            }

            if (!this.openForUpdate) {

                API.create_premises(this.token, data)
                    .then((responses) => {

                        this.fetchPremises()

                        loadingComponent.close();

                        this.showPremises = false

                        if (responses)
                            this.$buefy.toast.open({
                                message: "Premises has been created successfully",
                                type: "is-success",
                            });
                    })
                    .catch((error) => {
                        loadingComponent.close();
                        this.showPremises = false
                        API.APILog(error);
                    });
            } else {
                API.update_premises(this.token, this.newPremises.uuid, data).then((response) => {
                    this.fetchPremises()

                    loadingComponent.close();

                    this.showPremises = false

                    if (response)
                        this.$buefy.toast.open({
                            message: "Premises has been updated successfully",
                            type: "is-success",
                        });
                }).catch((error) => {
                    loadingComponent.close();
                    this.showPremises = false
                    API.APILog(error);
                });
            }

        },
        addGroup() {

            let json_data = {
                name: this.newGroup.name,
                render_enabled: this.newGroup.render_enabled,
                premises_organization: this.newGroup.organization.uuid,
                manager_uuid: this.newGroup.manager.uuid
            };

            const loadingComponent = this.$buefy.loading.open({ container: null });

            if(this.openForUpdate) {
                API.update_premises_group(this.token, this.newGroup.uuid, json_data).then((response) => {
                    this.fetchPremises()

                    loadingComponent.close();

                    this.showGroup = false

                    if (response)
                        this.$buefy.toast.open({
                            message: "Premises group has been updated successfully",
                            type: "is-success",
                        });
                }).catch((error) => {
                    loadingComponent.close();
                    this.showGroup = false
                    API.APILog(error);
                });
            } else {
            API.create_premises_group(this.token, json_data)
                .then((responses) => {

                    this.showGroup = false;

                    this.fetchPremises()

                    if (responses)
                        this.$buefy.toast.open({
                            message: "Premises group has been created successfully",
                            type: "is-success",
                        });

                    loadingComponent.close();


                })
                .catch((error) => {
                    this.showGroup = false;
                    loadingComponent.close();
                    API.APILog(error);
                });
            }

        },
        addOrganization() {

            let json_data = {
                name: this.newOrganization.name,
                render_enabled: this.newOrganization.render_enabled,
            };

            const loadingComponent = this.$buefy.loading.open({ container: null });

            if(this.openForUpdate) {
                API.update_premises_organization(this.token, this.newOrganization.uuid, json_data).then((response) => {
                    
                    this.fetchPremises()

                    loadingComponent.close();

                    this.showOrgnization = false

                    if (response)
                        this.$buefy.toast.open({
                            message: "Premises group has been updated successfully",
                            type: "is-success",
                        });
                }).catch((error) => {
                    loadingComponent.close();
                    this.showOrgnization = false
                    API.APILog(error);
                });
            } else {


            API.create_premises_organization(this.token, json_data)
                .then((responses) => {

                    loadingComponent.close();

                    if (responses)
                        this.$buefy.toast.open({
                            message: "Premises organization has been created successfully",
                            type: "is-success",
                        });

                    this.fetchPremises()

                    this.showOrgnization = false

                })
                .catch((error) => {
                    loadingComponent.close();
                    API.APILog(error);
                });
            }
        },
        editPremises(prem) {
            this.newPremises = Object.assign({}, prem)
            this.showPremises = true;
            this.openForUpdate = true;
        },
        editGroup(group) {
            this.newGroup = Object.assign({}, group);
            this.showGroup = true;
            this.openForUpdate = true;
        },
        editOrganization(org) {
            this.newOrganization = Object.assign({}, org);
            this.showOrgnization = true;
            this.openForUpdate = true;

        },
        deletePremises(uuid) {

            if (uuid) {

                this.$buefy.dialog.confirm({
                    title: "Deleting a premises",
                    message:
                        "Are you sure you want to <b>delete</b> a premise? This action cannot be undone.",
                    confirmText: "Delete",
                    type: "is-danger",
                    hasIcon: true,
                    onConfirm: () => {



                        const loadingComponent = this.$buefy.loading.open({ container: null });
                        API.delete_premises(this.token, uuid)
                            .then(() => {

                                this.fetchPremises()

                                loadingComponent.close();

                                this.$buefy.toast.open({
                                    message: "A permises has been deleted successfully",
                                    type: "is-success",
                                });
                            })
                            .catch((error) => {
                                loadingComponent.close();
                                API.APILog(error);
                            });
                    },
                });
            } else {

                this.$buefy.dialog.alert(
                    "No premises found."
                );
            }
        },
        deleteOrganization(uuid) {
            if (uuid) {
                this.$buefy.dialog.confirm({
                    title: "Deleting an organization",
                    message:
                        "Are you sure you want to <b>delete</b> a premise organization? This action cannot be undone.",
                    confirmText: "Delete",
                    type: "is-danger",
                    hasIcon: true,
                    onConfirm: () => {
                        const loadingComponent = this.$buefy.loading.open({ container: null });
                        API.delete_premises_organization(this.token, uuid)
                            .then(() => {

                                this.fetchPremises()
                                loadingComponent.close();
                                this.$buefy.toast.open({
                                    message: "A permises organization has been deleted successfully",
                                    type: "is-success",
                                });
                            })
                            .catch((error) => {

                                loadingComponent.close();
                                API.APILog(error);
                            });
                    },
                });
            } else {
                this.$buefy.dialog.alert(
                    "No audit found. If you expect to see a new audit, try logging out first."
                );
            }
        },
        deleteGroup(uuid) {
            if (uuid) {
                this.$buefy.dialog.confirm({
                    title: "Deleting a group",
                    message:
                        "Are you sure you want to <b>delete</b> a premise group? This action cannot be undone.",
                    confirmText: "Delete",
                    type: "is-danger",
                    hasIcon: true,
                    onConfirm: () => {

                        const loadingComponent = this.$buefy.loading.open({ container: null });
                        API.delete_premises_group(this.token, uuid)
                            .then(() => {

                                this.fetchPremises()
                                loadingComponent.close();
                                this.$buefy.toast.open({
                                    message: "A permises group has been deleted successfully",
                                    type: "is-success",
                                });
                            })
                            .catch((error) => {

                                loadingComponent.close();
                                API.APILog(error);
                            });
                    },
                });
            } else {
                this.$buefy.dialog.alert(
                    "No audit found. If you expect to see a new audit, try logging out first."
                );
            }
        },
        onBack() {
            this.currentAuditIndex = -1;
            this.$router.push({ name: "home" });
            console.log("User voluntarily stopped location selection");
        },

        mapPremises(results) {
            this.premises = results.map(({ uuid, name, group_uuid, group }) => ({
                uuid,
                name,
                group: {
                    uuid: group_uuid,
                    name: group
                }
            }))
        },

        mapGroups(results) {
            this.groups = results.map(({ uuid, name, organization, organization_uuid, render_enabled, manager_name, manager_uuid}) => ({
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

            this.groupOptions.push(...this.groups.map(({ name, uuid }) => ({ name, uuid })));
            this.groupOptions = _.uniqBy(this.groupOptions, 'uuid');
        },

        fetchPremises() {
            const loadingComponent = this.$buefy.loading.open({ container: null });
            Promise.all([
                API.fetch_premises_sort(this.token, 'asc'),
                API.fetch_groups_sort(this.token, 'asc'),
                API.fetch_organizations_sort(this.token, 'asc'),
                API.fetch_managers(this.token)
            ])
                .then((responses) => {
                    console.log(responses)
                    this.mapPremises(responses[0].data["premises"])
                    this.mapGroups(responses[1].data["groups"])
                    this.organizations = responses[2].data["organizations"];
                    this.organizationOptions = this.organizations.map(({ name, uuid }) => ({ name, uuid }))
                    this.managers = responses[3].data["managers"]
                    loadingComponent.close();
                })
                .catch((error) => {
                    API.APILog(error);
                    loadingComponent.close();
                    this.$buefy.dialog.alert("Error fetching premises information.");
                });
        }
    },

    created() {
        this.fetchPremises()
    },
};
</script>


<style scoped>
.dropdown-box {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 8px;
}
.location-box {
  background-color: #fff;
  position: absolute;
  width: 200px;
  max-height: 400px;
  box-sizing: border-box;
  box-shadow: -1px 5px 15px -3px rgba(0,0,0,0.75);
  border-radius: 8px;
  padding: 8px;
  font-size: 17px;
  z-index: 999;
  overflow-y: auto;
}
</style>