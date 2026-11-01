import { supabase } from '../lib/supabase';
import type { Club, Profile, ClubCategory } from '../types';

export const getAllProfiles = async (): Promise<Profile[]> => {
  const { data, error } = await supabase.from('profiles').select('*').order('created_at', { ascending: false });
  if (error) throw error;
  return data as Profile[];
};

export const getAllClubs = async (): Promise<(Club & { club_categories: { name: string } | null })[]> => {
  const { data, error } = await supabase
    .from('clubs')
    .select('*, club_categories(name)')
    .order('created_at', { ascending: false });
  if (error) throw error;
  return data as any;
};

export const createClub = async (club: Omit<Club, 'id' | 'created_at'>) => {
  const { data, error } = await supabase.from('clubs').insert(club).select().single();
  if (error) throw error;
  return data as Club;
};

export const deleteClub = async (id: string) => {
  const { error } = await supabase.from('events').delete().eq('club_id', id);
  if (error) console.warn('Cleaned events', error);
  const { error: delErr } = await supabase.from('clubs').delete().eq('id', id);
  if (delErr) throw delErr;
};

export const createCategory = async (name: string, description: string) => {
  const { data, error } = await supabase.from('club_categories').insert({ name, description }).select().single();
  if (error) throw error;
  return data as ClubCategory;
};

export const assignCoordinator = async (clubId: string, coordinatorId: string) => {
  const { error } = await supabase.from('club_coordinators').insert({ club_id: clubId, coordinator_id: coordinatorId });
  if (error) throw error;
};

export const getCoordinatorClubs = async (coordinatorId: string): Promise<Club[]> => {
  // First attempt junction lookup
  const { data, error } = await supabase
    .from('club_coordinators')
    .select('clubs(*)')
    .eq('coordinator_id', coordinatorId);
  
  if (!error && data && data.length > 0) {
    const list = data.map((d: any) => d.clubs).filter(Boolean);
    if (list.length > 0) return list;
  }

  // Fallback: return all clubs so faculty coordinator can select and manage their club
  const { data: allClubs, error: fallbackErr } = await supabase.from('clubs').select('*').order('name');
  if (fallbackErr) throw fallbackErr;
  return (allClubs as Club[]) || [];
};
