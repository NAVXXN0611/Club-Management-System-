import { supabase } from '../lib/supabase';
import type { ClubMembership } from '../types';

export const getMyMemberships = async (studentId: string): Promise<(ClubMembership & { clubs: { name: string; slug: string; description?: string; faculty_coordinator?: string; contact_email?: string } })[]> => {
  const { data, error } = await supabase
    .from('club_memberships')
    .select('*, clubs(name, slug, description, faculty_coordinator, contact_email)')
    .eq('student_id', studentId);
  if (error) throw error;
  return data as any;
};

export const getClubMemberships = async (clubId: string): Promise<(ClubMembership & { profiles: { id: string; full_name: string; email: string; department?: string; student_id?: string; year?: string; phone?: string } })[]> => {
  const { data, error } = await supabase
    .from('club_memberships')
    .select('*, profiles(id, full_name, email, department, student_id, year, phone)')
    .eq('club_id', clubId)
    .order('applied_at', { ascending: false });
  if (error) throw error;
  return data as any;
};

export const applyForClubMembership = async (clubId: string, studentId: string) => {
  const { data, error } = await supabase
    .from('club_memberships')
    .insert({ club_id: clubId, student_id: studentId, status: 'pending' })
    .select()
    .single();
  if (error) throw error;
  return data;
};

export const updateMembershipStatus = async (id: string, status: 'approved' | 'rejected') => {
  const { error } = await supabase
    .from('club_memberships')
    .update({ status, approved_at: status === 'approved' ? new Date().toISOString() : null })
    .eq('id', id);
  if (error) throw error;
};
