export type Role = 'student' | 'coordinator' | 'admin';

export interface Profile {
  id: string;
  full_name: string;
  email: string;
  role: Role;
  student_id?: string;
  department?: string;
  year?: string;
  phone?: string;
  avatar_url?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ClubCategory {
  id: string;
  name: string;
  description: string;
}

export interface Club {
  id: string;
  name: string;
  slug: string;
  description: string;
  category_id: string;
  logo_url: string;
  cover_url: string;
  faculty_coordinator: string;
  contact_email: string;
  status: string;
  created_at: string;
}

export interface ClubMembership {
  id: string;
  student_id: string;
  club_id: string;
  status: 'pending' | 'approved' | 'rejected';
  applied_at: string;
  approved_at?: string;
  clubs?: {
    name: string;
    slug: string;
    description?: string;
    faculty_coordinator?: string;
    contact_email?: string;
  };
  profiles?: Profile;
}

export interface Event {
  id: string;
  club_id: string;
  title: string;
  description: string;
  event_date: string;
  start_time: string;
  end_time: string;
  venue: string;
  capacity: number;
  registration_open: boolean;
  day_of_week?: string;
  activity_type?: 'weekly_session' | 'workshop' | 'hackathon' | 'competition' | 'guest_lecture';
  created_at: string;
}

export interface EventRegistration {
  id: string;
  event_id: string;
  student_id: string;
  registered_at: string;
  events?: Event & { clubs?: { name: string; slug?: string } };
  profiles?: Profile;
}

export interface Announcement {
  id: string;
  club_id: string;
  title: string;
  content: string;
  created_at: string;
  clubs?: { name: string };
}

export interface Attendance {
  id: string;
  event_id: string;
  student_id: string;
  status: 'present' | 'absent' | 'late';
  marked_at: string;
  events?: Event;
  profiles?: Profile;
}

export interface TimetableSlot {
  id: string;
  club_id: string;
  club_name: string;
  day: string;
  time: string;
  activity: string;
  venue: string;
  type: string;
  faculty_coordinator: string;
  faculty_email: string;
}
