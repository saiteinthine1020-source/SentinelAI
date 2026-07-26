export function AuthLoadingScreen() {
  return (
    <main className="grid min-h-screen place-items-center bg-slate-950 px-4 text-slate-100">
      <div
        className="text-center"
        role="status"
        aria-live="polite"
      >
        <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-slate-700 border-t-cyan-400" />

        <p className="mt-4 text-sm text-slate-400">
          Checking your session...
        </p>
      </div>
    </main>
  );
}