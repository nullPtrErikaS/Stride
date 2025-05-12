// src/lib/api.ts
import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

// Attach token automatically if exists
API.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default API;

