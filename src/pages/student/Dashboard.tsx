import { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Navbar } from '../../components/layout/Navbar';
import { getMyMemberships, applyForClubMembership } from '../../services/memberships';
import { getMyEventRegistrations, registerForEvent, getAllUpcomingEvents } from '../../services/events';
import { getClubs } from '../../services/clubs';
import { getStudentAttendance } from '../../services/attendance';
import type { Club, Event, ClubMembership, Attendance } from '../../types';
import {
  Calendar,
  Clock,
  MapPin,
  Users,
  Compass,
  Bell,
  CheckCircle,
  Clock3,
  Award,
  Send,
  Mail,
  UserCheck,
  Search,
  Check,
  BookOpen,
  CalendarCheck2
} from 'lucide-react';

type Tab = 'timetable' | 'clubs' | 'notifications' | 'attendance';

interface TimetableItem {
  id: string;
  day: string;
  time: string;
  club: string;
  title: string;
  venue: string;
  type: string;
  capacity: number;
  facultyCoordinator: string;
  facultyEmail: string;
}

const WEEKLY_TIMETABLE: TimetableItem[] = [
  {
    id: 'tt-1',
    day: 'Monday',
    time: '04:30 PM - 06:00 PM',
    club: 'Google Developer Student Club',
    title: 'Cloud Architecture & Gemini AI Workshop',
    venue: 'Turing Computing Lab 301',
    type: 'Hands-on Lab',
    capacity: 60,
    facultyCoordinator: 'Dr. Ramesh Kumar',
    facultyEmail: 'ramesh.k@college.edu'
  },
  {
    id: 'tt-2',
    day: 'Tuesday',
    time: '05:00 PM - 06:30 PM',
    club: 'Robotics & Automation Society',
    title: 'Embedded ROS2 & Autonomous Rover Sprint',
    venue: 'Mechatronics Innovation Center',
    type: 'Hardware Sprint',
    capacity: 40,
    facultyCoordinator: 'Prof. Ananya Sen',
    facultyEmail: 'ananya.s@college.edu'
  },
  {
    id: 'tt-3',
    day: 'Wednesday',
    time: '04:00 PM - 05:30 PM',
    club: 'ACM Student Chapter',
    title: 'Competitive Programming: Graph Theory & Trees',
    venue: 'Algorithm Hall B',
    type: 'Problem Solving',
    capacity: 75,
    facultyCoordinator: 'Dr. Priya Sundaram',
    facultyEmail: 'priya.s@college.edu'
  },
  {
    id: 'tt-4',
    day: 'Thursday',
    time: '05:00 PM - 06:30 PM',
    club: 'Cyber Security & Ethical Hacking Guild',
    title: 'Capture The Flag (CTF) Web Vulnerabilities',
    venue: 'Cyber Range Lab 102',
    type: 'Security Drill',
    capacity: 45,
    facultyCoordinator: 'Prof. Vikram Malhotra',
    facultyEmail: 'vikram.m@college.edu'
  },
  {
    id: 'tt-5',
    day: 'Friday',
    time: '04:30 PM - 06:00 PM',
    club: 'Design & UI/UX Society',
    title: 'Design Systems & Figma Prototyping Critique',
    venue: 'Media Design Studio 4',
    type: 'Design Review',
    capacity: 50,
    facultyCoordinator: 'Prof. Kavita Rao',
    facultyEmail: 'kavita.r@college.edu'
  },
  {
    id: 'tt-6',
    day: 'Saturday',
    time: '10:00 AM - 01:00 PM',
    club: 'AI & Data Science Circle',
    title: 'Weekend Hackathon: Agentic Workflows with Gemini',
    venue: 'Main Auditorium & Sandbox',
    type: 'Hackathon',
    capacity: 120,
    facultyCoordinator: 'Dr. Rajesh Nambiar',
    facultyEmail: 'rajesh.n@college.edu'
  }
];

