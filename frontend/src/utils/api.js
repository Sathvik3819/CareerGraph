const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const authHeaders = () => ({
  Authorization: `Bearer ${localStorage.getItem("access_token") || ""}`,
});

export const apiFetch = (path, options = {}) => {
  return fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      ...options.headers,
      ...authHeaders(),
    },
  });
};

export { API_URL };