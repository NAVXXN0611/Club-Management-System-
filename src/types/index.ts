export type Role = 'student' | 'coordinator' | 'admin';

export interface Profile {
  id: string;
  full_name: string;
  email: string;
  role: Role;
  created_at?: string;
  updated_at?: string;
}
