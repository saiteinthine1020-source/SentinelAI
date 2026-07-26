import {
  Navigate,
  Route,
  Routes,
} from "react-router";

import { ProtectedRoute } from "../../features/auth/components/ProtectedRoute";
import { PublicOnlyRoute } from "../../features/auth/components/PublicOnlyRoute";
import { DashboardPage } from "../../pages/DashboardPage";
import { LoginPage } from "../../pages/LoginPage";
import { NotFoundPage } from "../../pages/NotFoundPage";
import { RegisterPage } from "../../pages/RegisterPage";

export function AppRouter() {
  return (
    <Routes>
      <Route element={<PublicOnlyRoute />}>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/register"
          element={<RegisterPage />}
        />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route
          path="/dashboard"
          element={<DashboardPage />}
        />
      </Route>

      <Route
        path="/"
        element={<Navigate replace to="/dashboard" />}
      />

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}