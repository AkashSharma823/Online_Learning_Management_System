import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { api } from "./api";
import type { User } from "./types";

type AuthCtx = {
  user: User | null;
  login: (identifier: string, password: string) => Promise<User | null>;
  logout: () => void;
  register: (data: { email: string; password: string; first_name?: string; last_name?: string }) => Promise<boolean>;
};

const C = createContext<AuthCtx>({
  user: null,
  login: async () => null,
  logout: () => {},
  register: async () => false,
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    try {
      return JSON.parse(localStorage.getItem("heartify_user") || "null") as User | null;
    } catch {
      return null;
    }
  });

  useEffect(() => {
    if (user) localStorage.setItem("heartify_user", JSON.stringify(user));
    else localStorage.removeItem("heartify_user");
  }, [user]);

  async function login(identifier: string, password: string): Promise<User | null> {
    try {
      const response = await api.post("/auth/login/", { username: identifier, password });
      const loggedInUser = response.data.user as User;
      localStorage.setItem("heartify_access", response.data.access);
      localStorage.setItem("heartify_refresh", response.data.refresh);
      setUser(loggedInUser);
      return loggedInUser;
    } catch {
      return null;
    }
  }

  async function register(data: { email: string; password: string; first_name?: string; last_name?: string }) {
    try {
      const response = await api.post("/auth/register/", data);
      return response.status === 201;
    } catch {
      return false;
    }
  }

  function logout() {
    localStorage.removeItem("heartify_access");
    localStorage.removeItem("heartify_refresh");
    setUser(null);
  }

  return <C.Provider value={{ user, login, logout, register }}>{children}</C.Provider>;
}

export const useAuth = () => useContext(C);
