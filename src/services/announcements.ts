import { supabase } from '../lib/supabase';
import type { Announcement } from '../types';

export const getClubAnnouncements = async (clubId: string): Promise<Announcement[]> => {
  const { data, error } = await supabase
    .from('announcements')
    .select('*')
    .eq('club_id', clubId)
    .order('created_at', { ascending: false });
  if (error) throw error;
  return data as Announcement[];
};

export const createAnnouncement = async (announcement: Omit<Announcement, 'id' | 'created_at'>) => {
  const { data, error } = await supabase.from('announcements').insert(announcement).select().single();
  if (error) throw error;
  return data as Announcement;
};

export const deleteAnnouncement = async (id: string) => {
  const { error } = await supabase.from('announcements').delete().eq('id', id);
  if (error) throw error;
};
