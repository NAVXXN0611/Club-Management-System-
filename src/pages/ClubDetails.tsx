import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getClubBySlug } from '../services/clubs';
import { supabase } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';
import { Club } from '../types';
import { Button } from '../components/ui/button';

export default function ClubDetails() {
  const { slug } = useParams<{ slug: string }>();
  const { user } = useAuth();
  const [club, setClub] = useState<Club | null>(null);
  const [loading, setLoading] = useState(true);
  const [membershipStatus, setMembershipStatus] = useState<string | null>(null);

  useEffect(() => {
    if (slug) {
      getClubBySlug(slug).then(async (c) => {
        setClub(c);
        if (user && c) {
          const { data } = await supabase
            .from('club_memberships')
            .select('status')
            .eq('student_id', user.id)
            .eq('club_id', c.id)
            .single();
          if (data) setMembershipStatus(data.status);
        }
        setLoading(false);
      }).catch(console.error);
    }
  }, [slug, user]);

  const handleJoin = async () => {
    if (!user || !club) return;
    try {
      const { error } = await supabase.from('club_memberships').insert({
        student_id: user.id,
        club_id: club.id,
        status: 'pending'
      });
      if (error) throw error;
      setMembershipStatus('pending');
      alert('Application sent successfully!');
    } catch (e: any) {
      alert(e.message || 'Error joining club');
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (!club) return <div className="p-8 text-center text-red-500">Club not found</div>;

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <Link to="/clubs" className="text-primary hover:underline mb-8 block">&larr; Back to Clubs</Link>
      <div className="bg-white rounded-lg shadow-sm border p-8">
        <h1 className="text-4xl font-bold mb-4">{club.name}</h1>
        <p className="text-gray-600 mb-8">{club.description}</p>

        <div className="grid grid-cols-2 gap-4 mb-8">
          <div>
            <h3 className="font-semibold text-gray-700">Faculty Coordinator</h3>
            <p>{club.faculty_coordinator || 'N/A'}</p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-700">Contact Email</h3>
            <p>{club.contact_email || 'N/A'}</p>
          </div>
        </div>

        {user ? (
          <div>
            {!membershipStatus && (
              <Button onClick={handleJoin}>Join Club</Button>
            )}
            {membershipStatus === 'pending' && (
              <Button variant="outline" disabled className="bg-yellow-50 text-yellow-700 border-yellow-200">Application Pending</Button>
            )}
            {membershipStatus === 'approved' && (
              <Button variant="outline" disabled className="bg-green-50 text-green-700 border-green-200">You are a Member</Button>
            )}
          </div>
        ) : (
          <p className="text-sm text-gray-500"><Link to="/login" className="text-primary hover:underline">Log in</Link> to join this club.</p>
        )}
      </div>
    </div>
  );
}
