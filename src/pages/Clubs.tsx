import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getClubs, getCategories } from '../services/clubs';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import type { Club, ClubCategory } from '../types';
import { Sparkles, Sun, Moon, Search, Compass, ArrowRight, ArrowLeft } from 'lucide-react';

export default function Clubs() {
  const { profile } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [clubs, setClubs] = useState<Club[]>([]);
  const [categories, setCategories] = useState<ClubCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    Promise.all([getClubs(), getCategories()])
      .then(([c, cat]) => {
        setClubs(c);
        setCategories(cat);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const filtered = clubs.filter((c) => {
    const matchSearch =
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      (c.description ?? '').toLowerCase().includes(search.toLowerCase());
    const matchCat = filter === 'all' || c.category_id === filter;
    return matchSearch && matchCat;
  });

  const backLink =
    profile?.role === 'coordinator'
      ? '/coordinator/dashboard'
      : profile?.role === 'student'
      ? '/student/dashboard'
      : '/';

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-200">
      {/* Top Bar */}
      <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur border-b border-slate-200 dark:border-slate-800 px-6 py-4 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-700 to-indigo-700 rounded-lg flex items-center justify-center text-white font-bold text-sm shadow-sm">
              <Sparkles className="w-4 h-4 text-purple-200" />
            </div>
            <span className="font-bold text-slate-900 dark:text-white text-base">CCMS</span>
          </Link>

          <div className="flex items-center gap-4">
            <button
              onClick={toggleTheme}
              aria-label="Toggle theme"
              className="p-2 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
            </button>
            <Link
              to={backLink}
              className="inline-flex items-center gap-1.5 text-xs sm:text-sm font-semibold text-purple-600 dark:text-purple-400 hover:underline"
            >
              <ArrowLeft className="w-4 h-4" />
              Back to Dashboard
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="mb-10">
          <span className="text-xs font-bold uppercase tracking-widest text-purple-600 dark:text-purple-400 block mb-2">
            Campus Catalog
          </span>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-3">
            Explore Campus Clubs
          </h1>
          <p className="text-sm text-slate-600 dark:text-slate-400 max-w-xl leading-relaxed">
            Discover student communities across technology, creative arts, robotics, and leadership. Apply to join and meet faculty coordinators.
          </p>
        </div>

        {/* Search + filter */}
        <div className="flex flex-col sm:flex-row gap-3 mb-10">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search clubs by name or keywords..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-xl text-sm bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 shadow-sm"
            />
          </div>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-3 rounded-xl text-sm bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 shadow-sm"
          >
            <option value="all">All Domains &amp; Categories</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 animate-pulse">
                <div className="h-5 bg-slate-200 dark:bg-slate-800 rounded mb-3 w-2/3" />
                <div className="h-3 bg-slate-100 dark:bg-slate-800/60 rounded mb-2" />
                <div className="h-3 bg-slate-100 dark:bg-slate-800/60 rounded w-3/4" />
              </div>
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-20 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
            <Compass className="w-12 h-12 text-slate-400 mx-auto mb-3" />
            <p className="text-slate-900 dark:text-slate-100 font-semibold">No clubs found matching your search.</p>
            <button
              onClick={() => {
                setSearch('');
                setFilter('all');
              }}
              className="mt-3 text-purple-600 dark:text-purple-400 text-sm font-semibold hover:underline"
            >
              Clear filters
            </button>
          </div>
        ) : (
          <>
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-5 font-medium">
              {filtered.length} club{filtered.length !== 1 ? 's' : ''} active on campus
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filtered.map((club) => {
                const cat = categories.find((c) => c.id === club.category_id);
                return (
                  <div
                    key={club.id}
                    className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 hover:shadow-lg transition-all flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-start justify-between mb-4">
                        <div className="w-11 h-11 bg-purple-100 dark:bg-purple-950/70 border border-purple-200 dark:border-purple-800 rounded-xl flex items-center justify-center text-lg font-bold text-purple-700 dark:text-purple-300">
                          {club.name.charAt(0)}
                        </div>
                        {cat && (
                          <span className="text-xs bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 font-medium px-2.5 py-1 rounded-full">
                            {cat.name}
                          </span>
                        )}
                      </div>

                      <h3 className="font-bold text-slate-900 dark:text-white text-base mb-2">
                        {club.name}
                      </h3>
                      <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 line-clamp-3 mb-4 leading-relaxed">
                        {club.description || 'Dedicated campus club fostering student innovation.'}
                      </p>
                    </div>

                    <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                      <div className="text-[11px] text-slate-500 dark:text-slate-400 truncate max-w-[170px]">
                        Faculty: {club.faculty_coordinator || 'Assigned Lead'}
                      </div>
                      <Link
                        to={`/clubs/${club.slug}`}
                        className="inline-flex items-center gap-1 text-xs font-semibold text-purple-600 dark:text-purple-400 hover:underline"
                      >
                        Details
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
