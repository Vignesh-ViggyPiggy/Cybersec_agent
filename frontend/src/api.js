import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export const analyzeLog = async (logText, useBraveSearch = true) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/analyze`, {
      log_text: logText,
      use_brave_search: useBraveSearch
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Analysis failed');
    } else if (error.request) {
      throw new Error('Cannot connect to API server. Please ensure the server is running on http://localhost:8080');
    } else {
      throw new Error('An unexpected error occurred');
    }
  }
};

export const checkHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    throw new Error('API health check failed');
  }
};
