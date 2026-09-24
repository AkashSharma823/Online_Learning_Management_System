import axios from "axios";

export const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

export const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("heartify_access");
  if (token) {
    config.headers.set("Authorization", `Bearer ${token}`);
  }
  return config;
});

export async function getData<T = unknown>(url: string, fallback: T): Promise<T> {
  try {
    const response = await api.get(url);
    return (response.data?.results ?? response.data) as T;
  } catch {
    return fallback;
  }
}
