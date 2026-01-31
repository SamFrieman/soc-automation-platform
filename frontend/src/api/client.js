import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;

// API Methods
export const auth = {
  login: (username, password) =>
    axios.post(`${API_BASE_URL}/token/`, { username, password }),
  
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
};

export const alerts = {
  list: (params) => apiClient.get('/alerts/', { params }),
  get: (id) => apiClient.get(`/alerts/${id}/`),
  create: (data) => apiClient.post('/alerts/', data),
  resolve: (id) => apiClient.post(`/alerts/${id}/resolve/`),
};

export const playbooks = {
  list: () => apiClient.get('/playbooks/'),
  execute: (id, alertId) => apiClient.post(`/playbooks/${id}/execute/`, { alert_id: alertId }),
};

export const dashboard = {
  getStats: () => apiClient.get('/dashboard/'),
};