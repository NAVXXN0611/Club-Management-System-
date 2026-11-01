import { supabase } from '../lib/supabase';
import type { Event, EventRegistration } from '../types';

export const getClubEvents = async (clubId: string): Promise<Event[]> => {
  const { data, error } = await supabase
    .from('events')
    .select('*')
    .eq('club_id', clubId)
    .order('event_date', { ascending: true });
  if (error) throw error;
  return data as Event[];
};

export const getAllUpcomingEvents = async (): Promise<(Event & { clubs: { name: string; slug: string } })[]> => {
  const today = new Date().toISOString().split('T')[0];
  const { data, error } = await supabase
    .from('events')
    .select('*, clubs(name, slug)')
    .gte('event_date', today)
    .order('event_date', { ascending: true })
    .limit(10);
  if (error) throw error;
  return data as any;
};

export const createEvent = async (event: Omit<Event, 'id' | 'created_at'>) => {
  const { data, error } = await supabase.from('events').insert(event).select().single();
  if (error) throw error;
  return data as Event;
};

export const updateEvent = async (id: string, event: Partial<Event>) => {
  const { error } = await supabase.from('events').update(event).eq('id', id);
  if (error) throw error;
};

export const deleteEvent = async (id: string) => {
  const { error } = await supabase.from('events').delete().eq('id', id);
  if (error) throw error;
};

export const getMyEventRegistrations = async (studentId: string): Promise<(EventRegistration & { events: Event & { clubs: { name: string } } })[]> => {
  const { data, error } = await supabase
    .from('event_registrations')
    .select('*, events(*, clubs(name))')
    .eq('student_id', studentId);
  if (error) throw error;
  return data as any;
};

export const registerForEvent = async (eventId: string, studentId: string) => {
  const { error } = await supabase.from('event_registrations').insert({ event_id: eventId, student_id: studentId });
  if (error) throw error;
};

export const getEventRegistrations = async (eventId: string): Promise<(EventRegistration & { profiles: { full_name: string; email: string } })[]> => {
  const { data, error } = await supabase
    .from('event_registrations')
    .select('*, profiles(full_name, email)')
    .eq('event_id', eventId);
  if (error) throw error;
  return data as any;
};
