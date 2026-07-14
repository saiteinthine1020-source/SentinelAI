import { Link } from "react-router";

import { AuthLayout } from "../components/layout/AuthLayout";

export function RegisterPage() {
  return (
    <AuthLayout>
      <h1 className="text-3xl font-bold tracking-tight">
        Create your account
      </h1>

      <p className="mt-2 text-sm text-slate-400">
        Start building your secure observability workspace.
      </p>

      <div className="mt-8 rounded-xl border border-dashed border-slate-700 p-6 text-center">
        <p className="text-sm text-slate-400">
          The registration form will be implemented in the registration
          feature issue.
        </p>
      </div>

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