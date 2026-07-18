import { Link, useLocation } from "react-router";

import { AuthLayout } from "../components/layout/AuthLayout";

export function LoginPage() {
  const location = useLocation();

  const navigationState = location.state as
    | {
        registrationMessage?: string;
        registeredEmail?: string;
      }
    | null;

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

      <div className="mt-8 rounded-xl border border-dashed border-slate-700 p-6 text-center">
        <p className="text-sm text-slate-400">
          The login form will be implemented in the authentication feature
          issue.
        </p>
      </div>

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
