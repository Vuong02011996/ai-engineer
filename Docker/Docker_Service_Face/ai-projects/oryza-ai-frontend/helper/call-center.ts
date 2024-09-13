import { CookieStoreControl } from "@/hooks/cookie-storage";
import axios, {
  AxiosError,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from "axios";
const LOGIN_URL = "/login";

const axiosClient = axios.create({
  baseURL: "/service/api/v1",
});

const cookieInstance = CookieStoreControl.getInstance();
axiosClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    const accessToken = cookieInstance.token.get_access_token();

    if (config.url === "/user/get/me" && !accessToken) {
      return Promise.reject();
    }

    if (accessToken) {
      config.headers.Authorization = "Bearer " + accessToken;
    }

    return config;
  },
  (err: AxiosError) => {
    return Promise.reject(err);
  }
);

const directToHome = () => {
  if (window && window.location.pathname !== LOGIN_URL) {
    window.location.replace(LOGIN_URL);
  }
};

axiosClient.interceptors.response.use(
  async (response: AxiosResponse) => {
    return response;
  },

  async (err) => {
    if (err.response && err.response?.data) {
    } else {
      return Promise.reject(err);
    }
    const { statusCode, message } = err.response?.data as any;

    if (statusCode === 401) {
      cookieInstance.token.remove_access_token();
      directToHome();
      return Promise.reject(err);
    } else {
      return Promise.reject(err);
    }
  }
);

export default axiosClient;
