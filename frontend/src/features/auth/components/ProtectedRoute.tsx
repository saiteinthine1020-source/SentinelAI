import { Navigate, Outlet, useLocation } from "react-router";

import { AuthLoadingScreen } from "../../../components/layout/AuthLoadingScreen";
import { SessionErrorScreen } from "../../../components/layout/SessionErrorScreen";
import { useAuth } from "../hooks/use-auth";

export function ProtectedRoute() {
  const location = useLocation();
  const { status } = useAuth();

  if (status === "loading") {
    return <AuthLoadingScreen />;
  }

  if (status === "error") {
    return <SessionErrorScreen />;
  }

  if (status !== "authenticated") {
    return (
      <Navigate
        replace
        state={{
          sessionMessage:
            "Please sign in to access that page.",
          from: location.pathname,
        }}
        to="/login"
      />
    );
  }

  return <Outlet />;
}
