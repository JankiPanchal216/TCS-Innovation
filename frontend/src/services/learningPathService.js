import axios from 'axios';

const API_URL = 'http://localhost:8000/api/learning-path';

export const getLearningPath = async (id = 'lp-1') => {
  const response = await axios.get(`${API_URL}`);
  return response.data;
};

export const getLearningPathWeeks = async (id = 'lp-1') => {
  const response = await axios.get(`${API_URL}/${id}/weeks`);
  return response.data;
};

export const getLearningPathAnalytics = async (id = 'lp-1') => {
  const response = await axios.get(`${API_URL}/${id}/analytics`);
  return response.data;
};

export const regenerateLearningPath = async (id = 'lp-1') => {
  const response = await axios.post(`${API_URL}/${id}/regenerate`);
  return response.data;
};
