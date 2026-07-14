import { AppLayout } from "../components/layout/AppLayout";

export function DashboardPage() {
  return (
    <AppLayout>
      <section className="rounded-2xl border border-slate-800 bg-slate-900 p-8">
        <p className="text-sm font-medium text-cyan-400">
          Development foundation
        </p>

        <h1 className="mt-2 text-3xl font-bold tracking-tight">
          SentinelAI frontend is initialized
        </h1>

        <p className="mt-4 max-w-2xl text-slate-400">
          React, TypeScript, Vite, Tailwind CSS, React Router, Axios, React
          Hook Form, and Zod are now available.
        </p>

        <div className="mt-8 rounded-xl border border-dashed border-slate-700 p-6">
          <p className="text-sm text-slate-400">
            Authentication protection and user data will be added in later
            Phase 1 issues.
          </p>
        </div>
      </section>
    </AppLayout>
  );
}