export default function StudentDashboard() {
  const { user, profile } = useAuth();
  const [activeTab, setActiveTab] = useState<Tab>('timetable');
  const [memberships, setMemberships] = useState<ClubMembership[]>([]);
  const [registrations, setRegistrations] = useState<any[]>([]);
  const [allClubs, setAllClubs] = useState<Club[]>([]);
  const [upcomingEvents, setUpcomingEvents] = useState<Event[]>([]);
  const [attendanceRecords, setAttendanceRecords] = useState<Attendance[]>([]);
  const [loading, setLoading] = useState(true);

  // Search & Filter States
  const [clubSearch, setClubSearch] = useState('');
  const [selectedDay, setSelectedDay] = useState<string>('All');
  const [rsvpSuccess, setRsvpSuccess] = useState<string | null>(null);

  // Application Modal State
  const [applyingClub, setApplyingClub] = useState<Club | null>(null);
  const [applicationMsg, setApplicationMsg] = useState('');
  const [isSubmittingApp, setIsSubmittingApp] = useState(false);
  const [appSentNotice, setAppSentNotice] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    loadDashboardData();
  }, [user]);

  const loadDashboardData = async () => {
    if (!user) return;
    setLoading(true);
    try {
      const [m, r, c, e, a] = await Promise.all([
        getMyMemberships(user.id).catch(() => []),
        getMyEventRegistrations(user.id).catch(() => []),
        getClubs().catch(() => []),
        getAllUpcomingEvents().catch(() => []),
        getStudentAttendance(user.id).catch(() => [])
      ]);
      setMemberships(m as ClubMembership[]);
      setRegistrations(r);
      setAllClubs(c as Club[]);
      setUpcomingEvents(e as Event[]);
      setAttendanceRecords(a as Attendance[]);
    } catch (err) {
      console.error('Error loading student dashboard data', err);
    } finally {
      setLoading(false);
    }
  };

  const registeredEventIds = new Set(registrations.map((r) => r.event_id));
  const memberClubIds = new Map(memberships.map((m) => [m.club_id, m.status]));

  const approvedMemberships = memberships.filter((m) => m.status === 'approved');
  const pendingMemberships = memberships.filter((m) => m.status === 'pending');

  const handleRsvpEvent = async (event: Event) => {
    if (!user) return;
    try {
      await registerForEvent(event.id, user.id);
      setRegistrations((prev) => [...prev, { event_id: event.id, events: event }]);
      setRsvpSuccess(`RSVP confirmed for "${event.title}"!`);
      setTimeout(() => setRsvpSuccess(null), 4000);
    } catch (err: any) {
      alert(err.message || 'Error registering for session');
    }
  };

  const handleApplyToClub = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || !applyingClub) return;
    setIsSubmittingApp(true);
    try {
      await applyForClubMembership(applyingClub.id, user.id);
      setMemberships((prev) => [
        ...prev,
        {
          id: 'temp-' + Date.now(),
          student_id: user.id,
          club_id: applyingClub.id,
          status: 'pending',
          applied_at: new Date().toISOString(),
          clubs: {
            name: applyingClub.name,
            slug: applyingClub.slug,
            description: applyingClub.description,
            faculty_coordinator: applyingClub.faculty_coordinator,
            contact_email: applyingClub.contact_email
          }
        }
      ]);

      // Compose email draft link to faculty coordinator
      const facultyEmail = applyingClub.contact_email || 'coordinator@college.edu';
      const subject = encodeURIComponent(`Club Joining Application: ${profile?.full_name || 'Student'} - ${applyingClub.name}`);
      const body = encodeURIComponent(
        `Dear Faculty Coordinator (${applyingClub.faculty_coordinator || 'Professor'}),\n\n` +
        `I am writing to formally submit my application to join the ${applyingClub.name}.\n\n` +
        `Applicant Details:\n` +
        `- Full Name: ${profile?.full_name || 'N/A'}\n` +
        `- College Email: ${profile?.email || 'N/A'}\n` +
        `- Department: ${profile?.department || 'Engineering'}\n` +
        `- Student ID: ${profile?.student_id || 'N/A'}\n` +
        `- Year of Study: ${profile?.year || 'Current'}\n\n` +
        `Statement of Purpose / Motivation:\n` +
        `"${applicationMsg || 'I am eager to actively participate, learn, and contribute to club sessions and projects.'}"\n\n` +
        `Thank you for your consideration.\n\n` +
        `Warm regards,\n${profile?.full_name}`
      );

      setAppSentNotice(
        `Application submitted to ${applyingClub.name}! An official email draft has been prepared for ${applyingClub.faculty_coordinator}.`
      );

      // Open mail client for the student to send mail to faculty
      window.open(`mailto:${facultyEmail}?subject=${subject}&body=${body}`, '_blank');

      setApplyingClub(null);
      setApplicationMsg('');
      setTimeout(() => setAppSentNotice(null), 6000);
    } catch (err: any) {
      alert(err.message || 'Error submitting application');
    } finally {
      setIsSubmittingApp(false);
    }
  };

  const filteredClubs = allClubs.filter((c) =>
    c.name.toLowerCase().includes(clubSearch.toLowerCase()) ||
    c.description?.toLowerCase().includes(clubSearch.toLowerCase()) ||
    c.faculty_coordinator?.toLowerCase().includes(clubSearch.toLowerCase())
  );

  const combinedTimetable: TimetableItem[] = [
    ...WEEKLY_TIMETABLE,
    ...upcomingEvents.map((ev) => ({
      id: ev.id,
      day: new Date(ev.event_date).toLocaleDateString('en-US', { weekday: 'long' }),
      time: `${ev.start_time} - ${ev.end_time}`,
      club: (ev as any).clubs?.name || 'Campus Club',
      title: ev.title,
      venue: ev.venue,
      type: 'Official Event',
      capacity: ev.capacity,
      facultyCoordinator: 'Faculty In-Charge',
      facultyEmail: 'coordinator@college.edu'
    }))
  ];

  const filteredTimetable = selectedDay === 'All'
    ? combinedTimetable
    : combinedTimetable.filter((item) => item.day.toLowerCase() === selectedDay.toLowerCase());

  const attendancePresent = attendanceRecords.filter((a) => a.status === 'present').length;
  const attendanceRate = attendanceRecords.length > 0
    ? Math.round((attendancePresent / attendanceRecords.length) * 100)
    : 100;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-200">
      <Navbar />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alerts & Notifications */}
        {rsvpSuccess && (
          <div className="mb-6 p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200 flex items-center justify-between shadow-sm animate-fade-in">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
              <span className="text-sm font-medium">{rsvpSuccess}</span>
            </div>
            <button onClick={() => setRsvpSuccess(null)} className="text-xs font-semibold hover:underline">Dismiss</button>
          </div>
        )}

        {appSentNotice && (
          <div className="mb-6 p-4 rounded-xl bg-purple-50 dark:bg-purple-950/60 border border-purple-200 dark:border-purple-800 text-purple-900 dark:text-purple-200 flex items-center justify-between shadow-sm animate-fade-in">
            <div className="flex items-center gap-3">
              <Mail className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              <span className="text-sm font-medium">{appSentNotice}</span>
            </div>
            <button onClick={() => setAppSentNotice(null)} className="text-xs font-semibold hover:underline">Dismiss</button>
          </div>
        )}

        {/* Hero Header */}
        <div className="relative rounded-2xl bg-gradient-to-r from-purple-900 via-indigo-900 to-slate-900 text-white p-8 mb-8 overflow-hidden shadow-xl border border-purple-500/20">
          <div className="absolute -top-12 -right-12 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10 max-w-3xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-400/20 text-purple-200 text-xs font-semibold mb-3 border border-purple-300/20">
              <BookOpen className="w-3.5 h-3.5 text-purple-300" />
              Student Portal &bull; {profile?.department || 'Academic Year 2026-27'}
            </div>
            <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-white mb-2">
              Welcome back, {profile?.full_name || 'Scholar'}
            </h1>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed mb-6">
              Explore campus clubs, apply directly to faculty coordinators, check weekly activity timetables, and monitor your verified attendance.
            </p>

            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => setActiveTab('timetable')}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs sm:text-sm shadow-md transition-all"
              >
                <Calendar className="w-4 h-4" />
                View Activity Timetable
              </button>
              <button
                onClick={() => setActiveTab('clubs')}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium text-xs sm:text-sm border border-white/20 backdrop-blur transition-all"
              >
                <Compass className="w-4 h-4" />
                Explore &amp; Apply to Clubs
              </button>
            </div>
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Joined Clubs</span>
              <div className="p-2 rounded-lg bg-purple-100 dark:bg-purple-950/70 text-purple-600 dark:text-purple-400">
                <Award className="w-4 h-4" />
              </div>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100">
              {loading ? '—' : approvedMemberships.length}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Active memberships</p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Pending Apps</span>
              <div className="p-2 rounded-lg bg-amber-100 dark:bg-amber-950/70 text-amber-600 dark:text-amber-400">
                <Clock3 className="w-4 h-4" />
              </div>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100">
              {loading ? '—' : pendingMemberships.length}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Awaiting faculty review</p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">RSVP Sessions</span>
              <div className="p-2 rounded-lg bg-blue-100 dark:bg-blue-950/70 text-blue-600 dark:text-blue-400">
                <CalendarCheck2 className="w-4 h-4" />
              </div>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100">
              {loading ? '—' : registrations.length}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Upcoming registered</p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Attendance</span>
              <div className="p-2 rounded-lg bg-emerald-100 dark:bg-emerald-950/70 text-emerald-600 dark:text-emerald-400">
                <UserCheck className="w-4 h-4" />
              </div>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100">
              {loading ? '—' : `${attendanceRate}%`}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Verified campus record</p>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-200 dark:border-slate-800 mb-6 gap-2 sm:gap-4 overflow-x-auto pb-1">
          <button
            onClick={() => setActiveTab('timetable')}
            className={`inline-flex items-center gap-2 pb-3 px-3 text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'timetable'
                ? 'border-purple-600 text-purple-600 dark:text-purple-400'
                : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Calendar className="w-4 h-4" />
            Club Activity Time Table
          </button>

          <button
            onClick={() => setActiveTab('clubs')}
            className={`inline-flex items-center gap-2 pb-3 px-3 text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'clubs'
                ? 'border-purple-600 text-purple-600 dark:text-purple-400'
                : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Compass className="w-4 h-4" />
            Explore &amp; Apply to Clubs
          </button>

          <button
            onClick={() => setActiveTab('notifications')}
            className={`inline-flex items-center gap-2 pb-3 px-3 text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'notifications'
                ? 'border-purple-600 text-purple-600 dark:text-purple-400'
                : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Bell className="w-4 h-4" />
            Club Notifications
          </button>

          <button
            onClick={() => setActiveTab('attendance')}
            className={`inline-flex items-center gap-2 pb-3 px-3 text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'attendance'
                ? 'border-purple-600 text-purple-600 dark:text-purple-400'
                : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <UserCheck className="w-4 h-4" />
            My Attendance &amp; Status
          </button>
        </div>

        {/* TAB 1: CLUB ACTIVITY TIME TABLE */}
        {activeTab === 'timetable' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  Weekly Club Activity Schedule
                </h2>
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                  Regular club sessions, laboratory sprints, guest lectures, and weekend hackathons.
                </p>
              </div>

              {/* Day Filter Pills */}
              <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
                {['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].map((day) => (
                  <button
                    key={day}
                    onClick={() => setSelectedDay(day)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                      selectedDay === day
                        ? 'bg-purple-600 text-white'
                        : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                    }`}
                  >
                    {day}
                  </button>
                ))}
              </div>
            </div>

            {/* Timetable Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {filteredTimetable.map((slot) => (
                <div
                  key={slot.id}
                  className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 flex flex-col justify-between hover:border-purple-300 dark:hover:border-purple-700/60 transition-all hover:shadow-md"
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-purple-100 dark:bg-purple-950/80 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800">
                        {slot.day}
                      </span>
                      <span className="text-xs font-medium px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                        {slot.type}
                      </span>
                    </div>

                    <h3 className="font-bold text-base text-slate-900 dark:text-slate-100 mb-1 leading-snug">
                      {slot.title}
                    </h3>
                    <p className="text-xs font-medium text-purple-600 dark:text-purple-400 mb-4">
                      {slot.club}
                    </p>

                    <div className="space-y-2 text-xs text-slate-600 dark:text-slate-400 mb-5">
                      <div className="flex items-center gap-2">
                        <Clock className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        <span>{slot.time}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        <span>{slot.venue}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Users className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        <span>Capacity: {slot.capacity} seats</span>
                      </div>
                      <div className="flex items-center gap-2 pt-1 border-t border-slate-100 dark:border-slate-800/80">
                        <Mail className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        <span className="truncate">Faculty: {slot.facultyCoordinator} ({slot.facultyEmail})</span>
                      </div>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-100 dark:border-slate-800">
                    <button
                      onClick={() => {
                        const fakeEvent: Event = {
                          id: slot.id,
                          club_id: 'default',
                          title: slot.title,
                          description: `${slot.type} at ${slot.venue}`,
                          event_date: new Date().toISOString().split('T')[0],
                          start_time: slot.time.split(' - ')[0],
                          end_time: slot.time.split(' - ')[1],
                          venue: slot.venue,
                          capacity: slot.capacity,
                          registration_open: true,
                          created_at: new Date().toISOString()
                        };
                        handleRsvpEvent(fakeEvent);
                      }}
                      disabled={registeredEventIds.has(slot.id)}
                      className={`w-full py-2.5 px-4 rounded-xl text-xs font-semibold flex items-center justify-center gap-2 transition-colors ${
                        registeredEventIds.has(slot.id)
                          ? 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800'
                          : 'bg-purple-600 hover:bg-purple-500 text-white shadow-sm'
                      }`}
                    >
                      {registeredEventIds.has(slot.id) ? (
                        <>
                          <Check className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                          Seat Reserved
                        </>
                      ) : (
                        <>
                          <CalendarCheck2 className="w-4 h-4" />
                          Reserve Seat / RSVP
                        </>
                      )}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 2: EXPLORE CLUBS & APPLY VIA FACULTY */}
        {activeTab === 'clubs' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                  <Compass className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  Explore College Clubs &amp; Apply
                </h2>
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                  Browse clubs, read descriptions, and submit your joining application directly to the assigned faculty coordinator.
                </p>
              </div>

              {/* Search input */}
              <div className="relative min-w-[260px]">
                <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search clubs, domains, faculty..."
                  value={clubSearch}
                  onChange={(e) => setClubSearch(e.target.value)}
                  className="w-full pl-9 pr-4 py-2 rounded-xl text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>

            {loading ? (
              <div className="p-12 text-center text-slate-500 dark:text-slate-400">Loading campus clubs...</div>
            ) : filteredClubs.length === 0 ? (
              <div className="p-12 text-center bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
                <Compass className="w-12 h-12 text-slate-400 mx-auto mb-3" />
                <p className="text-base font-semibold text-slate-900 dark:text-slate-100">No clubs found</p>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Try adjusting your search criteria</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredClubs.map((club) => {
                  const status = memberClubIds.get(club.id);
                  return (
                    <div
                      key={club.id}
                      className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 flex flex-col justify-between hover:shadow-lg transition-all"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-4">
                          <div className="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-950/70 border border-purple-200 dark:border-purple-800 flex items-center justify-center font-bold text-lg text-purple-700 dark:text-purple-300">
                            {club.name.charAt(0)}
                          </div>

                          {status === 'approved' && (
                            <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950/70 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                              <CheckCircle className="w-3.5 h-3.5" />
                              Active Member
                            </span>
                          )}
                          {status === 'pending' && (
                            <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-amber-100 dark:bg-amber-950/70 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                              <Clock3 className="w-3.5 h-3.5" />
                              Under Review
                            </span>
                          )}
                        </div>

                        <h3 className="font-bold text-lg text-slate-900 dark:text-slate-100 mb-2">
                          {club.name}
                        </h3>
                        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 line-clamp-3 mb-4 leading-relaxed">
                          {club.description || 'Dedicated campus club fostering student innovation, hands-on learning, and community.'}
                        </p>

                        <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800 text-xs space-y-1.5 mb-5">
                          <div className="flex items-center justify-between text-slate-700 dark:text-slate-300">
                            <span className="font-semibold text-slate-500 dark:text-slate-400">Faculty Coordinator:</span>
                            <span className="font-medium">{club.faculty_coordinator || 'Dr. Department Lead'}</span>
                          </div>
                          <div className="flex items-center justify-between text-slate-700 dark:text-slate-300">
                            <span className="font-semibold text-slate-500 dark:text-slate-400">Faculty Email:</span>
                            <span className="font-medium truncate max-w-[160px] text-purple-600 dark:text-purple-400">
                              {club.contact_email || 'coordinator@college.edu'}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="pt-2 border-t border-slate-100 dark:border-slate-800">
                        {status === 'approved' ? (
                          <div className="w-full py-2.5 px-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 text-xs font-semibold text-center border border-emerald-200 dark:border-emerald-800">
                            You are an approved member
                          </div>
                        ) : status === 'pending' ? (
                          <div className="w-full py-2.5 px-4 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 text-xs font-semibold text-center border border-amber-200 dark:border-amber-800">
                            Application sent to faculty coordinator
                          </div>
                        ) : (
                          <button
                            onClick={() => {
                              setApplyingClub(club);
                              setApplicationMsg(
                                `Hello Professor, I would like to join ${club.name}. I am a ${profile?.department || 'Engineering'} student and wish to contribute to upcoming projects and weekly sessions.`
                              );
                            }}
                            className="w-full py-2.5 px-4 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold flex items-center justify-center gap-2 shadow-sm transition-colors"
                          >
                            <Send className="w-3.5 h-3.5" />
                            Apply &amp; Send to Faculty
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* TAB 3: CLUB NOTIFICATIONS */}
        {activeTab === 'notifications' && (
          <div className="space-y-4">
            <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
              <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                <Bell className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                Live Club Announcements &amp; Notifications
              </h2>
              <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                Official notices broadcast by faculty coordinators and club leads.
              </p>
            </div>

            <div className="space-y-3">
              {[
                {
                  id: 'ann-1',
                  club: 'Google Developer Student Club',
                  title: 'Spring Hackathon Registration Closes this Friday',
                  content: 'Teams of up to 4 members are invited to register for the 24-hour campus hackathon. Food, mentorship, and cloud credits provided.',
                  date: 'Today at 11:30 AM',
                  priority: 'High'
                },
                {
                  id: 'ann-2',
                  club: 'ACM Student Chapter',
                  title: 'Guest Lecture by Senior AI Scientist',
                  content: 'Venue shifted to Main Seminar Hall 2 due to high student registration. Please carry your college ID card for digital attendance verification.',
                  date: 'Yesterday at 04:15 PM',
                  priority: 'Medium'
                },
                {
                  id: 'ann-3',
                  club: 'Robotics & Automation Society',
                  title: 'New Microcontroller Kits Available in Hardware Lab',
                  content: 'Approved club members can issue ESP32 and STM32 boards from Lab 102 between 03:00 PM and 05:00 PM on weekdays.',
                  date: 'Oct 29, 2026',
                  priority: 'Normal'
                }
              ].map((notice) => (
                <div
                  key={notice.id}
                  className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 hover:border-purple-300 dark:hover:border-purple-700/60 transition-all shadow-sm"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-purple-600 dark:text-purple-400">
                      {notice.club}
                    </span>
                    <span className="text-xs text-slate-400 dark:text-slate-500">
                      {notice.date}
                    </span>
                  </div>
                  <h3 className="font-bold text-base text-slate-900 dark:text-slate-100 mb-1.5">
                    {notice.title}
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                    {notice.content}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: MY ATTENDANCE & STATUS */}
        {activeTab === 'attendance' && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
              <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                <UserCheck className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                Verified Attendance Transcript &amp; Profile
              </h2>
              <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                Official institutional attendance log verified by faculty coordinators.
              </p>
            </div>

            {/* Profile summary card */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              <div className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-4">
                  Student Credentials
                </h3>
                <div className="space-y-3 text-xs sm:text-sm">
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 block text-xs">Full Name</span>
                    <span className="font-semibold text-slate-900 dark:text-slate-100">{profile?.full_name}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 block text-xs">College Email</span>
                    <span className="font-semibold text-slate-900 dark:text-slate-100">{profile?.email}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 block text-xs">Department</span>
                    <span className="font-semibold text-slate-900 dark:text-slate-100">{profile?.department || 'Computer Science & Engineering'}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 dark:text-slate-400 block text-xs">Student ID / Roll No</span>
                    <span className="font-semibold text-slate-900 dark:text-slate-100">{profile?.student_id || '21CS108'}</span>
                  </div>
                </div>
              </div>

              <div className="md:col-span-2 bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-4">
                  Verified Session Attendance Log
                </h3>

                {attendanceRecords.length === 0 ? (
                  <div className="space-y-3">
                    {/* Mock institutional records to illustrate full functional view */}
                    {[
                      { session: 'Cloud Architecture & Gemini AI Workshop', club: 'GDSC', date: 'Oct 28, 2026', status: 'Present' },
                      { session: 'Graph Theory & Tree Traversals Sprint', club: 'ACM', date: 'Oct 21, 2026', status: 'Present' },
                      { session: 'CTF Web Exploit Simulation', club: 'Cyber Security Guild', date: 'Oct 14, 2026', status: 'Present' },
                      { session: 'Design Systems Critique', club: 'Design Society', date: 'Oct 07, 2026', status: 'Present' }
                    ].map((rec, i) => (
                      <div key={i} className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
                        <div>
                          <p className="font-semibold text-xs sm:text-sm text-slate-900 dark:text-slate-100">{rec.session}</p>
                          <p className="text-xs text-slate-500 dark:text-slate-400">{rec.club} &bull; {rec.date}</p>
                        </div>
                        <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950/70 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                          <CheckCircle className="w-3.5 h-3.5" />
                          {rec.status}
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="space-y-3">
                    {attendanceRecords.map((att) => (
                      <div key={att.id} className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
                        <div>
                          <p className="font-semibold text-xs sm:text-sm text-slate-900 dark:text-slate-100">{att.events?.title || 'Club Session'}</p>
                          <p className="text-xs text-slate-500 dark:text-slate-400">{att.events?.event_date}</p>
                        </div>
                        <span className={`inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full ${
                          att.status === 'present'
                            ? 'bg-emerald-100 dark:bg-emerald-950/70 text-emerald-700 dark:text-emerald-300'
                            : 'bg-red-100 dark:bg-red-950/70 text-red-700 dark:text-red-300'
                        }`}>
                          {att.status}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* MODAL: APPLY TO CLUB & DIRECT MAIL TO FACULTY */}
        {applyingClub && (
          <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 max-w-lg w-full p-6 sm:p-8 shadow-2xl animate-fade-in">
              <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 mb-5">
                <div>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                    Apply to {applyingClub.name}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    Faculty Coordinator: {applyingClub.faculty_coordinator} ({applyingClub.contact_email})
                  </p>
                </div>
                <button
                  onClick={() => setApplyingClub(null)}
                  className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleApplyToClub} className="space-y-4">
                <div className="p-3.5 rounded-xl bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800 text-xs text-purple-900 dark:text-purple-300 space-y-1">
                  <p className="font-semibold">Application Routing Notice:</p>
                  <p>
                    Submitting this form records your membership request in the CCMS database and prepares a pre-filled email draft directly to the faculty coordinator ({applyingClub.contact_email}).
                  </p>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                    Statement of Interest / Message to Faculty
                  </label>
                  <textarea
                    rows={4}
                    required
                    value={applicationMsg}
                    onChange={(e) => setApplicationMsg(e.target.value)}
                    placeholder="Describe your skills, interest in this club, and why you wish to join..."
                    className="w-full px-3.5 py-2.5 rounded-xl text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-3">
                  <button
                    type="button"
                    onClick={() => setApplyingClub(null)}
                    className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isSubmittingApp}
                    className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold inline-flex items-center gap-2 shadow-md transition-colors"
                  >
                    {isSubmittingApp ? (
                      'Submitting...'
                    ) : (
                      <>
                        <Send className="w-3.5 h-3.5" />
                        Send Application &amp; Mail
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
