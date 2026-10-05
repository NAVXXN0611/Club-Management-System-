import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../../components/ui/button';

export default function AdminDashboard() {
  const { profile, signOut } = useAuth();

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Admin Dashboard</h1>
        <Button onClick={signOut} variant="outline" className="border-red-500 text-red-500 hover:bg-red-50">
          Logout
        </Button>
      </div>
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h2 className="text-xl font-semibold mb-4">Welcome back, {profile?.full_name} 👋</h2>
        <p className="text-gray-600">Your role: {profile?.role}</p>
        <div className="mt-8 space-y-4 text-gray-500 italic">
          <p>System Overview (Coming soon)</p>
          <p>Manage Clubs (Coming soon)</p>
          <p>Manage Users (Coming soon)</p>
        </div>
      </div>
    </div>
  );
}
