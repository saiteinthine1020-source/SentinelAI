import { Navigate, Outlet } from "react-router";

import { AuthLoadingScreen } from "../../../components/layout/AuthLoadingScreen";
import { SessionErrorScreen } from "../../../components/layout/SessionErrorScreen";
import { useAuth } from "../hooks/use-auth";

export function PublicOnlyRoute() {
  const { status } = useAuth();

  if (status === "loading") {
    return <AuthLoadingScreen />;
  }

  if (status === "error") {
    return <SessionErrorScreen />;
  }

  if (status === "authenticated") {
    return <Navigate replace to="/dashboard" />;
  }

  return <Outlet />;
}
