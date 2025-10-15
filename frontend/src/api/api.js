import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export const getForecasts = async () => {
  const response = await API.get("/forecasts/");
  return response.data;
};

export const getInsight = async (forecastId) => {
  const response = await API.get(`/insights/${forecastId}`);
  return response.data;
};
