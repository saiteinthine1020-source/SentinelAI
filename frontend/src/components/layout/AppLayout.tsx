import type { ReactNode } from "react";
import { useNavigate } from "react-router";

import { useAuth } from "../../features/auth/hooks/use-auth";

interface AppLayoutProps {
  children: ReactNode;
}

export function AppLayout({
  children,
}: AppLayoutProps) {
  const navigate = useNavigate();

  const {
    user,
    logout,
    isLoggingOut,
  } = useAuth();

  async function handleLogout() {
    const result = await logout();

    navigate("/login", {
      replace: true,
      state: {
        logoutMessage: result.serverConfirmed
          ? "You have been signed out."
          : "You have been signed out locally. The server could not be reached.",
      },
    });
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/80">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4">
          <p className="font-semibold tracking-wide text-cyan-400">
            SentinelAI
          </p>

          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium">
                {user?.username}
              </p>

              <p className="text-xs text-slate-500">
                Phase 1 — Authentication MVP
              </p>
            </div>

            <button
              className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200 hover:border-cyan-400 hover:text-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
              disabled={isLoggingOut}
              onClick={handleLogout}
              type="button"
            >
              {isLoggingOut
                ? "Signing out..."
                : "Logout"}
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-10">
        {children}
      </main>
    </div>
  );
}
