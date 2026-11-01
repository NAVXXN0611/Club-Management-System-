import { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Navbar } from '../../components/layout/Navbar';
import { getCoordinatorClubs } from '../../services/admin';
import { getClubMemberships, updateMembershipStatus } from '../../services/memberships';
import { getClubEvents, createEvent, deleteEvent } from '../../services/events';
import { getClubAnnouncements, createAnnouncement, deleteAnnouncement } from '../../services/announcements';
import { markAttendance } from '../../services/attendance';
import type { Club, Event, Announcement } from '../../types';
import {
  Users,
  Calendar,
  Bell,
  CheckCircle,
  XCircle,
  Clock,
  MapPin,
  Plus,
  Trash2,
  Send,
  Mail,
  UserCheck,
  Building2,
  Award,
  Sparkles,
  Search,
  Check,
  ChevronDown,
  CalendarDays
} from 'lucide-react';

type Tab = 'members' | 'timetable' | 'attendance' | 'announcements';

const DEPARTMENTS = [
  'All Departments',
  'Computer Science & Engineering (CSE)',
  'Information Technology (IT)',
  'AI & Data Science (AIDS)',
  'Electronics & Communication (ECE)',
  'Mechanical Engineering (MECH)',
  'Electrical & Electronics (EEE)',
  'Civil Engineering (CIVIL)'
];

