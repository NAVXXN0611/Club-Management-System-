import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getClubBySlug } from '../services/clubs';
import { getClubEvents, registerForEvent } from '../services/events';
import { getClubAnnouncements } from '../services/announcements';
import { supabase } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import type { Club, Event, Announcement } from '../types';
import {
  Sun,
  Moon,
  ArrowLeft,
  Calendar,
  Clock,
  MapPin,
  Users,
  Mail,
  CheckCircle,
  Clock3,
  Send
} from 'lucide-react';

export default function ClubDetails() {
  const { slug } = useParams<{ slug: string }>();
  const { user, profile } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const [club, setClub] = useState<Club | null>(null);
  const [events, setEvents] = useState<Event[]>([]);
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);
  const [membershipStatus, setMembershipStatus] = useState<string | null>(null);
  const [registeredIds, setRegisteredIds] = useState<Set<string>>(new Set());
  const [joining, setJoining] = useState(false);
  const [registeringId, setRegisteringId] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    getClubBySlug(slug)
      .then(async (c) => {
        setClub(c);
        if (c) {
          const [evData, annData] = await Promise.all([
            getClubEvents(c.id).catch(() => []),
            getClubAnnouncements(c.id).catch(() => [])
          ]);
          setEvents(evData);
          setAnnouncements(annData);
          if (user) {
            const { data: mem } = await supabase
              .from('club_memberships')
              .select('status')
              .eq('student_id', user.id)
              .eq('club_id', c.id)
              .single();
            if (mem) setMembershipStatus((mem as any).status);
            const { data: regs } = await supabase
              .from('event_registrations')
              .select('event_id')
              .eq('student_id', user.id);
            if (regs) setRegisteredIds(new Set((regs as any[]).map((r) => r.event_id)));
          }
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [slug, user]);

  const handleJoin = async () => {
    if (!user || !club) return;
    setJoining(true);
    try {
      const { error } = await supabase
        .from('club_memberships')
        .insert({ student_id: user.id, club_id: club.id, status: 'pending' });
      if (error) throw error;
      setMembershipStatus('pending');

      // Compose email draft to faculty coordinator
      const facultyEmail = club.contact_email || 'coordinator@college.edu';
      const subject = encodeURIComponent(`Application to Join ${club.name}`);
      const body = encodeURIComponent(
        `Dear Professor (${club.faculty_coordinator || 'Faculty In-Charge'}),\n\n` +
        `I have submitted my membership request for ${club.name} via the CCMS portal.\n` +
        `Applicant: ${profile?.full_name || 'Student'}\n` +
        `Department: ${profile?.department || 'Engineering'}\n\n` +
        `I look forward to contributing to upcoming sessions.`
      );
      window.open(`mailto:${facultyEmail}?subject=${subject}&body=${body}`, '_blank');
    } catch (e: any) {
      alert(e.message || 'Error joining club');
    } finally {
      setJoining(false);
    }
  };

  const handleRegister = async (eventId: string) => {
    if (!user) return;
    setRegisteringId(eventId);
    try {
      await registerForEvent(eventId, user.id);
      setRegisteredIds((prev) => new Set([...prev, eventId]));
    } catch (e: any) {
      alert(e.message || 'Error registering');
    } finally {
      setRegisteringId(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-purple-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!club) {
    return (
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex items-center justify-center text-center p-6">
        <div>
          <p className="text-xl font-bold text-slate-900 dark:text-slate-100 mb-2">Club not found</p>
          <Link to="/clubs" className="text-purple-600 dark:text-purple-400 font-semibold hover:underline text-sm">
            &larr; Back to Clubs
          </Link>
        </div>
      </div>
    );
  }

  const today = new Date().toISOString().split('T')[0];
  const upcomingEvents = events.filter((e) => e.event_date >= today);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-200">
      {/* Top Bar */}
      <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur border-b border-slate-200 dark:border-slate-800 px-6 py-4 sticky top-0 z-40">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <Link
            to="/clubs"
            className="inline-flex items-center gap-1.5 text-xs sm:text-sm font-semibold text-purple-600 dark:text-purple-400 hover:underline"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Clubs Directory
          </Link>

          <button
            onClick={toggleTheme}
            aria-label="Toggle theme"
            className="p-2 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
          </button>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10">
        {/* Club hero card */}
        <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm mb-8">
          <div className="bg-gradient-to-r from-purple-700 via-indigo-700 to-slate-900 h-24 w-full" />
          <div className="p-6 sm:p-8 -mt-12">
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-6">
              <div className="flex items-center gap-4">
                <div className="w-20 h-20 rounded-2xl bg-white dark:bg-slate-800 border-2 border-purple-300 dark:border-purple-700 shadow-md flex items-center justify-center text-3xl font-bold text-purple-700 dark:text-purple-300">
                  {club.name.charAt(0)}
                </div>
                <div>
                  <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
                    {club.name}
                  </h1>
                  <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                    Faculty Coordinator: {club.faculty_coordinator || 'Assigned Lead'}
                  </p>
                </div>
              </div>

              {/* Action / Status Button */}
              <div>
                {membershipStatus === 'approved' ? (
                  <span className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-emerald-100 dark:bg-emerald-950/70 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 text-xs font-bold">
                    <CheckCircle className="w-4 h-4" />
                    Official Member
                  </span>
                ) : membershipStatus === 'pending' ? (
                  <span className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-amber-100 dark:bg-amber-950/70 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800 text-xs font-bold">
                    <Clock3 className="w-4 h-4" />
                    Application Pending Review
                  </span>
                ) : (
                  <button
                    onClick={handleJoin}
                    disabled={joining}
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs sm:text-sm shadow-md transition-colors"
                  >
                    <Send className="w-4 h-4" />
                    {joining ? 'Submitting...' : 'Apply to Join & Email Faculty'}
                  </button>
                )}
              </div>
            </div>

            <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed mb-6">
              {club.description || 'Welcome to our campus club. Join us to learn, collaborate, and build projects.'}
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800 text-xs">
              <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300">
                <Mail className="w-4 h-4 text-purple-600 dark:text-purple-400 shrink-0" />
                <span>Contact Email: {club.contact_email || 'coordinator@college.edu'}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300">
                <Users className="w-4 h-4 text-purple-600 dark:text-purple-400 shrink-0" />
                <span>Status: Active Academic Year 2026-27</span>
              </div>
            </div>
          </div>
        </div>

        {/* Club Events & Activity Timetable */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              Upcoming Activities &amp; Sessions
            </h2>
            <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">
              {upcomingEvents.length} scheduled
            </span>
          </div>

          {/* Announcements section */}
          {announcements.length > 0 && (
            <div className="space-y-4 pt-4">
              <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                <Mail className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                Latest Announcements
              </h2>
              <div className="space-y-3">
                {announcements.map((ann) => (
                  <div key={ann.id} className="bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
                    <h3 className="font-bold text-sm text-slate-900 dark:text-slate-100 mb-1">{ann.title}</h3>
                    <p className="text-xs text-slate-600 dark:text-slate-400">{ann.content}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {upcomingEvents.length === 0 ? (
            <div className="p-8 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 text-xs sm:text-sm">
              No sessions scheduled currently. Check back soon or view the general activity timetable.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {upcomingEvents.map((ev) => (
                <div
                  key={ev.id}
                  className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between"
                >
                  <div>
                    <span className="text-xs font-bold px-2 py-0.5 rounded-md bg-purple-100 dark:bg-purple-950/70 text-purple-700 dark:text-purple-300 mb-2 inline-block">
                      {ev.event_date}
                    </span>
                    <h3 className="font-bold text-base text-slate-900 dark:text-slate-100 mb-1">
                      {ev.title}
                    </h3>
                    <p className="text-xs text-slate-600 dark:text-slate-400 mb-3 line-clamp-2">
                      {ev.description}
                    </p>
                    <div className="space-y-1 text-xs text-slate-500 dark:text-slate-400 mb-4">
                      <div className="flex items-center gap-1.5">
                        <Clock className="w-3.5 h-3.5" />
                        <span>{ev.start_time} - {ev.end_time}</span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <MapPin className="w-3.5 h-3.5" />
                        <span>{ev.venue}</span>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => handleRegister(ev.id)}
                    disabled={registeredIds.has(ev.id) || registeringId === ev.id}
                    className={`w-full py-2 px-3 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors ${
                      registeredIds.has(ev.id)
                        ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300'
                        : 'bg-purple-600 hover:bg-purple-500 text-white'
                    }`}
                  >
                    {registeredIds.has(ev.id) ? (
                      <>
                        <CheckCircle className="w-4 h-4" />
                        Seat Confirmed
                      </>
                    ) : (
                      'Reserve Seat / RSVP'
                    )}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
