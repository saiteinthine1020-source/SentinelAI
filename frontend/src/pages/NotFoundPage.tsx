import { Link } from "react-router";

export function NotFoundPage() {
  return (
    <main className="grid min-h-screen place-items-center bg-slate-950 px-4 text-slate-100">
      <section className="text-center">
        <p className="text-sm font-semibold tracking-[0.2em] text-cyan-400 uppercase">
          404
        </p>

        <h1 className="mt-3 text-4xl font-bold">Page not found</h1>

        <p className="mt-4 text-slate-400">
          The requested SentinelAI page does not exist.
        </p>

        <Link
          className="mt-8 inline-flex rounded-lg bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400"
          to="/login"
        >
          Return to SentinelAI
        </Link>
      </section>
    </main>
  );
}