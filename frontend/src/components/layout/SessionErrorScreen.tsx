export function SessionErrorScreen() {
  return (
    <main className="grid min-h-screen place-items-center bg-slate-950 px-4 text-slate-100">
      <section className="max-w-md text-center">
        <h1 className="text-2xl font-bold">
          Session check unavailable
        </h1>

        <p className="mt-3 text-slate-400">
          SentinelAI could not verify your session. Check the
          backend service and try again.
        </p>

        <button
          className="mt-6 rounded-lg bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400"
          onClick={() => window.location.reload()}
          type="button"
        >
          Try again
        </button>
      </section>
    </main>
  );
}
