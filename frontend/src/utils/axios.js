import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com'
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

// api.interceptors.response.use(
//   (response) => response, // Pass through successful responses
//   (error) => {
//     if (error.response?.status === 401) {
//       console.log('Unauthorized! Redirecting to login...');
//       // Handle token expiration (e.g., logout user)
//     }
//     return Promise.reject(error);
//   }
// );

export default api;