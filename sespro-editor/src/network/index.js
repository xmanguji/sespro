import settings from "./settings";
import axios from "axios";

const network = axios.create({
    baseURL: settings.API_URL,
    headers: settings.HEADERS,
    validateStatus: x => x ? true : true
});

export default network;
