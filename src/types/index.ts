export type Role = 'student' | 'coordinator' | 'admin';

export interface Profile {
  id: string;
  full_name: string;
  email: string;
  role: Role;
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
  created_at: string;
}

export interface EventRegistration {
  id: string;
  event_id: string;
  student_id: string;
  registered_at: string;
}

export interface Attendance {
  id: string;
  event_id: string;
  student_id: string;
  status: 'present' | 'absent' | 'late';
  marked_at: string;
}

export interface Announcement {
  id: string;
  club_id: string;
  title: string;
  content: string;
  created_at: string;
}
