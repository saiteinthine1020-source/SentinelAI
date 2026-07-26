export interface PublicUser {
  id: string;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export type AuthStatus =
  | "loading"
  | "authenticated"
  | "unauthenticated"
  | "error";

export interface AuthState {
  status: AuthStatus;
  user: PublicUser | null;
}

export interface AuthContextValue extends AuthState {
  refreshSession: () => Promise<void>;
  setAuthenticatedUser: (user: PublicUser) => void;
  clearSession: () => void;
}