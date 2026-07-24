import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

export const getHealth = () => api.get('/health');
export const getMetadata = () => api.get('/metadata');
export const predictFault = (payload) => api.post('/predict-fault', payload);
export const predictAnomaly = (payload) => api.post('/predict-anomaly', payload);
export const predictMaintenance = (payload) => api.post('/predict-maintenance', payload);

export default api;
