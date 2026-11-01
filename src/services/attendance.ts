import { supabase } from '../lib/supabase';
import type { Attendance } from '../types';

export const getStudentAttendance = async (studentId: string): Promise<Attendance[]> => {
  const { data, error } = await supabase
    .from('attendance')
    .select('*, events(title, event_date, venue, clubs(name))')
    .eq('student_id', studentId)
    .order('marked_at', { ascending: false });
  if (error) throw error;
  return data as any;
};

export const getEventAttendance = async (eventId: string): Promise<Attendance[]> => {
  const { data, error } = await supabase
    .from('attendance')
    .select('*, profiles(id, full_name, email, department, student_id)')
    .eq('event_id', eventId);
  if (error) throw error;
  return data as any;
};

export const markAttendance = async (eventId: string, studentId: string, status: 'present' | 'absent' | 'late') => {
  const { data, error } = await supabase
    .from('attendance')
    .upsert(
      { event_id: eventId, student_id: studentId, status, marked_at: new Date().toISOString() },
      { onConflict: 'event_id,student_id' }
    )
    .select()
    .single();
  if (error) throw error;
  return data;
};

