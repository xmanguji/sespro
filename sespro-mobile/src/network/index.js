import settings from "./settings";
import axios from "axios";

const network = axios.create({
    // baseURL: localStorage.getItem('dev') ? settings.API_URL_DEV : settings.API_URL_PROD,
    baseURL: settings.API_URL,
    headers: settings.HEADERS,
    validateStatus: x => x ? true : true
});

export default network;
