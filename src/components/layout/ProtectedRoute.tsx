import { Navigate, Outlet, useLocation } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Role } from '../../types';

interface ProtectedRouteProps {
  allowedRoles?: Role[];
}

export function ProtectedRoute({ allowedRoles }: ProtectedRouteProps) {
  const { user, profile, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles && profile) {
    if (!allowedRoles.includes(profile.role)) {
      // Redirect to appropriate dashboard if they try to access unauthorized role route
      switch (profile.role) {
        case 'student':
          return <Navigate to="/student/dashboard" replace />;
        case 'coordinator':
          return <Navigate to="/coordinator/dashboard" replace />;
        case 'admin':
          return <Navigate to="/admin/dashboard" replace />;
        default:
          return <Navigate to="/login" replace />;
      }
    }
  }

  return <Outlet />;
}
