import { apiClient } from "../../../lib/api-client";
import type { LoginFormValues } from "../schemas/login-schema";
import type { RegisterFormValues } from "../schemas/register-schema";
import type { PublicUser } from "../types/auth";

interface LoginResponse {
  message: string;
}

type RegisterRequest = Omit<RegisterFormValues, "confirmPassword">;

export async function registerUser(
  values: RegisterFormValues,
): Promise<PublicUser> {
  const request: RegisterRequest = {
    username: values.username,
    email: values.email,
    password: values.password,
  };

  const response = await apiClient.post<PublicUser>(
    "/api/v1/auth/register",
    request,
  );

  return response.data;
}

export async function loginUser(
  values: LoginFormValues,
): Promise<LoginResponse> {
  const response = await apiClient.post<LoginResponse>(
    "/api/v1/auth/login",
    values,
  );

  return response.data;
}

export async function getCurrentUser(): Promise<PublicUser> {
  const response = await apiClient.get<PublicUser>("/api/v1/auth/me");

  return response.data;
}

export async function logoutUser(): Promise<void> {
  await apiClient.post("/api/v1/auth/logout");
}