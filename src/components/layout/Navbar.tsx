import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import { Sun, Moon, LogOut, Compass, Sparkles } from 'lucide-react';

export function Navbar() {
  const { profile, signOut } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    await signOut();
    navigate('/');
  };

  const dashboardLink = profile?.role === 'coordinator' ? '/coordinator/dashboard' : '/student/dashboard';
  const roleLabel = profile?.role === 'coordinator' ? 'Faculty Coordinator' : 'Student';

  return (
    <nav className="bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-6 py-3.5 sticky top-0 z-40 transition-colors duration-200">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link to={dashboardLink} className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-700 to-indigo-700 rounded-lg flex items-center justify-center text-white font-bold text-sm shadow-sm group-hover:scale-105 transition-transform">
              <Sparkles className="w-4 h-4 text-purple-200" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-slate-900 dark:text-white tracking-tight leading-none text-base">CCMS</span>
              <span className="text-[10px] text-purple-600 dark:text-purple-400 font-medium">Campus Portal</span>
            </div>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            <Link
              to={dashboardLink}
              className="text-xs font-semibold px-3 py-1.5 rounded-lg text-slate-600 dark:text-slate-300 hover:text-purple-600 dark:hover:text-purple-400 hover:bg-slate-100 dark:hover:bg-slate-800/60 transition-colors"
            >
              Dashboard
            </Link>
            <Link
              to="/clubs"
              className="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg text-slate-600 dark:text-slate-300 hover:text-purple-600 dark:hover:text-purple-400 hover:bg-slate-100 dark:hover:bg-slate-800/60 transition-colors"
            >
              <Compass className="w-3.5 h-3.5" />
              Explore Clubs
            </Link>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Theme Toggle Button */}
          <button
            onClick={toggleTheme}
            aria-label="Toggle theme"
            className="p-2 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          >
            {theme === 'dark' ? (
              <Sun className="w-4 h-4 text-amber-400" />
            ) : (
              <Moon className="w-4 h-4 text-slate-600" />
            )}
          </button>

          {/* User & Role Badge */}
          <div className="flex items-center gap-2.5 pl-2 border-l border-slate-200 dark:border-slate-800">
            <div className="hidden sm:flex flex-col text-right">
              <span className="text-xs font-semibold text-slate-900 dark:text-slate-100 leading-tight">
                {profile?.full_name || 'Member'}
              </span>
              <span className="text-[11px] text-slate-500 dark:text-slate-400 leading-tight">
                {profile?.department ? `${profile.department}` : roleLabel}
              </span>
            </div>

            <span
              className={`text-[11px] font-bold px-2.5 py-1 rounded-full border ${
                profile?.role === 'coordinator'
                  ? 'bg-purple-100 dark:bg-purple-950/70 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800'
                  : 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800'
              }`}
            >
              {profile?.role === 'coordinator' ? 'Faculty' : 'Student'}
            </span>
          </div>

          {/* Sign Out Button */}
          <button
            onClick={handleSignOut}
            className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-600 dark:text-slate-300 hover:text-red-600 dark:hover:text-red-400 border border-slate-200 dark:border-slate-800 hover:border-red-300 dark:hover:border-red-900/50 px-3 py-1.5 rounded-lg transition-colors ml-1"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </nav>
  );
}
