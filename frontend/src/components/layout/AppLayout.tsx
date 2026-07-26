import type { ReactNode } from "react";

import { useAuth } from "../../features/auth/hooks/use-auth";

interface AppLayoutProps {
  children: ReactNode;
}

export function AppLayout({
  children,
}: AppLayoutProps) {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/80">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4">
          <p className="font-semibold tracking-wide text-cyan-400">
            SentinelAI
          </p>

          <div className="text-right">
            <p className="text-sm font-medium">
              {user?.username}
            </p>
            <p className="text-xs text-slate-500">
              Phase 1 — Authentication MVP
            </p>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-10">
        {children}
      </main>
    </div>
  );
}