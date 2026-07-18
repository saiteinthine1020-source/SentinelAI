import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router";

import { AuthLayout } from "../components/layout/AuthLayout";
import { registerUser } from "../features/auth/api/auth-api";
import {
  registerSchema,
  type RegisterFormValues,
} from "../features/auth/schemas/register-schema";

interface ApiErrorResponse {
  detail?: string;
}

export function RegisterPage() {
  const navigate = useNavigate();
  const [formError, setFormError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });

  async function onSubmit(values: RegisterFormValues) {
    setFormError(null);

    try {
      await registerUser(values);

      navigate("/login", {
        replace: true,
        state: {
          registrationMessage:
            "Account created successfully. Sign in to continue.",
          registeredEmail: values.email.trim().toLowerCase(),
        },
      });
    } catch (error: unknown) {
      if (axios.isAxiosError<ApiErrorResponse>(error)) {
        setFormError(
          error.response?.data?.detail ??
            "We could not create your account. Please try again.",
        );

        return;
      }

      setFormError(
        "We could not create your account. Please try again.",
      );
    }
  }

  return (
    <AuthLayout>
      <h1 className="text-3xl font-bold tracking-tight">
        Create your account
      </h1>

      <p className="mt-2 text-sm text-slate-400">
        Start building your secure observability workspace.
      </p>

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
            htmlFor="username"
          >
            Username
          </label>

          <input
            autoComplete="username"
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 outline-none focus:border-cyan-400"
            id="username"
            type="text"
            {...register("username")}
          />

          {errors.username ? (
            <p className="mt-2 text-sm text-red-300">
              {errors.username.message}
            </p>
          ) : null}
        </div>

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
            autoComplete="new-password"
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

          <p className="mt-2 text-xs leading-5 text-slate-500">
            Use 12–128 characters with uppercase, lowercase,
            numeric, and special characters.
          </p>
        </div>

        <div>
          <label
            className="mb-2 block text-sm font-medium"
            htmlFor="confirmPassword"
          >
            Confirm password
          </label>

          <input
            autoComplete="new-password"
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 outline-none focus:border-cyan-400"
            id="confirmPassword"
            type="password"
            {...register("confirmPassword")}
          />

          {errors.confirmPassword ? (
            <p className="mt-2 text-sm text-red-300">
              {errors.confirmPassword.message}
            </p>
          ) : null}
        </div>

        <button
          className="w-full rounded-lg bg-cyan-500 px-4 py-3 font-semibold text-slate-950 hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={isSubmitting}
          type="submit"
        >
          {isSubmitting ? "Creating account..." : "Create account"}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate-400">
        Already have an account?{" "}
        <Link
          className="font-medium text-cyan-400 hover:text-cyan-300"
          to="/login"
        >
          Sign in
        </Link>
      </p>
    </AuthLayout>
  );
}