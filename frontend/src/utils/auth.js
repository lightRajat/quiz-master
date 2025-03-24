import axios from "axios";

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
    sessionStorage.setItem('user', response.data.user);
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
  sessionStorage.removeItem('user');
  window.showToast('Successfully Logged Out', 'primary');
}

const getCurrentUser = () => {
  return sessionStorage.getItem('user');
};

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
  if (typeof(response.data === 'string')) {
    try {
      response.data = JSON.parse(response.data);
    } catch (error) {
      console.error('Error parsing JSON response:', error);
    }
  }
  return response;
}, (error) => {
  if (error.response) {
    const statusCode = error.response.status;
    if (statusCode === 401 || statusCode === 403) {
      window.location.href = '/unauthorized';
    }
  }
  return Promise.reject(error);
});

export { api, loginUser, logoutUser, getCurrentUser };