import { supabase } from '../lib/supabase';
import { Club, ClubCategory } from '../types';

export const getClubs = async (): Promise<Club[]> => {
  const { data, error } = await supabase.from('clubs').select('*');
  if (error) throw error;
  return data as Club[];
};

export const getCategories = async (): Promise<ClubCategory[]> => {
  const { data, error } = await supabase.from('club_categories').select('*');
  if (error) throw error;
  return data as ClubCategory[];
};

export const getClubBySlug = async (slug: string): Promise<Club | null> => {
  const { data, error } = await supabase.from('clubs').select('*').eq('slug', slug).single();
  if (error) throw error;
  return data as Club;
};
