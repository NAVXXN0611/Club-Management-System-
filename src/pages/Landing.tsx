import { Link } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';
import {
  Sparkles,
  Sun,
  Moon,
  GraduationCap,
  Building2,
  Calendar,
  Compass,
  CheckCircle,
  ArrowRight,
  Award,
  BookOpen,
  Mail,
  Clock,
  MapPin
} from 'lucide-react';

const FEATURES = [
  {
    icon: Compass,
    title: 'Club Discovery & Overview',
    desc: 'Browse dynamic club catalogs across tech, robotics, coding, design, cultural, and sports domains with complete faculty coordinator details.'
  },
  {
    icon: Calendar,
    title: 'Weekly Activity Time Table',
    desc: 'Weekly lab sessions, hands-on workshops, coding sprints, and weekend hackathons scheduled with venues and seat capacities.'
  },
  {
    icon: Mail,
    title: 'Department Sorting & Colorful Email',
    desc: 'Faculty coordinators arrange registered students by department and approve members with colorful, official welcome acceptance emails.'
  },
  {
    icon: Award,
    title: 'Institutional Attendance',
    desc: 'Digital check-in and verified attendance transcript to document student co-curricular participation.'
  }
];

export default function Landing() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-200">
      {/* Top Banner Ticker */}
      <div className="bg-purple-900 text-white text-xs py-2 px-4 text-center font-medium tracking-wide flex items-center justify-center gap-2">
        <span className="inline-flex items-center gap-1.5 bg-purple-700/80 text-purple-100 px-2 py-0.5 rounded-full text-[11px] font-bold">
          <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-ping" />
          ACTIVE
        </span>
        <span>Campus Club Spring Registrations &amp; Activity Timetables are now live!</span>
        <Link to="/clubs" className="underline hover:text-purple-200 font-semibold ml-1">
          Explore Clubs &rarr;
        </Link>
      </div>

      {/* Navigation Bar */}
      <nav className="sticky top-0 z-40 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 bg-gradient-to-br from-purple-700 to-indigo-700 rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-md group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5 text-purple-200" />
            </div>
            <div>
              <span className="font-bold text-lg text-slate-900 dark:text-white tracking-tight leading-none block">
                CCMS
              </span>
              <span className="text-[10px] text-purple-600 dark:text-purple-400 font-semibold uppercase tracking-wider">
                Campus Club System
              </span>
            </div>
          </Link>

          <div className="hidden md:flex items-center gap-8 text-xs font-semibold text-slate-600 dark:text-slate-300">
            <a href="#portals" className="hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Portals</a>
            <a href="#timetable" className="hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Activity Timetable</a>
            <a href="#features" className="hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Key Features</a>
            <Link to="/clubs" className="hover:text-purple-600 dark:hover:text-purple-400 transition-colors">Clubs Directory</Link>
          </div>

          <div className="flex items-center gap-3">
            {/* Theme Toggle Button */}
            <button
              onClick={toggleTheme}
              aria-label="Toggle theme"
              className="p-2 rounded-xl border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            >
              {theme === 'dark' ? (
                <Sun className="w-4 h-4 text-amber-400" />
              ) : (
                <Moon className="w-4 h-4 text-slate-600" />
              )}
            </button>

            <Link
              to="/login"
              className="text-xs sm:text-sm font-semibold text-slate-700 dark:text-slate-200 hover:text-purple-600 px-3 py-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="text-xs sm:text-sm font-semibold bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded-xl shadow-md hover:shadow-lg transition-all"
            >
              Get Started &rarr;
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative px-6 pt-16 pb-24 overflow-hidden">
        <div className="absolute top-10 right-10 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-10 left-5 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-6xl mx-auto relative z-10 text-center">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-purple-100 dark:bg-purple-950/70 border border-purple-200 dark:border-purple-800 text-purple-700 dark:text-purple-300 text-xs font-semibold mb-6">
            <BookOpen className="w-3.5 h-3.5" />
            Institutional Extracurricular &amp; Club Management Platform
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white max-w-4xl mx-auto leading-tight mb-6">
            Empowering Campus Life for{' '}
            <span className="bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
              Students &amp; Faculty
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto mb-10 leading-relaxed">
            A unified system where students explore clubs, submit joining requests to faculty coordinators, and check activity timetables &mdash; while faculty arrange candidates by department and approve them with colorful welcome letters.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 mb-16">
            <Link
              to="/register"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-2xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-sm shadow-xl hover:shadow-purple-500/25 transition-all"
            >
              <GraduationCap className="w-4 h-4" />
              Join as Student
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>

            <Link
              to="/login"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-2xl bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 border border-slate-200 dark:border-slate-800 font-semibold text-sm hover:border-purple-500 transition-all shadow-sm"
            >
              <Building2 className="w-4 h-4 text-purple-600 dark:text-purple-400" />
              Faculty Coordinator Access
            </Link>
          </div>

          {/* Quick Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
            {[
              { label: 'Active Campus Clubs', value: '50+' },
              { label: 'College Departments', value: '8 Disciplines' },
              { label: 'Weekly Timetable Labs', value: '35+ Slots' },
              { label: 'Verified Attendance', value: '100% Digital' }
            ].map((stat, idx) => (
              <div
                key={idx}
                className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm"
              >
                <p className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
                  {stat.value}
                </p>
                <p className="text-xs text-slate-500 dark:text-slate-400 font-medium mt-1">
                  {stat.label}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Dedicated Dual Portals Section */}
      <section id="portals" className="py-20 px-6 bg-slate-100/60 dark:bg-slate-900/40 border-y border-slate-200 dark:border-slate-800">
        <div className="max-w-6xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-14">
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white tracking-tight mb-3">
              Two Dedicated Campus Portals
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Purpose-built workflows tailored precisely for student participation and faculty supervision.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Student Card */}
            <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 shadow-sm flex flex-col justify-between hover:border-purple-300 dark:hover:border-purple-700/60 transition-all">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-purple-100 dark:bg-purple-950/70 border border-purple-200 dark:border-purple-800 flex items-center justify-center text-purple-700 dark:text-purple-300 mb-6">
                  <GraduationCap className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 mb-2">
                  Student Portal
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">
                  Discover clubs matching your domain, submit joining applications with custom motivation letters directly to faculty coordinators, and stay on top of weekly activities.
                </p>

                <div className="space-y-3 mb-8">
                  {[
                    'Explore clubs with faculty contact emails & descriptions',
                    'Direct email joining applications to faculty leads',
                    'Weekly activity timetable with venue, timings & seat reservation',
                    'Verified attendance transcript with attendance percentage'
                  ].map((perk, i) => (
                    <div key={i} className="flex items-start gap-2.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300">
                      <CheckCircle className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                      <span>{perk}</span>
                    </div>
                  ))}
                </div>
              </div>

              <Link
                to="/register"
                className="w-full py-3 px-4 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs sm:text-sm text-center inline-flex items-center justify-center gap-2 shadow-md transition-all"
              >
                Access Student Portal
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Faculty Coordinator Card */}
            <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 shadow-sm flex flex-col justify-between hover:border-purple-300 dark:hover:border-purple-700/60 transition-all">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-indigo-100 dark:bg-indigo-950/70 border border-indigo-200 dark:border-indigo-800 flex items-center justify-center text-indigo-700 dark:text-indigo-300 mb-6">
                  <Building2 className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-slate-100 mb-2">
                  Faculty Coordinator Hub
                </h3>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mb-6 leading-relaxed">
                  Supervise club cohorts, arrange registered applicants by college department, dispatch colorful acceptance emails, schedule timetable sessions, and verify student attendance.
                </p>

                <div className="space-y-3 mb-8">
                  {[
                    'Arrange & filter student applicants by College Department (CSE, ECE, MECH, etc.)',
                    'Accept invitations with colorful HTML welcome letters',
                    'Schedule and manage club weekly activity timetables',
                    'Mark & verify student session attendance (Present / Absent / Late)'
                  ].map((perk, i) => (
                    <div key={i} className="flex items-start gap-2.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300">
                      <CheckCircle className="w-4 h-4 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
                      <span>{perk}</span>
                    </div>
                  ))}
                </div>
              </div>

              <Link
                to="/login"
                className="w-full py-3 px-4 rounded-xl bg-slate-900 dark:bg-slate-800 hover:bg-slate-800 dark:hover:bg-slate-700 text-white font-semibold text-xs sm:text-sm text-center inline-flex items-center justify-center gap-2 shadow-md transition-all"
              >
                Sign In as Faculty Coordinator
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Activity Timetable Highlight Section */}
      <section id="timetable" className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-purple-600 dark:text-purple-400">
                Institutional Timetable
              </span>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white tracking-tight mt-1">
                Weekly Club Activity Schedule
              </h2>
            </div>
            <Link
              to="/student/dashboard"
              className="text-xs sm:text-sm font-semibold text-purple-600 dark:text-purple-400 hover:underline inline-flex items-center gap-1"
            >
              View Full Timetable in Portal &rarr;
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                day: 'Monday',
                time: '04:30 PM - 06:00 PM',
                club: 'Google Developer Student Club',
                title: 'Cloud Architecture & Gemini AI Workshop',
                venue: 'Turing Lab 301',
                type: 'Hands-on Lab'
              },
              {
                day: 'Wednesday',
                time: '04:00 PM - 05:30 PM',
                club: 'ACM Student Chapter',
                title: 'Competitive Programming: Graph Algorithms',
                venue: 'Algorithm Hall B',
                type: 'Problem Solving'
              },
              {
                day: 'Saturday',
                time: '10:00 AM - 01:00 PM',
                club: 'AI & Data Science Circle',
                title: 'Weekend Hackathon: Autonomous Agents',
                venue: 'Main Innovation Sandbox',
                type: 'Hackathon'
              }
            ].map((slot, i) => (
              <div
                key={i}
                className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm"
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-purple-100 dark:bg-purple-950/80 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800">
                    {slot.day}
                  </span>
                  <span className="text-xs font-medium px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                    {slot.type}
                  </span>
                </div>
                <h3 className="font-bold text-base text-slate-900 dark:text-slate-100 mb-1">
                  {slot.title}
                </h3>
                <p className="text-xs font-medium text-purple-600 dark:text-purple-400 mb-4">
                  {slot.club}
                </p>
                <div className="space-y-1.5 text-xs text-slate-500 dark:text-slate-400">
                  <div className="flex items-center gap-2">
                    <Clock className="w-3.5 h-3.5 text-slate-400" />
                    <span>{slot.time}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    <span>{slot.venue}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Key Features Section */}
      <section id="features" className="py-20 px-6 bg-slate-100/60 dark:bg-slate-900/40 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-6xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-14">
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white tracking-tight mb-3">
              Built for Modern Campus Governance
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              High-contrast accessibility, transparent communications, and automated verification.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {FEATURES.map((item, i) => {
              const IconComponent = item.icon;
              return (
                <div
                  key={i}
                  className="bg-white dark:bg-slate-900 p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm"
                >
                  <div className="w-10 h-10 rounded-xl bg-purple-100 dark:bg-purple-950/70 border border-purple-200 dark:border-purple-800 flex items-center justify-center text-purple-700 dark:text-purple-300 mb-4">
                    <IconComponent className="w-5 h-5" />
                  </div>
                  <h3 className="font-bold text-base text-slate-900 dark:text-slate-100 mb-2">
                    {item.title}
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                    {item.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-10 px-6 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 text-slate-600 dark:text-slate-400 text-xs">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-purple-600 rounded-md flex items-center justify-center text-white font-bold text-xs">
              C
            </div>
            <span className="font-bold text-slate-900 dark:text-slate-100">CCMS &bull; College Club Management System</span>
          </div>
          <p>&copy; {new Date().getFullYear()} CCMS. High-contrast Accessible Campus Edition.</p>
        </div>
      </footer>
    </div>
  );
}
