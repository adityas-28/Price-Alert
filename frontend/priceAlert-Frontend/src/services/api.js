import axios from "axios";
import { API_BASE_URL } from "../config";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (userData) => {
    const response = await api.post("/api/user/register", userData);
    return response.data;
  },

  login: async (userData) => {
    const response = await api.post("/api/user/login", userData);
    return response.data;
  },

  logout: async () => {
    const response = await api.post("/api/user/logout");
    return response.data;
  },
};

// Product API
export const productAPI = {
  getProduct: async (asin) => {
    const response = await api.get(`/api/product/${asin}`);
    return response.data;
  },

  scrapeProduct: async (asin) => {
    const response = await api.get(`/api/scraper/scrap/${asin}`);
    return response.data;
  },
};

// Alert API
export const alertAPI = {
  addAlert: async (alertData) => {
    const response = await api.post("/api/alert/add", alertData);
    return response.data;
  },
};

// Helper function to extract ASIN from Tanishq URL
// export const extractASINFromURL = (url) => {
//   try {
//     // Tanishq URL format: https://www.tanishq.co.in/product/product-name-{asin}.html?lang=en_IN
//     // Or: https://www.tanishq.co.in/product/{asin}
//     const urlObj = new URL(url);
//     const pathParts = urlObj.pathname.split("/").filter((part) => part);
//     const productPart = pathParts[pathParts.length - 1];

//     // Remove .html and query params if present
//     let cleanPart = productPart.split(".html")[0].split("?")[0];

//     // Extract ASIN - it's typically the last segment after the last hyphen
//     // Format: "product-name-50e5b1fck2a02" -> "50e5b1fck2a02"
//     const parts = cleanPart.split("-");

//     // ASIN is usually alphanumeric and at the end
//     // Try to find the last segment that looks like an ASIN (alphanumeric, typically 8-15 chars)
//     for (let i = parts.length - 1; i >= 0; i--) {
//       const segment = parts[i];
//       // ASIN-like identifier: alphanumeric, typically 8-15 characters
//       if (/^[a-zA-Z0-9]{8,15}$/.test(segment)) {
//         return segment;
//       }
//     }

//     // Fallback: return the last part
//     return parts[parts.length - 1] || cleanPart;
//   } catch (error) {
//     console.error("Error extracting ASIN:", error);
//     return null;
//   }
// };
export const extractASINFromURL = (url) => {
  try {
    const urlObj = new URL(url);

    // Get last segment of pathname
    const pathParts = urlObj.pathname.split("/").filter(Boolean);
    const lastSegment = pathParts[pathParts.length - 1];

    // Attach query params if present
    const fullASIN = lastSegment + (urlObj.search || "");

    return fullASIN;
  } catch (error) {
    console.error("Error extracting ASIN:", error);
    return null;
  }
};


export default api;
