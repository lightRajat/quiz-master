import axios from "axios";
import router from "./router";

const loginUser = async (email, passwd) => {
  const formData = new FormData();
  formData.set('email', email);
  formData.set('password', passwd);
  const returnMsg = {
    'status': ''
  };
  try {
    const response = await axios.post('/api/login', formData);
    sessionStorage.setItem('token', response.data.token);
    returnMsg.status = 'success';
    returnMsg.user = response.data.user;
  } catch (error) {
    returnMsg.status = 'failed';
    returnMsg.info = error.response.data.info;
  } finally {
    return returnMsg;
  }
};

const logoutUser = () => {
  sessionStorage.removeItem('token');
  router.push('/');
}

const api = axios.create({
  baseURL: '/api'
});

api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  Promise.reject(error);
});

api.interceptors.response.use((response) => {
  return response;
}, (error) => {
  if (error.response) {
    const statusCode = error.response.status;
    if (statusCode === 401 || statusCode === 403) {
      sessionStorage.removeItem('token');
      router.push('/unauthorized');
    }
  }
  return Promise.reject(error);
});

export { api, loginUser, logoutUser };