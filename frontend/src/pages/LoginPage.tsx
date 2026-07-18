import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useLocation, useNavigate } from "react-router";

import { AuthLayout } from "../components/layout/AuthLayout";
import { loginUser } from "../features/auth/api/auth-api";
import {
  loginSchema,
  type LoginFormValues,
} from "../features/auth/schemas/login-schema";

interface ApiErrorResponse {
  detail?: string;
}

interface LoginNavigationState {
  registrationMessage?: string;
  registeredEmail?: string;
}

export function LoginPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const navigationState = location.state as LoginNavigationState | null;

  const [formError, setFormError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: navigationState?.registeredEmail ?? "",
      password: "",
    },
  });

  async function onSubmit(values: LoginFormValues) {
    setFormError(null);

    try {
      await loginUser({
        email: values.email.trim().toLowerCase(),
        password: values.password,
      });

      navigate("/dashboard", {
        replace: true,
      });
    } catch (error: unknown) {
      if (axios.isAxiosError<ApiErrorResponse>(error)) {
        if (error.response?.status === 403) {
          setFormError("Your account is currently disabled.");

          return;
        }

        setFormError(
          error.response?.data?.detail ??
            "We could not sign you in. Please try again.",
        );

        return;
      }

      setFormError("We could not sign you in. Please try again.");
    }
  }

  return (
    <AuthLayout>
      <h1 className="text-3xl font-bold tracking-tight">Welcome back</h1>

      <p className="mt-2 text-sm text-slate-400">
        Sign in to access your SentinelAI workspace.
      </p>

      {navigationState?.registrationMessage ? (
        <div
          className="mt-6 rounded-lg border border-emerald-800 bg-emerald-950/50 p-3 text-sm text-emerald-200"
          role="status"
        >
          {navigationState.registrationMessage}
        </div>
      ) : null}

      <form
        className="mt-8 space-y-5"
        noValidate
        onSubmit={handleSubmit(onSubmit)}
      >
        {formError ? (
          <div
            className="rounded-lg border border-red-800 bg-red-950/50 p-3 text-sm text-red-200"
            role="alert"
          >
            {formError}
          </div>
        ) : null}

        <div>
          <label
            className="mb-2 block text-sm font-medium"
            htmlFor="email"
          >
            Email address
          </label>

          <input
            autoComplete="email"
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 outline-none focus:border-cyan-400"
            id="email"
            type="email"
            {...register("email")}
          />

          {errors.email ? (
            <p className="mt-2 text-sm text-red-300">
              {errors.email.message}
            </p>
          ) : null}
        </div>

        <div>
          <label
            className="mb-2 block text-sm font-medium"
            htmlFor="password"
          >
            Password
          </label>

          <input
            autoComplete="current-password"
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 outline-none focus:border-cyan-400"
            id="password"
            type="password"
            {...register("password")}
          />

          {errors.password ? (
            <p className="mt-2 text-sm text-red-300">
              {errors.password.message}
            </p>
          ) : null}
        </div>

        <button
          className="w-full rounded-lg bg-cyan-500 px-4 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={isSubmitting}
          type="submit"
        >
          {isSubmitting ? "Signing in..." : "Sign in"}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate-400">
        Do not have an account?{" "}
        <Link
          className="font-medium text-cyan-400 hover:text-cyan-300"
          to="/register"
        >
          Create one
        </Link>
      </p>
    </AuthLayout>
  );
}
