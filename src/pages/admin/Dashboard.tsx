import { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Navbar } from '../../components/layout/Navbar';
import { getAllProfiles, getAllClubs, createClub, deleteClub, assignCoordinator } from '../../services/admin';
import { getCategories } from '../../services/clubs';
import type { Profile, ClubCategory } from '../../types';

const JM = { fontFamily: 'JetBrains Mono, monospace' };
const IN = { fontFamily: 'Inter, sans-serif' };
type Tab = 'clubs' | 'users' | 'assign';

export default function AdminDashboard() {
  const { profile } = useAuth();
  const [tab, setTab]             = useState<Tab>('clubs');
  const [profiles, setProfiles]   = useState<Profile[]>([]);
  const [clubs, setClubs]         = useState<any[]>([]);
  const [categories, setCategories] = useState<ClubCategory[]>([]);
  const [loading, setLoading]     = useState(true);

  const [showClubForm, setShowClubForm] = useState(false);
  const [clubForm, setClubForm] = useState({ name:'', slug:'', description:'', category_id:'', faculty_coordinator:'', contact_email:'' });
  const [clubSaving, setClubSaving] = useState(false);

  const [assignClubId, setAssignClubId] = useState('');
  const [assignUserId, setAssignUserId] = useState('');
  const [assigning, setAssigning]       = useState(false);
  const [assignMsg, setAssignMsg]       = useState('');

  useEffect(() => {
    Promise.all([getAllProfiles(), getAllClubs(), getCategories()])
      .then(([p, c, cat]) => { setProfiles(p); setClubs(c); setCategories(cat); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const handleCreateClub = async (e: React.FormEvent) => {
    e.preventDefault(); setClubSaving(true);
    try {
      const created = await createClub({ name: clubForm.name, slug: clubForm.slug.toLowerCase().replace(/\s+/g,'-'),
        description: clubForm.description, category_id: clubForm.category_id,
        faculty_coordinator: clubForm.faculty_coordinator, contact_email: clubForm.contact_email,
        logo_url:'', cover_url:'', status:'approved' });
      setClubs((p) => [{ ...created, club_categories: categories.find((c) => c.id === clubForm.category_id) }, ...p]);
      setShowClubForm(false);
      setClubForm({ name:'', slug:'', description:'', category_id:'', faculty_coordinator:'', contact_email:'' });
    } catch (err: any) { alert(err.message); } finally { setClubSaving(false); }
  };

  const handleAssign = async (e: React.FormEvent) => {
    e.preventDefault(); setAssigning(true); setAssignMsg('');
    try { await assignCoordinator(assignClubId, assignUserId); setAssignMsg('✓ Coordinator assigned successfully.'); setAssignClubId(''); setAssignUserId(''); }
    catch (err: any) { setAssignMsg(err.message || 'Error assigning coordinator'); } finally { setAssigning(false); }
  };

  const coordinators = profiles.filter((p) => p.role === 'coordinator');
  const students     = profiles.filter((p) => p.role === 'student');

  const stats = [
    { icon: '🏫', label: 'Total Clubs',   value: clubs.length,        color: 'bg-brand-pale/40' },
    { icon: '👥', label: 'Total Users',   value: profiles.length,     color: 'bg-brand-light/20' },
    { icon: '🧑‍🎓', label: 'Students',     value: students.length,     color: 'bg-green-100' },
    { icon: '🧑‍💼', label: 'Coordinators', value: coordinators.length, color: 'bg-blue-50' },
  ];

  const roleColors: Record<string, string> = {
    admin:       'bg-brand-pale/60 text-brand-deep',
    coordinator: 'bg-brand-mid/20 text-brand-deep',
    student:     'bg-brand-pale/30 text-brand-deep',
  };

  const inputCls = "w-full border border-brand-pale bg-white rounded-xl px-3 py-2.5 text-sm text-[#1a0a28] focus:outline-none focus:ring-2 focus:ring-brand-mid/40 focus:border-brand-mid";

  return (
    <div className="min-h-screen bg-brand-cream">
      <Navbar />
      <div className="max-w-6xl mx-auto px-6 py-8">

        {/* Banner */}
        <div className="bg-brand-deep rounded-2xl p-8 mb-8 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl" />
          <div className="relative">
            <p className="text-purple-300 text-sm font-medium mb-1" style={IN}>Admin Dashboard</p>
            <h1 className="text-3xl font-bold text-white mb-1" style={JM}>Hello, {profile?.full_name} 🛡️</h1>
            <p className="text-purple-300 text-sm" style={IN}>Manage clubs, users, and coordinator assignments across the system.</p>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {stats.map((s) => (
            <div key={s.label} className={`${s.color} rounded-2xl p-5 border border-brand-pale/30`}>
              <div className="text-2xl mb-2">{s.icon}</div>
              <p className="text-2xl font-bold text-[#1a0a28]" style={JM}>{loading ? '—' : s.value}</p>
              <p className="text-xs text-[#3d2558] mt-0.5" style={IN}>{s.label}</p>
            </div>
          ))}
        </div>

        <div className="bg-white rounded-2xl border border-brand-pale/40 overflow-hidden">
          {/* Tabs */}
          <div className="flex border-b border-brand-pale/30 px-6">
            {(['clubs','users','assign'] as Tab[]).map((t) => (
              <button key={t} onClick={() => setTab(t)}
                className={`py-4 px-5 text-sm font-semibold border-b-2 transition-all capitalize ${tab === t ? 'border-brand-deep text-brand-deep' : 'border-transparent text-[#6b5080] hover:text-[#3d2558]'}`} style={IN}>
                {t === 'assign' ? 'Assign Coordinator' : t}
              </button>
            ))}
          </div>

          <div className="p-6">
            {loading ? (
              <div className="flex justify-center py-12">
                <div className="w-6 h-6 border-2 border-brand-deep border-t-transparent rounded-full animate-spin" />
              </div>
            ) : (
              <>
                {/* CLUBS */}
                {tab === 'clubs' && (
                  <div>
                    <div className="flex justify-between items-center mb-5">
                      <h3 className="font-bold text-[#1a0a28]" style={JM}>Clubs ({clubs.length})</h3>
                      <button onClick={() => setShowClubForm((v) => !v)}
                        className={`text-sm font-semibold px-5 py-2 rounded-full transition-all ${showClubForm ? 'bg-gray-100 text-[#3d2558]' : 'bg-brand-deep text-white hover:bg-purple-900'}`} style={IN}>
                        {showClubForm ? '✕ Cancel' : '+ New Club'}
                      </button>
                    </div>

                    {showClubForm && (
                      <form onSubmit={handleCreateClub} className="bg-brand-cream rounded-2xl border border-brand-pale/30 p-6 mb-6 space-y-4">
                        <h4 className="font-bold text-[#1a0a28]" style={JM}>New Club</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {[{l:'Club Name *',k:'name',t:'text',r:true,ph:'e.g. Robotics Club'},{l:'Slug *',k:'slug',t:'text',r:true,ph:'e.g. robotics-club'},{l:'Faculty Coordinator',k:'faculty_coordinator',t:'text',r:false,ph:''},{l:'Contact Email',k:'contact_email',t:'email',r:false,ph:''}].map(({l,k,t,r,ph}) => (
                            <div key={k}>
                              <label className="text-xs font-semibold text-[#3d2558] mb-1 block" style={IN}>{l}</label>
                              <input required={r} type={t} placeholder={ph} value={(clubForm as any)[k]} onChange={(e) => setClubForm((p) => ({...p,[k]:e.target.value}))} className={inputCls} />
                            </div>
                          ))}
                          <div>
                            <label className="text-xs font-semibold text-[#3d2558] mb-1 block" style={IN}>Category</label>
                            <select value={clubForm.category_id} onChange={(e) => setClubForm((p) => ({...p,category_id:e.target.value}))} className={inputCls}>
                              <option value="">— Select —</option>
                              {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
                            </select>
                          </div>
                        </div>
                        <div>
                          <label className="text-xs font-semibold text-[#3d2558] mb-1 block" style={IN}>Description</label>
                          <textarea value={clubForm.description} onChange={(e) => setClubForm((p) => ({...p,description:e.target.value}))} rows={2} className={inputCls} />
                        </div>
                        <button type="submit" disabled={clubSaving} className="bg-brand-deep text-white font-semibold px-6 py-2.5 rounded-full hover:bg-purple-900 disabled:opacity-60 transition-colors text-sm" style={IN}>
                          {clubSaving ? 'Creating...' : 'Create Club'}
                        </button>
                      </form>
                    )}

                    {clubs.length === 0 ? (
                      <div className="text-center py-12"><div className="text-4xl mb-3">🏫</div><p className="text-[#6b5080] text-sm" style={IN}>No clubs yet.</p></div>
                    ) : (
                      <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                          <thead>
                            <tr className="text-left border-b border-brand-pale/30 text-xs font-bold text-[#6b5080] uppercase tracking-wide" style={JM}>
                              <th className="pb-3">Name</th><th className="pb-3">Category</th><th className="pb-3">Contact</th><th className="pb-3">Status</th><th className="pb-3">Actions</th>
                            </tr>
                          </thead>
                          <tbody>
                            {clubs.map((c: any) => (
                              <tr key={c.id} className="border-b border-brand-pale/20 last:border-0 hover:bg-brand-cream/50 transition-colors">
                                <td className="py-3 font-semibold text-[#1a0a28]" style={IN}>{c.name}</td>
                                <td className="py-3 text-[#3d2558]" style={IN}>{c.club_categories?.name || '—'}</td>
                                <td className="py-3 text-[#3d2558]" style={IN}>{c.contact_email || '—'}</td>
                                <td className="py-3"><span className="text-xs bg-green-100 text-green-800 font-semibold px-2.5 py-0.5 rounded-full" style={IN}>{c.status}</span></td>
                                <td className="py-3"><button onClick={async () => { if(!confirm('Delete this club?')) return; await deleteClub(c.id); setClubs((p) => p.filter((x) => x.id !== c.id)); }} className="text-xs text-brand-deep hover:underline font-medium" style={IN}>Delete</button></td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </div>
                )}

                {/* USERS */}
                {tab === 'users' && (
                  <div>
                    <h3 className="font-bold text-[#1a0a28] mb-5" style={JM}>All Users ({profiles.length})</h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="text-left border-b border-brand-pale/30 text-xs font-bold text-[#6b5080] uppercase tracking-wide" style={JM}>
                            <th className="pb-3">Name</th><th className="pb-3">Email</th><th className="pb-3">Role</th><th className="pb-3">Joined</th>
                          </tr>
                        </thead>
                        <tbody>
                          {profiles.map((p) => (
                            <tr key={p.id} className="border-b border-brand-pale/20 last:border-0 hover:bg-brand-cream/50 transition-colors">
                              <td className="py-3">
                                <div className="flex items-center gap-3">
                                  <div className="w-8 h-8 bg-brand-pale/40 rounded-lg flex items-center justify-center text-brand-deep font-bold text-xs shrink-0" style={JM}>{p.full_name?.charAt(0) || '?'}</div>
                                  <span className="font-semibold text-[#1a0a28]" style={IN}>{p.full_name || '—'}</span>
                                </div>
                              </td>
                              <td className="py-3 text-[#3d2558]" style={IN}>{p.email}</td>
                              <td className="py-3"><span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${roleColors[p.role] ?? 'bg-gray-100 text-gray-600'}`} style={IN}>{p.role}</span></td>
                              <td className="py-3 text-[#6b5080]" style={IN}>{p.created_at ? new Date(p.created_at).toLocaleDateString() : '—'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* ASSIGN */}
                {tab === 'assign' && (
                  <div className="max-w-lg">
                    <h3 className="font-bold text-[#1a0a28] mb-2" style={JM}>Assign Coordinator to Club</h3>
                    <p className="text-sm text-[#3d2558] mb-6" style={IN}>Link a coordinator account to a club so they can manage it.</p>
                    <form onSubmit={handleAssign} className="space-y-4">
                      <div>
                        <label className="text-xs font-semibold text-[#3d2558] mb-1.5 block" style={IN}>Select Club</label>
                        <select required value={assignClubId} onChange={(e) => setAssignClubId(e.target.value)} className={inputCls}>
                          <option value="">— Choose a club —</option>
                          {clubs.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
                        </select>
                      </div>
                      <div>
                        <label className="text-xs font-semibold text-[#3d2558] mb-1.5 block" style={IN}>Select Coordinator</label>
                        <select required value={assignUserId} onChange={(e) => setAssignUserId(e.target.value)} className={inputCls}>
                          <option value="">— Choose a coordinator —</option>
                          {coordinators.map((c) => <option key={c.id} value={c.id}>{c.full_name} ({c.email})</option>)}
                        </select>
                        {coordinators.length === 0 && <p className="text-xs text-[#6b5080] mt-1" style={IN}>No coordinators registered yet.</p>}
                      </div>
                      <button type="submit" disabled={assigning} className="bg-brand-deep text-white font-semibold px-6 py-2.5 rounded-full hover:bg-purple-900 disabled:opacity-60 transition-colors text-sm" style={IN}>
                        {assigning ? 'Assigning...' : 'Assign Coordinator'}
                      </button>
                      {assignMsg && (
                        <div className={`text-sm px-4 py-3 rounded-xl ${assignMsg.startsWith('✓') ? 'bg-green-50 text-green-800 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'}`} style={IN}>{assignMsg}</div>
                      )}
                    </form>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
