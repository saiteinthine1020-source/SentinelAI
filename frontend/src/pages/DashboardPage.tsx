import { AppLayout } from "../components/layout/AppLayout";
import { useAuth } from "../features/auth/hooks/use-auth";

export function DashboardPage() {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <AppLayout>
      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-8">
        <p className="text-sm font-medium text-cyan-400">
          Authenticated session
        </p>

        <h1 className="mt-2 text-3xl font-bold tracking-tight">
          Welcome to SentinelAI, {user.username}
        </h1>

        <p className="mt-4 max-w-2xl text-slate-400">
          Your authentication cookie was validated by the
          backend, and this protected route is now available.
        </p>
      </section>

      <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-8">
        <h2 className="text-xl font-semibold">
          Account information
        </h2>

        <dl className="mt-6 grid gap-5 sm:grid-cols-2">
          <div>
            <dt className="text-sm text-slate-500">
              Username
            </dt>
            <dd className="mt-1 font-medium">
              {user.username}
            </dd>
          </div>

          <div>
            <dt className="text-sm text-slate-500">
              Email
            </dt>
            <dd className="mt-1 font-medium">
              {user.email}
            </dd>
          </div>

          <div>
            <dt className="text-sm text-slate-500">
              Status
            </dt>
            <dd className="mt-1 font-medium text-emerald-400">
              {user.is_active ? "Active" : "Inactive"}
            </dd>
          </div>

          <div>
            <dt className="text-sm text-slate-500">
              Created
            </dt>
            <dd className="mt-1 font-medium">
              {new Date(user.created_at).toLocaleString()}
            </dd>
          </div>
        </dl>
      </section>
    </AppLayout>
  );
}