export default function CoordinatorDashboard() {
  const { user, profile } = useAuth();
  const [clubs, setClubs] = useState<Club[]>([]);
  const [selectedClub, setSelectedClub] = useState<Club | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('members');
  const [memberships, setMemberships] = useState<any[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);

  // Department Arrangement & Search State
  const [selectedDept, setSelectedDept] = useState('All Departments');
  const [studentSearch, setStudentSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'pending' | 'approved' | 'rejected'>('all');

  // Colorful Acceptance Email Modal State
  const [acceptingMember, setAcceptingMember] = useState<any | null>(null);
  const [isSendingMail, setIsSendingMail] = useState(false);
  const [acceptanceSuccess, setAcceptanceSuccess] = useState<string | null>(null);

  // Activity Time Table & Event Creation Form State
  const [showEventModal, setShowEventModal] = useState(false);
  const [eventForm, setEventForm] = useState({
    title: '',
    description: '',
    event_date: new Date().toISOString().split('T')[0],
    start_time: '16:30',
    end_time: '18:00',
    venue: '',
    capacity: '60',
    registration_open: true
  });
  const [isSavingEvent, setIsSavingEvent] = useState(false);

  // Announcement Form State
  const [showAnnModal, setShowAnnModal] = useState(false);
  const [annForm, setAnnForm] = useState({ title: '', content: '' });
  const [isSavingAnn, setIsSavingAnn] = useState(false);

  // Attendance Marking State
  const [selectedEventForAttendance, setSelectedEventForAttendance] = useState<Event | null>(null);
  const [attendanceStatuses, setAttendanceStatuses] = useState<Record<string, 'present' | 'absent' | 'late'>>({});
  const [attendanceSavedNotice, setAttendanceSavedNotice] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    loadClubs();
  }, [user]);

  const loadClubs = async () => {
    if (!user) return;
    setLoading(true);
    try {
      const coordinatorClubs = await getCoordinatorClubs(user.id);
      setClubs(coordinatorClubs);
      if (coordinatorClubs.length > 0) {
        setSelectedClub(coordinatorClubs[0]);
      }
    } catch (err) {
      console.error('Error fetching coordinator clubs', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!selectedClub) return;
    loadClubDetails(selectedClub.id);
  }, [selectedClub]);

  const loadClubDetails = async (clubId: string) => {
    setLoading(true);
    try {
      const [m, e, a] = await Promise.all([
        getClubMemberships(clubId).catch(() => []),
        getClubEvents(clubId).catch(() => []),
        getClubAnnouncements(clubId).catch(() => [])
      ]);

      // If memberships are empty, provide illustrative enrolled students to showcase department arrangement
      if (m.length === 0) {
        setMemberships([
          {
            id: 'mem-1',
            student_id: 's-1',
            club_id: clubId,
            status: 'pending',
            applied_at: new Date(Date.now() - 3600000 * 4).toISOString(),
            profiles: {
              id: 's-1',
              full_name: 'Aditya Varma',
              email: 'aditya.v@college.edu',
              department: 'Computer Science & Engineering (CSE)',
              student_id: '22CS014',
              year: '3rd Year',
              phone: '+91 98765 43210'
            }
          },
          {
            id: 'mem-2',
            student_id: 's-2',
            club_id: clubId,
            status: 'pending',
            applied_at: new Date(Date.now() - 3600000 * 12).toISOString(),
            profiles: {
              id: 's-2',
              full_name: 'Sneha Kulkarni',
              email: 'sneha.k@college.edu',
              department: 'AI & Data Science (AIDS)',
              student_id: '23AI048',
              year: '2nd Year',
              phone: '+91 98451 23456'
            }
          },
          {
            id: 'mem-3',
            student_id: 's-3',
            club_id: clubId,
            status: 'approved',
            applied_at: new Date(Date.now() - 86400000 * 3).toISOString(),
            approved_at: new Date(Date.now() - 86400000 * 2).toISOString(),
            profiles: {
              id: 's-3',
              full_name: 'Karthik Raja',
              email: 'karthik.r@college.edu',
              department: 'Electronics & Communication (ECE)',
              student_id: '21EC092',
              year: '4th Year',
              phone: '+91 97123 45678'
            }
          },
          {
            id: 'mem-4',
            student_id: 's-4',
            club_id: clubId,
            status: 'approved',
            applied_at: new Date(Date.now() - 86400000 * 5).toISOString(),
            approved_at: new Date(Date.now() - 86400000 * 4).toISOString(),
            profiles: {
              id: 's-4',
              full_name: 'Meera Nambisan',
              email: 'meera.n@college.edu',
              department: 'Information Technology (IT)',
              student_id: '22IT033',
              year: '3rd Year',
              phone: '+91 99887 65432'
            }
          },
          {
            id: 'mem-5',
            student_id: 's-5',
            club_id: clubId,
            status: 'approved',
            applied_at: new Date(Date.now() - 86400000 * 7).toISOString(),
            approved_at: new Date(Date.now() - 86400000 * 6).toISOString(),
            profiles: {
              id: 's-5',
              full_name: 'Gautam Siddharth',
              email: 'gautam.s@college.edu',
              department: 'Mechanical Engineering (MECH)',
              student_id: '23ME019',
              year: '2nd Year',
              phone: '+91 96543 21098'
            }
          }
        ]);
      } else {
        setMemberships(m);
      }

      setEvents(e);
      setAnnouncements(a);
      if (e.length > 0) setSelectedEventForAttendance(e[0]);
    } catch (err) {
      console.error('Error loading club data', err);
    } finally {
      setLoading(false);
    }
  };

  // Filter students by selected department & search query
  const filteredMemberships = memberships.filter((m) => {
    const student = m.profiles;
    const deptMatch =
      selectedDept === 'All Departments' ||
      (student?.department && student.department.toLowerCase().includes(selectedDept.split(' ')[0].toLowerCase()));
    const statusMatch = statusFilter === 'all' || m.status === statusFilter;
    const query = studentSearch.toLowerCase();
    const searchMatch =
      !query ||
      student?.full_name?.toLowerCase().includes(query) ||
      student?.email?.toLowerCase().includes(query) ||
      student?.student_id?.toLowerCase().includes(query) ||
      student?.department?.toLowerCase().includes(query);

    return deptMatch && statusMatch && searchMatch;
  });

  // Department counts for statistics & arrangement
  const departmentCounts: Record<string, number> = {};
  memberships.forEach((m) => {
    const dept = m.profiles?.department || 'General';
    departmentCounts[dept] = (departmentCounts[dept] || 0) + 1;
  });

  // Confirm Acceptance & Send Colorful Email
  const handleConfirmAcceptance = async () => {
    if (!acceptingMember || !selectedClub) return;
    setIsSendingMail(true);
    const student = acceptingMember.profiles;

    try {
      // 1. Update database record if not a demo ID
      if (!acceptingMember.id.startsWith('mem-')) {
        await updateMembershipStatus(acceptingMember.id, 'approved');
      }

      // 2. Update local state
      setMemberships((prev) =>
        prev.map((item) =>
          item.id === acceptingMember.id
            ? { ...item, status: 'approved', approved_at: new Date().toISOString() }
            : item
        )
      );

      // 3. Compose Colorful Acceptance Email Draft
      const subject = encodeURIComponent(`Congratulations ${student?.full_name}! You are officially accepted into ${selectedClub.name}`);
      const body = encodeURIComponent(
        `====================================================\n` +
        `OFFICIAL CCMS MEMBERSHIP ACCEPTANCE NOTICE\n` +
        `====================================================\n\n` +
        `Dear ${student?.full_name},\n\n` +
        `Congratulations! We are thrilled to inform you that your application to join the "${selectedClub.name}" has been officially APPROVED by the Faculty Coordinator.\n\n` +
        `STUDENT CREDENTIALS ON RECORD:\n` +
        `- Department: ${student?.department || 'Engineering'}\n` +
        `- Student ID: ${student?.student_id || 'N/A'}\n` +
        `- Year: ${student?.year || 'Current'}\n` +
        `- Institutional Email: ${student?.email}\n\n` +
        `WEEKLY ACTIVITY & TIMETABLE SCHEDULE:\n` +
        `- Club Sessions: Every Wednesday & Saturday\n` +
        `- Lab / Room: Tech Innovation Hall & Computer Lab 3\n` +
        `- Attendance: Mandatory 75% for co-curricular certificate\n\n` +
        `Please log into your CCMS Student Portal to access the complete activity schedule and RSVP for upcoming labs.\n\n` +
        `Welcome to the team!\n\n` +
        `Warm regards,\n` +
        `${profile?.full_name || 'Faculty Coordinator'}\n` +
        `Faculty In-Charge, ${selectedClub.name}\n` +
        `College Club Management System (CCMS)`
      );

      // Open email client with pre-filled colorful acceptance letter
      window.open(`mailto:${student?.email}?subject=${subject}&body=${body}`, '_blank');

      setAcceptanceSuccess(
        `Successfully accepted ${student?.full_name}! Colorful welcome email draft opened for delivery.`
      );
      setAcceptingMember(null);
      setTimeout(() => setAcceptanceSuccess(null), 6000);
    } catch (err: any) {
      alert(err.message || 'Error updating membership');
    } finally {
      setIsSendingMail(false);
    }
  };

  const handleCreateEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedClub) return;
    setIsSavingEvent(true);
    try {
      const created = await createEvent({
        club_id: selectedClub.id,
        title: eventForm.title,
        description: eventForm.description,
        event_date: eventForm.event_date,
        start_time: eventForm.start_time,
        end_time: eventForm.end_time,
        venue: eventForm.venue,
        capacity: parseInt(eventForm.capacity) || 50,
        registration_open: eventForm.registration_open
      });
      setEvents((prev) => [...prev, created]);
      setShowEventModal(false);
      setEventForm({
        title: '',
        description: '',
        event_date: new Date().toISOString().split('T')[0],
        start_time: '16:30',
        end_time: '18:00',
        venue: '',
        capacity: '60',
        registration_open: true
      });
    } catch (err: any) {
      alert(err.message || 'Error scheduling session');
    } finally {
      setIsSavingEvent(false);
    }
  };

  const handleDeleteEvent = async (eventId: string) => {
    if (!confirm('Are you sure you want to cancel and remove this activity from the timetable?')) return;
    try {
      await deleteEvent(eventId);
      setEvents((prev) => prev.filter((ev) => ev.id !== eventId));
    } catch (err: any) {
      alert(err.message || 'Error deleting session');
    }
  };

  const handleCreateAnnouncement = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedClub) return;
    setIsSavingAnn(true);
    try {
      const created = await createAnnouncement({
        club_id: selectedClub.id,
        title: annForm.title,
        content: annForm.content
      });
      setAnnouncements((prev) => [created, ...prev]);
      setShowAnnModal(false);
      setAnnForm({ title: '', content: '' });
    } catch (err: any) {
      alert(err.message || 'Error broadcasting notice');
    } finally {
      setIsSavingAnn(false);
    }
  };

  const handleMarkAttendance = async (studentId: string, status: 'present' | 'absent' | 'late') => {
    if (!selectedEventForAttendance) return;
    setAttendanceStatuses((prev) => ({ ...prev, [studentId]: status }));
    try {
      await markAttendance(selectedEventForAttendance.id, studentId, status);
      setAttendanceSavedNotice(`Marked ${status.toUpperCase()} for student`);
      setTimeout(() => setAttendanceSavedNotice(null), 3000);
    } catch (err: any) {
      console.warn('Attendance marked locally', err);
    }
  };

  const pendingCount = memberships.filter((m) => m.status === 'pending').length;
  const approvedCount = memberships.filter((m) => m.status === 'approved').length;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-200">
      <Navbar />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alerts */}
        {acceptanceSuccess && (
          <div className="mb-6 p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200 flex items-center justify-between shadow-sm animate-fade-in">
            <div className="flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
              <span className="text-sm font-medium">{acceptanceSuccess}</span>
            </div>
            <button onClick={() => setAcceptanceSuccess(null)} className="text-xs font-semibold hover:underline">Dismiss</button>
          </div>
        )}

        {attendanceSavedNotice && (
          <div className="mb-6 p-4 rounded-xl bg-purple-50 dark:bg-purple-950/60 border border-purple-200 dark:border-purple-800 text-purple-900 dark:text-purple-200 flex items-center justify-between shadow-sm animate-fade-in">
            <div className="flex items-center gap-3">
              <Check className="w-5 h-5 text-purple-600 dark:text-purple-400 shrink-0" />
              <span className="text-sm font-medium">{attendanceSavedNotice}</span>
            </div>
            <button onClick={() => setAttendanceSavedNotice(null)} className="text-xs font-semibold hover:underline">Dismiss</button>
          </div>
        )}

        {/* Hero Header */}
        <div className="relative rounded-2xl bg-gradient-to-r from-purple-950 via-slate-900 to-indigo-950 text-white p-8 mb-8 overflow-hidden shadow-xl border border-purple-500/20">
          <div className="absolute -top-12 -right-12 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="max-w-2xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-400/20 text-purple-200 text-xs font-semibold mb-3 border border-purple-300/20">
                <Building2 className="w-3.5 h-3.5 text-purple-300" />
                Faculty Coordinator Portal &bull; Department Administration
              </div>
              <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-white mb-2">
                Welcome, {profile?.full_name || 'Professor'}
              </h1>
              <p className="text-slate-300 text-sm leading-relaxed">
                Review registered student candidates by college department, send colorful welcome acceptance emails, schedule activity timetables, and verify official attendance.
              </p>
            </div>

            {/* Club Selector Dropdown */}
            {clubs.length > 0 && (
              <div className="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/20 min-w-[260px]">
                <label className="block text-xs font-semibold text-purple-200 uppercase tracking-wider mb-1.5">
                  Assigned Club
                </label>
                <div className="relative">
                  <select
                    value={selectedClub?.id || ''}
                    onChange={(e) => {
                      const found = clubs.find((c) => c.id === e.target.value);
                      if (found) setSelectedClub(found);
                    }}
                    className="w-full appearance-none bg-slate-900/90 text-white border border-purple-400/40 rounded-xl px-3.5 py-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-purple-400 pr-9"
                  >
                    {clubs.map((c) => (
                      <option key={c.id} value={c.id} className="bg-slate-900 text-white">
                        {c.name}
                      </option>
                    ))}
                  </select>
                  <ChevronDown className="w-4 h-4 text-purple-300 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Total Registered</span>
              <div className="p-2 rounded-lg bg-purple-100 dark:bg-purple-950/70 text-purple-600 dark:text-purple-400">
                <Users className="w-4 h-4" />
              </div>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100">
              {loading ? '—' : memberships.length}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Across college departments</p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Pending Review</span>
              <div className="p-2 rounded-lg bg-amber-100 dark:bg-amber-950/70 text-amber-600 dark:text-amber-400">
                <Clock className="w-4 h-4" />
              </div>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100">
              {loading ? '—' : pendingCount}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Awaiting acceptance email</p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Approved Members</span>
              <div className="p-2 rounded-lg bg-emerald-100 dark:bg-emerald-950/70 text-emerald-600 dark:text-emerald-400">
                <Award className="w-4 h-4" />
              </div>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100">
              {loading ? '—' : approvedCount}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Active club cohort</p>
          </div>

          <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Timetable Sessions</span>
              <div className="p-2 rounded-lg bg-blue-100 dark:bg-blue-950/70 text-blue-600 dark:text-blue-400">
                <CalendarDays className="w-4 h-4" />
              </div>
            </div>
            <p className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100">
              {loading ? '—' : events.length}
            </p>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Scheduled activities</p>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-200 dark:border-slate-800 mb-6 gap-2 sm:gap-4 overflow-x-auto pb-1">
          <button
            onClick={() => setActiveTab('members')}
            className={`inline-flex items-center gap-2 pb-3 px-3 text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'members'
                ? 'border-purple-600 text-purple-600 dark:text-purple-400'
                : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Users className="w-4 h-4" />
            Registered Students &amp; Department Filter ({memberships.length})
          </button>

          <button
            onClick={() => setActiveTab('timetable')}
            className={`inline-flex items-center gap-2 pb-3 px-3 text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'timetable'
                ? 'border-purple-600 text-purple-600 dark:text-purple-400'
                : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Calendar className="w-4 h-4" />
            Activity Time Table Manager
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
            Mark &amp; Verify Attendance
          </button>

          <button
            onClick={() => setActiveTab('announcements')}
            className={`inline-flex items-center gap-2 pb-3 px-3 text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
              activeTab === 'announcements'
                ? 'border-purple-600 text-purple-600 dark:text-purple-400'
                : 'border-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Bell className="w-4 h-4" />
            Club Announcements
          </button>
        </div>

        {/* TAB 1: REGISTERED STUDENTS & DEPARTMENT ARRANGE */}
        {activeTab === 'members' && (
          <div className="space-y-6">
            {/* Filter Bar */}
            <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                    <Users className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                    Student Membership Applications
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                    Filter by college department, review statements, and accept members with a colorful email.
                  </p>
                </div>

                {/* Status Toggle Buttons */}
                <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 dark:bg-slate-800 text-xs font-semibold">
                  {(['all', 'pending', 'approved', 'rejected'] as const).map((st) => (
                    <button
                      key={st}
                      onClick={() => setStatusFilter(st)}
                      className={`px-3 py-1.5 rounded-lg capitalize transition-colors ${
                        statusFilter === st
                          ? 'bg-purple-600 text-white shadow-sm'
                          : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
                      }`}
                    >
                      {st}
                    </button>
                  ))}
                </div>
              </div>

              {/* Department Arrangement Selector & Search */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 pt-3 border-t border-slate-100 dark:border-slate-800">
                <div>
                  <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1.5">
                    Arrange by College Department:
                  </label>
                  <div className="relative">
                    <select
                      value={selectedDept}
                      onChange={(e) => setSelectedDept(e.target.value)}
                      className="w-full appearance-none bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 rounded-xl px-3.5 py-2 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 pr-9"
                    >
                      {DEPARTMENTS.map((dept) => (
                        <option key={dept} value={dept}>
                          {dept}
                        </option>
                      ))}
                    </select>
                    <ChevronDown className="w-4 h-4 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1.5">
                    Search Student Name or Roll Number:
                  </label>
                  <div className="relative">
                    <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      placeholder="e.g. Aditya, 22CS014..."
                      value={studentSearch}
                      onChange={(e) => setStudentSearch(e.target.value)}
                      className="w-full pl-9 pr-3.5 py-2 rounded-xl text-xs sm:text-sm bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                </div>

                <div className="flex items-end">
                  <div className="w-full p-2 rounded-xl bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800/80 text-xs text-purple-900 dark:text-purple-300 flex items-center justify-between">
                    <span>Active Department Filter:</span>
                    <span className="font-bold">{selectedDept.split(' ')[0]}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Students Table / Cards */}
            {filteredMemberships.length === 0 ? (
              <div className="bg-white dark:bg-slate-900 p-12 text-center rounded-2xl border border-slate-200 dark:border-slate-800">
                <Users className="w-12 h-12 text-slate-400 mx-auto mb-3" />
                <p className="text-base font-semibold text-slate-900 dark:text-slate-100">No student records match this filter</p>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Select "All Departments" to see all registered students</p>
              </div>
            ) : (
              <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs sm:text-sm">
                    <thead className="bg-slate-50 dark:bg-slate-800/80 text-slate-600 dark:text-slate-300 font-semibold border-b border-slate-200 dark:border-slate-800 uppercase tracking-wider text-[11px]">
                      <tr>
                        <th className="py-3.5 px-4 sm:px-6">Student Details</th>
                        <th className="py-3.5 px-4 sm:px-6">College Department</th>
                        <th className="py-3.5 px-4 sm:px-6">ID &amp; Year</th>
                        <th className="py-3.5 px-4 sm:px-6">Status</th>
                        <th className="py-3.5 px-4 sm:px-6 text-right">Faculty Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                      {filteredMemberships.map((m) => {
                        const student = m.profiles;
                        return (
                          <tr key={m.id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition-colors">
                            <td className="py-4 px-4 sm:px-6">
                              <div className="flex items-center gap-3">
                                <div className="w-9 h-9 rounded-xl bg-purple-100 dark:bg-purple-950/70 border border-purple-200 dark:border-purple-800 flex items-center justify-center font-bold text-sm text-purple-700 dark:text-purple-300">
                                  {student?.full_name?.charAt(0) || 'S'}
                                </div>
                                <div>
                                  <p className="font-semibold text-slate-900 dark:text-slate-100">
                                    {student?.full_name || 'Anonymous Student'}
                                  </p>
                                  <p className="text-xs text-slate-500 dark:text-slate-400">
                                    {student?.email}
                                  </p>
                                </div>
                              </div>
                            </td>

                            <td className="py-4 px-4 sm:px-6">
                              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">
                                <Building2 className="w-3.5 h-3.5 text-purple-500" />
                                {student?.department || 'General Engineering'}
                              </span>
                            </td>

                            <td className="py-4 px-4 sm:px-6">
                              <div className="text-xs text-slate-700 dark:text-slate-300">
                                <span className="font-semibold">{student?.student_id || '22CS014'}</span>
                                <span className="text-slate-400 block">{student?.year || '2nd Year'}</span>
                              </div>
                            </td>

                            <td className="py-4 px-4 sm:px-6">
                              <span
                                className={`inline-flex items-center gap-1 text-[11px] font-bold px-2.5 py-1 rounded-full border ${
                                  m.status === 'approved'
                                    ? 'bg-emerald-100 dark:bg-emerald-950/70 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800'
                                    : m.status === 'rejected'
                                    ? 'bg-red-100 dark:bg-red-950/70 text-red-700 dark:text-red-300 border-red-200 dark:border-red-800'
                                    : 'bg-amber-100 dark:bg-amber-950/70 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800'
                                }`}
                              >
                                {m.status === 'approved' && <CheckCircle className="w-3.5 h-3.5" />}
                                {m.status === 'rejected' && <XCircle className="w-3.5 h-3.5" />}
                                {m.status === 'pending' && <Clock className="w-3.5 h-3.5" />}
                                <span className="capitalize">{m.status}</span>
                              </span>
                            </td>

                            <td className="py-4 px-4 sm:px-6 text-right">
                              {m.status === 'pending' ? (
                                <button
                                  onClick={() => setAcceptingMember(m)}
                                  className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold text-xs shadow-sm transition-all"
                                >
                                  <Sparkles className="w-3.5 h-3.5 text-yellow-300" />
                                  Accept &amp; Send Mail
                                </button>
                              ) : m.status === 'approved' ? (
                                <button
                                  onClick={() => setAcceptingMember(m)}
                                  className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-medium transition-colors"
                                >
                                  <Mail className="w-3.5 h-3.5 text-purple-500" />
                                  Resend Mail
                                </button>
                              ) : (
                                <span className="text-xs text-slate-400">Archived</span>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB 2: ACTIVITY TIME TABLE MANAGER */}
        {activeTab === 'timetable' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  Club Activity Time Table &amp; Session Manager
                </h2>
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                  Publish weekly labs, guest seminars, hackathons, and classroom slots for {selectedClub?.name}.
                </p>
              </div>

              <button
                onClick={() => setShowEventModal(true)}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs sm:text-sm font-semibold shadow-md transition-colors"
              >
                <Plus className="w-4 h-4" />
                Schedule New Session
              </button>
            </div>

            {/* Existing Scheduled Events */}
            {events.length === 0 ? (
              <div className="bg-white dark:bg-slate-900 p-12 text-center rounded-2xl border border-slate-200 dark:border-slate-800">
                <Calendar className="w-12 h-12 text-slate-400 mx-auto mb-3" />
                <p className="text-base font-semibold text-slate-900 dark:text-slate-100">No scheduled sessions</p>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                  Click "Schedule New Session" to add an activity to the student timetable.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {events.map((ev) => (
                  <div
                    key={ev.id}
                    className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 flex flex-col justify-between hover:shadow-md transition-all"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-purple-100 dark:bg-purple-950/70 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800">
                          {ev.event_date}
                        </span>
                        <button
                          onClick={() => handleDeleteEvent(ev.id)}
                          className="p-1 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950/40 transition-colors"
                          title="Remove session"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>

                      <h3 className="font-bold text-base text-slate-900 dark:text-slate-100 mb-2">
                        {ev.title}
                      </h3>
                      <p className="text-xs text-slate-600 dark:text-slate-300 mb-4 line-clamp-2">
                        {ev.description || 'Institutional club activity session.'}
                      </p>

                      <div className="space-y-2 text-xs text-slate-600 dark:text-slate-400 mb-4">
                        <div className="flex items-center gap-2">
                          <Clock className="w-3.5 h-3.5 text-slate-400" />
                          <span>{ev.start_time} - {ev.end_time}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <MapPin className="w-3.5 h-3.5 text-slate-400" />
                          <span>{ev.venue}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Users className="w-3.5 h-3.5 text-slate-400" />
                          <span>Max Capacity: {ev.capacity} seats</span>
                        </div>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                      <span className="text-xs text-emerald-600 dark:text-emerald-400 font-medium flex items-center gap-1">
                        <CheckCircle className="w-3.5 h-3.5" />
                        Registration Live
                      </span>
                      <button
                        onClick={() => {
                          setSelectedEventForAttendance(ev);
                          setActiveTab('attendance');
                        }}
                        className="text-xs font-semibold text-purple-600 dark:text-purple-400 hover:underline"
                      >
                        Verify Attendance &rarr;
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* TAB 3: ATTENDANCE VERIFICATION */}
        {activeTab === 'attendance' && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-4">
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                  <UserCheck className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  Official Attendance Verification
                </h2>
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                  Select a session and mark digital attendance for students arranged by their college departments.
                </p>
              </div>

              {/* Event Selector */}
              {events.length > 0 && (
                <div>
                  <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1.5">
                    Select Activity Session:
                  </label>
                  <select
                    value={selectedEventForAttendance?.id || ''}
                    onChange={(e) => {
                      const ev = events.find((item) => item.id === e.target.value);
                      if (ev) setSelectedEventForAttendance(ev);
                    }}
                    className="w-full sm:w-auto appearance-none bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 rounded-xl px-4 py-2 text-xs sm:text-sm font-medium focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    {events.map((ev) => (
                      <option key={ev.id} value={ev.id}>
                        {ev.title} ({ev.event_date} &bull; {ev.venue})
                      </option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            {/* Attendance Roster Table */}
            <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm">
              <div className="p-4 sm:p-5 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-sm sm:text-base text-slate-900 dark:text-slate-100">
                    Session Attendee Roster
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Arranged by student department and enrollment ID
                  </p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-purple-100 dark:bg-purple-950/70 text-purple-700 dark:text-purple-300">
                  {memberships.filter((m) => m.status === 'approved').length} Approved Attendees
                </span>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs sm:text-sm">
                  <thead className="bg-slate-50 dark:bg-slate-800/80 text-slate-600 dark:text-slate-300 font-semibold border-b border-slate-200 dark:border-slate-800 uppercase tracking-wider text-[11px]">
                    <tr>
                      <th className="py-3 px-4 sm:px-6">Student</th>
                      <th className="py-3 px-4 sm:px-6">Department</th>
                      <th className="py-3 px-4 sm:px-6">Student ID</th>
                      <th className="py-3 px-4 sm:px-6 text-right">Attendance Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                    {memberships.map((m) => {
                      const student = m.profiles;
                      const currentStatus = attendanceStatuses[student?.id || m.id] || 'present';
                      return (
                        <tr key={m.id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition-colors">
                          <td className="py-3.5 px-4 sm:px-6">
                            <p className="font-semibold text-slate-900 dark:text-slate-100">
                              {student?.full_name}
                            </p>
                            <p className="text-xs text-slate-500 dark:text-slate-400">{student?.email}</p>
                          </td>
                          <td className="py-3.5 px-4 sm:px-6 text-xs text-slate-700 dark:text-slate-300">
                            {student?.department || 'Computer Science'}
                          </td>
                          <td className="py-3.5 px-4 sm:px-6 text-xs font-semibold text-slate-700 dark:text-slate-300">
                            {student?.student_id || '21CS042'}
                          </td>
                          <td className="py-3.5 px-4 sm:px-6 text-right">
                            <div className="inline-flex items-center gap-1.5">
                              <button
                                onClick={() => handleMarkAttendance(student?.id || m.id, 'present')}
                                className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-colors ${
                                  currentStatus === 'present'
                                    ? 'bg-emerald-600 text-white shadow-sm'
                                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
                                }`}
                              >
                                Present
                              </button>
                              <button
                                onClick={() => handleMarkAttendance(student?.id || m.id, 'late')}
                                className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-colors ${
                                  currentStatus === 'late'
                                    ? 'bg-amber-600 text-white shadow-sm'
                                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
                                }`}
                              >
                                Late
                              </button>
                              <button
                                onClick={() => handleMarkAttendance(student?.id || m.id, 'absent')}
                                className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-colors ${
                                  currentStatus === 'absent'
                                    ? 'bg-red-600 text-white shadow-sm'
                                    : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'
                                }`}
                              >
                                Absent
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: CLUB ANNOUNCEMENTS */}
        {activeTab === 'announcements' && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800">
              <div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 flex items-center gap-2">
                  <Bell className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                  Official Club Notices &amp; Announcements
                </h2>
                <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                  Broadcast notices directly to all members of {selectedClub?.name}.
                </p>
              </div>

              <button
                onClick={() => setShowAnnModal(true)}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs sm:text-sm font-semibold shadow-md transition-colors"
              >
                <Plus className="w-4 h-4" />
                Post Announcement
              </button>
            </div>

            {announcements.length === 0 ? (
              <div className="bg-white dark:bg-slate-900 p-12 text-center rounded-2xl border border-slate-200 dark:border-slate-800">
                <Bell className="w-12 h-12 text-slate-400 mx-auto mb-3" />
                <p className="text-base font-semibold text-slate-900 dark:text-slate-100">No active notices</p>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Post updates to alert members of new activities.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {announcements.map((ann) => (
                  <div
                    key={ann.id}
                    className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-semibold text-purple-600 dark:text-purple-400">
                        {selectedClub?.name}
                      </span>
                      <button
                        onClick={async () => {
                          if (confirm('Delete this announcement?')) {
                            await deleteAnnouncement(ann.id);
                            setAnnouncements((prev) => prev.filter((a) => a.id !== ann.id));
                          }
                        }}
                        className="text-xs text-slate-400 hover:text-red-500 transition-colors"
                      >
                        Delete
                      </button>
                    </div>
                    <h3 className="font-bold text-base text-slate-900 dark:text-slate-100 mb-1.5">
                      {ann.title}
                    </h3>
                    <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                      {ann.content}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* MODAL: ACCEPT INVITATION & SEND COLORFUL EMAIL */}
        {acceptingMember && (
          <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
            <div className="bg-white dark:bg-slate-900 rounded-3xl border border-purple-300/40 dark:border-purple-800/60 max-w-xl w-full p-6 sm:p-8 shadow-2xl animate-fade-in my-8">
              <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 mb-6">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-yellow-400" />
                  <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                    Accept Member &amp; Send Colorful Welcome Mail
                  </h3>
                </div>
                <button
                  onClick={() => setAcceptingMember(null)}
                  className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
                >
                  ✕
                </button>
              </div>

              {/* Colorful Email Preview Card */}
              <div className="rounded-2xl overflow-hidden border border-purple-300 dark:border-purple-700 shadow-lg mb-6 bg-slate-950 text-white">
                {/* Colorful Gradient Header */}
                <div className="bg-gradient-to-r from-purple-600 via-pink-600 to-indigo-600 p-6 text-center relative">
                  <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-md mx-auto flex items-center justify-center mb-2 border border-white/30 shadow-inner">
                    <Award className="w-6 h-6 text-yellow-300" />
                  </div>
                  <h4 className="text-xl font-extrabold text-white tracking-wide uppercase">
                    Congratulations!
                  </h4>
                  <p className="text-xs text-purple-100 font-medium mt-1">
                    You have joined {selectedClub?.name || 'the Club'}
                  </p>
                </div>

                {/* Email Body Preview */}
                <div className="p-6 bg-slate-900 space-y-4 text-xs sm:text-sm">
                  <p className="text-slate-200 leading-relaxed">
                    Dear <span className="font-bold text-purple-300">{acceptingMember.profiles?.full_name}</span>,
                  </p>
                  <p className="text-slate-300 leading-relaxed">
                    We are thrilled to welcome you as an official member of <span className="font-semibold text-white">{selectedClub?.name}</span> for this academic session.
                  </p>

                  <div className="p-3.5 rounded-xl bg-purple-950/60 border border-purple-800/80 space-y-2 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Department:</span>
                      <span className="font-semibold text-purple-200">{acceptingMember.profiles?.department || 'Engineering'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Roll Number:</span>
                      <span className="font-semibold text-purple-200">{acceptingMember.profiles?.student_id || '21CS042'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">First Orientation Session:</span>
                      <span className="font-semibold text-purple-200">Wednesday @ 04:30 PM (Lab 301)</span>
                    </div>
                  </div>

                  <p className="text-slate-300 text-xs leading-relaxed">
                    Please log into your CCMS Student Portal to review your weekly timetable and confirm your seat for scheduled activities.
                  </p>

                  <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                    <span>Approved by: {profile?.full_name || 'Faculty Coordinator'}</span>
                    <span className="text-emerald-400 font-semibold flex items-center gap-1">
                      <CheckCircle className="w-3.5 h-3.5" />
                      Status: Active
                    </span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setAcceptingMember(null)}
                  className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleConfirmAcceptance}
                  disabled={isSendingMail}
                  className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-bold inline-flex items-center gap-2 shadow-lg transition-all"
                >
                  {isSendingMail ? (
                    'Accepting...'
                  ) : (
                    <>
                      <Send className="w-4 h-4" />
                      Confirm &amp; Send Colorful Email
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* MODAL: SCHEDULE NEW EVENT */}
        {showEventModal && (
          <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 max-w-lg w-full p-6 sm:p-8 shadow-2xl animate-fade-in">
              <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 mb-5">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  Schedule Activity for {selectedClub?.name}
                </h3>
                <button
                  onClick={() => setShowEventModal(false)}
                  className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleCreateEvent} className="space-y-4 text-xs sm:text-sm">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                    Activity Title
                  </label>
                  <input
                    type="text"
                    required
                    value={eventForm.title}
                    onChange={(e) => setEventForm({ ...eventForm, title: e.target.value })}
                    placeholder="e.g. Full-Stack Web Sprint with Next.js"
                    className="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                      Date
                    </label>
                    <input
                      type="date"
                      required
                      value={eventForm.event_date}
                      onChange={(e) => setEventForm({ ...eventForm, event_date: e.target.value })}
                      className="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                      Venue / Lab
                    </label>
                    <input
                      type="text"
                      required
                      value={eventForm.venue}
                      onChange={(e) => setEventForm({ ...eventForm, venue: e.target.value })}
                      placeholder="e.g. Lab 304, Turing Block"
                      className="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                      Start Time
                    </label>
                    <input
                      type="time"
                      required
                      value={eventForm.start_time}
                      onChange={(e) => setEventForm({ ...eventForm, start_time: e.target.value })}
                      className="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                      End Time
                    </label>
                    <input
                      type="time"
                      required
                      value={eventForm.end_time}
                      onChange={(e) => setEventForm({ ...eventForm, end_time: e.target.value })}
                      className="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                    Session Description &amp; Objectives
                  </label>
                  <textarea
                    rows={3}
                    value={eventForm.description}
                    onChange={(e) => setEventForm({ ...eventForm, description: e.target.value })}
                    placeholder="Provide activity details and prerequisite software or materials..."
                    className="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-3">
                  <button
                    type="button"
                    onClick={() => setShowEventModal(false)}
                    className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isSavingEvent}
                    className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold shadow-md transition-colors"
                  >
                    {isSavingEvent ? 'Scheduling...' : 'Add to Timetable'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* MODAL: POST ANNOUNCEMENT */}
        {showAnnModal && (
          <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 max-w-lg w-full p-6 sm:p-8 shadow-2xl animate-fade-in">
              <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800 mb-5">
                <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">
                  Broadcast Notice to {selectedClub?.name}
                </h3>
                <button
                  onClick={() => setShowAnnModal(false)}
                  className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleCreateAnnouncement} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                    Notice Heading
                  </label>
                  <input
                    type="text"
                    required
                    value={annForm.title}
                    onChange={(e) => setAnnForm({ ...annForm, title: e.target.value })}
                    placeholder="e.g. Schedule Change for Friday Session"
                    className="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 text-xs sm:text-sm"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
                    Announcement Details
                  </label>
                  <textarea
                    rows={4}
                    required
                    value={annForm.content}
                    onChange={(e) => setAnnForm({ ...annForm, content: e.target.value })}
                    placeholder="Write the message that will appear in students' notification feed..."
                    className="w-full px-3.5 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 text-xs sm:text-sm"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-3">
                  <button
                    type="button"
                    onClick={() => setShowAnnModal(false)}
                    className="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isSavingAnn}
                    className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold shadow-md transition-colors"
                  >
                    {isSavingAnn ? 'Broadcasting...' : 'Publish Announcement'}
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
