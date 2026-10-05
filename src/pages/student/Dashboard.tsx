import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../../components/ui/button';
import { Link } from 'react-router-dom';

export default function StudentDashboard() {
  const { profile, signOut } = useAuth();

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Student Dashboard</h1>
        <Button onClick={signOut} variant="outline" className="border-red-500 text-red-500 hover:bg-red-50">
          Logout
        </Button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 md:col-span-3">
          <h2 className="text-xl font-semibold mb-2">Welcome back, {profile?.full_name} 👋</h2>
          <p className="text-gray-600 mb-4">Discover clubs, register for events, and track your attendance.</p>
          <Link to="/clubs">
            <Button>Explore Clubs</Button>
          </Link>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="font-semibold text-lg mb-4">My Clubs</h3>
          <p className="text-sm text-gray-500 italic">No clubs joined yet.</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="font-semibold text-lg mb-4">Upcoming Events</h3>
          <p className="text-sm text-gray-500 italic">No registered events.</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="font-semibold text-lg mb-4">My Attendance</h3>
          <p className="text-sm text-gray-500 italic">Overall: 0%</p>
        </div>
      </div>
    </div>
  );
}
