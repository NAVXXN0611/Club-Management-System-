import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import type { Role } from '../../types';

interface ProtectedRouteProps {
  allowedRoles?: Role[];
}

export function ProtectedRoute({ allowedRoles }: ProtectedRouteProps) {
  const { user, profile, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-purple-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  // Not authenticated
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If a role is required, we MUST have a verified profile loaded
  if (allowedRoles) {
    if (!profile) {
      return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col items-center justify-center p-6 text-center">
          <div className="w-8 h-8 border-2 border-purple-600 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-sm text-slate-600 dark:text-slate-300">Verifying authorization permissions...</p>
        </div>
      );
    }

    if (!allowedRoles.includes(profile.role)) {
      // Redirect to appropriate dashboard based on actual verified role
      if (profile.role === 'coordinator' || profile.role === 'admin') {
        return <Navigate to="/coordinator/dashboard" replace />;
      }
      return <Navigate to="/student/dashboard" replace />;
    }
  }

  return <Outlet />;
}
