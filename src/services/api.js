// src/services/api.js
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // FastAPI backend

export const analyzeTwitter = async (username, company) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/analyze`, {
      username,
      company
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};
