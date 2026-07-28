import axios from "axios";
import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  getCurrentUser,
  logoutUser,
} from "../api/auth-api";
import type {
  AuthContextValue,
  AuthState,
  PublicUser,
} from "../types/auth";
import { AuthContext } from "./AuthContext";

interface AuthProviderProps {
  children: ReactNode;
}

const initialState: AuthState = {
  status: "loading",
  user: null,
};

export function AuthProvider({ children }: AuthProviderProps) {
  const [authState, setAuthState] =
    useState<AuthState>(initialState);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const refreshSession = useCallback(async () => {
    setAuthState({
      status: "loading",
      user: null,
    });

    try {
      const user = await getCurrentUser();

      setAuthState({
        status: "authenticated",
        user,
      });
    } catch (error: unknown) {
      if (
        axios.isAxiosError(error) &&
        (error.response?.status === 401 ||
          error.response?.status === 403)
      ) {
        setAuthState({
          status: "unauthenticated",
          user: null,
        });

        return;
      }

      setAuthState({
        status: "error",
        user: null,
      });
    }
  }, []);

  const setAuthenticatedUser = useCallback(
    (user: PublicUser) => {
      setAuthState({
        status: "authenticated",
        user,
      });
    },
    [],
  );

  const clearSession = useCallback(() => {
    setAuthState({
      status: "unauthenticated",
      user: null,
    });
  }, []);

  const logout = useCallback(async () => {
    setIsLoggingOut(true);

    let serverConfirmed = false;

    try {
      await logoutUser();
      serverConfirmed = true;
    } catch {
      serverConfirmed = false;
    } finally {
      setAuthState({
        status: "unauthenticated",
        user: null,
      });

      setIsLoggingOut(false);
    }

    return {
      serverConfirmed,
    };
  }, []);

  useEffect(() => {
    void refreshSession();
  }, [refreshSession]);

  const value = useMemo<AuthContextValue>(
    () => ({
      ...authState,
      refreshSession,
      setAuthenticatedUser,
      clearSession,
      isLoggingOut,
      logout,
    }),
    [
      authState,
      clearSession,
      isLoggingOut,
      logout,
      refreshSession,
      setAuthenticatedUser,
    ],
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
