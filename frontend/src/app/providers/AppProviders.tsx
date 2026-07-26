import type { ReactNode } from "react";
import { BrowserRouter } from "react-router";

import { AuthProvider } from "../../features/auth/context/AuthProvider";

interface AppProvidersProps {
  children: ReactNode;
}

export function AppProviders({
  children,
}: AppProvidersProps) {
  return (
    <BrowserRouter>
      <AuthProvider>{children}</AuthProvider>
    </BrowserRouter>
  );
}