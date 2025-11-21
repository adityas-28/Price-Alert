// API Configuration
let API_BASE_URL = "http://localhost:8000";

try {
  if (import.meta && import.meta.env && import.meta.env.VITE_API_BASE_URL) {
    API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
  }
} catch (error) {
  console.warn(
    "Could not read VITE_API_BASE_URL from env, using default:",
    API_BASE_URL
  );
}

export { API_BASE_URL };
