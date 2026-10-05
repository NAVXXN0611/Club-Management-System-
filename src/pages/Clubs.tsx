import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getClubs, getCategories } from '../services/clubs';
import { Club, ClubCategory } from '../types';

export default function Clubs() {
  const [clubs, setClubs] = useState<Club[]>([]);
  const [categories, setCategories] = useState<ClubCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    Promise.all([getClubs(), getCategories()]).then(([clubsData, categoriesData]) => {
      setClubs(clubsData);
      setCategories(categoriesData);
      setLoading(false);
    }).catch(console.error);
  }, []);

  const filteredClubs = clubs.filter(c => {
    const matchesSearch = c.name.toLowerCase().includes(search.toLowerCase());
    const matchesCat = filter === 'all' || c.category_id === filter;
    return matchesSearch && matchesCat;
  });

  if (loading) return <div className="p-8 text-center">Loading clubs...</div>;

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Explore Clubs</h1>
        <Link to="/student/dashboard" className="text-primary hover:underline">Back to Dashboard</Link>
      </div>

      <div className="flex gap-4 mb-8">
        <input 
          type="text" 
          placeholder="Search clubs..." 
          className="border p-2 rounded flex-1"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <select 
          className="border p-2 rounded"
          value={filter}
          onChange={e => setFilter(e.target.value)}
        >
          <option value="all">All Categories</option>
          {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredClubs.map(club => (
          <div key={club.id} className="border rounded-lg p-6 bg-white shadow-sm hover:shadow-md transition">
            <h2 className="text-xl font-semibold mb-2">{club.name}</h2>
            <p className="text-gray-600 mb-4 h-12 overflow-hidden">{club.description || 'No description available.'}</p>
            <Link to={`/clubs/${club.slug}`} className="text-primary font-medium hover:underline">
              View Club &rarr;
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
