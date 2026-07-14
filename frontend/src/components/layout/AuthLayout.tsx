import type { ReactNode } from "react";

interface AuthLayoutProps {
  children: ReactNode;
}

export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <main className="min-h-screen bg-slate-950 px-4 py-12 text-slate-100">
      <div className="mx-auto flex min-h-[calc(100vh-6rem)] max-w-md items-center">
        <section className="w-full rounded-2xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl shadow-black/20">
          <div className="mb-8">
            <p className="text-sm font-semibold tracking-[0.2em] text-cyan-400 uppercase">
              SentinelAI
            </p>
          </div>

          {children}
        </section>
      </div>
    </main>
  );
}