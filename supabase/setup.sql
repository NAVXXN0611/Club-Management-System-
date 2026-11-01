-- Run this entire script in your Supabase SQL Editor

-----------------------------------------
-- 1. PROFILES
-----------------------------------------
CREATE TABLE IF NOT EXISTS public.profiles (
    id uuid references auth.users on delete cascade not null primary key,
    full_name text,
    email text,
    role text default 'student'::text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id);
-- Admins can view all profiles
CREATE POLICY "Admins can view all profiles" ON public.profiles FOR SELECT USING (
  EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
);

-- Create profile rows from Auth user metadata. This runs with definer rights so
-- profile creation does not depend on a browser session during email signup.
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, email, role)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data ->> 'full_name', ''),
    NEW.email,
    COALESCE(NULLIF(NEW.raw_user_meta_data ->> 'role', ''), 'student')
  )
  ON CONFLICT (id) DO UPDATE
  SET
    full_name = EXCLUDED.full_name,
    email = EXCLUDED.email,
    role = EXCLUDED.role,
    updated_at = timezone('utc'::text, now());

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

INSERT INTO public.profiles (id, full_name, email, role)
SELECT
  users.id,
  COALESCE(users.raw_user_meta_data ->> 'full_name', ''),
  users.email,
  COALESCE(NULLIF(users.raw_user_meta_data ->> 'role', ''), 'student')
FROM auth.users
LEFT JOIN public.profiles ON profiles.id = users.id
WHERE profiles.id IS NULL;

-----------------------------------------
-- 2. CLUB CATEGORIES
-----------------------------------------
CREATE TABLE IF NOT EXISTS public.club_categories (
    id uuid default gen_random_uuid() primary key,
    name text not null,
    description text
);
ALTER TABLE public.club_categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Categories are viewable by everyone" ON public.club_categories FOR SELECT USING (true);
CREATE POLICY "Only admins can modify categories" ON public.club_categories FOR ALL USING (
  EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
);

-----------------------------------------
-- 3. CLUBS
-----------------------------------------
CREATE TABLE IF NOT EXISTS public.clubs (
    id uuid default gen_random_uuid() primary key,
    name text not null,
    slug text unique not null,
    description text,
    category_id uuid references public.club_categories on delete set null,
    logo_url text,
    cover_url text,
    faculty_coordinator text,
    contact_email text,
    status text default 'approved',
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);
ALTER TABLE public.clubs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Clubs are viewable by everyone" ON public.clubs FOR SELECT USING (true);
CREATE POLICY "Only admins can modify clubs" ON public.clubs FOR ALL USING (
  EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
);
-- Allow coordinators to update their assigned club (we need a linking table for coordinator assignments)

-----------------------------------------
-- 4. CLUB COORDINATORS (Link table)
-----------------------------------------
CREATE TABLE IF NOT EXISTS public.club_coordinators (
    id uuid default gen_random_uuid() primary key,
    club_id uuid references public.clubs on delete cascade not null,
    coordinator_id uuid references public.profiles on delete cascade not null,
    UNIQUE(club_id, coordinator_id)
);
ALTER TABLE public.club_coordinators ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Viewable by everyone" ON public.club_coordinators FOR SELECT USING (true);
CREATE POLICY "Admins can manage coordinators" ON public.club_coordinators FOR ALL USING (
  EXISTS (SELECT 1 FROM public.profiles WHERE id = auth.uid() AND role = 'admin')
);

-- Update clubs policy to allow assigned coordinators to update the club
CREATE POLICY "Coordinators can update their clubs" ON public.clubs FOR UPDATE USING (
  EXISTS (SELECT 1 FROM public.club_coordinators WHERE club_id = id AND coordinator_id = auth.uid())
);

-----------------------------------------
-- 5. CLUB MEMBERSHIPS
-----------------------------------------
CREATE TABLE IF NOT EXISTS public.club_memberships (
    id uuid default gen_random_uuid() primary key,
    student_id uuid references public.profiles on delete cascade not null,
    club_id uuid references public.clubs on delete cascade not null,
    status text default 'pending', -- pending, approved, rejected
    applied_at timestamp with time zone default timezone('utc'::text, now()),
    approved_at timestamp with time zone,
    UNIQUE(student_id, club_id)
);
ALTER TABLE public.club_memberships ENABLE ROW LEVEL SECURITY;
-- Students can see their own memberships
CREATE POLICY "Students can view own memberships" ON public.club_memberships FOR SELECT USING (student_id = auth.uid());
-- Students can insert their own memberships
CREATE POLICY "Students can apply" ON public.club_memberships FOR INSERT WITH CHECK (student_id = auth.uid());
-- Coordinators can view memberships for their clubs
CREATE POLICY "Coordinators can view memberships" ON public.club_memberships FOR SELECT USING (
  EXISTS (SELECT 1 FROM public.club_coordinators WHERE club_id = public.club_memberships.club_id AND coordinator_id = auth.uid())
);
-- Coordinators can update memberships for their clubs
CREATE POLICY "Coordinators can update memberships" ON public.club_memberships FOR UPDATE USING (
  EXISTS (SELECT 1 FROM public.club_coordinators WHERE club_id = public.club_memberships.club_id AND coordinator_id = auth.uid())
);

-----------------------------------------
-- 6. EVENTS
-----------------------------------------
CREATE TABLE IF NOT EXISTS public.events (
    id uuid default gen_random_uuid() primary key,
    club_id uuid references public.clubs on delete cascade not null,
    title text not null,
    description text,
    event_date date not null,
    start_time time not null,
    end_time time not null,
    venue text,
    capacity integer,
    registration_open boolean default true,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
ALTER TABLE public.events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Events viewable by everyone" ON public.events FOR SELECT USING (true);
CREATE POLICY "Coordinators can manage their club events" ON public.events FOR ALL USING (
  EXISTS (SELECT 1 FROM public.club_coordinators WHERE club_id = public.events.club_id AND coordinator_id = auth.uid())
);

-----------------------------------------
-- 7. EVENT REGISTRATIONS
-----------------------------------------
CREATE TABLE IF NOT EXISTS public.event_registrations (
    id uuid default gen_random_uuid() primary key,
    event_id uuid references public.events on delete cascade not null,
    student_id uuid references public.profiles on delete cascade not null,
    registered_at timestamp with time zone default timezone('utc'::text, now()),
    UNIQUE(event_id, student_id)
);
ALTER TABLE public.event_registrations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Students view own registrations" ON public.event_registrations FOR SELECT USING (student_id = auth.uid());
CREATE POLICY "Students register themselves" ON public.event_registrations FOR INSERT WITH CHECK (student_id = auth.uid());
CREATE POLICY "Coordinators view event registrations" ON public.event_registrations FOR SELECT USING (
  EXISTS (
    SELECT 1 FROM public.events e 
    JOIN public.club_coordinators cc ON e.club_id = cc.club_id 
    WHERE e.id = public.event_registrations.event_id AND cc.coordinator_id = auth.uid()
  )
);

-----------------------------------------
-- 8. ATTENDANCE
-----------------------------------------
CREATE TABLE IF NOT EXISTS public.attendance (
    id uuid default gen_random_uuid() primary key,
    event_id uuid references public.events on delete cascade not null,
    student_id uuid references public.profiles on delete cascade not null,
    status text default 'present', -- present, absent, late
    marked_at timestamp with time zone default timezone('utc'::text, now()),
    UNIQUE(event_id, student_id)
);
ALTER TABLE public.attendance ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Students view own attendance" ON public.attendance FOR SELECT USING (student_id = auth.uid());
CREATE POLICY "Coordinators manage attendance" ON public.attendance FOR ALL USING (
  EXISTS (
    SELECT 1 FROM public.events e 
    JOIN public.club_coordinators cc ON e.club_id = cc.club_id 
    WHERE e.id = public.attendance.event_id AND cc.coordinator_id = auth.uid()
  )
);

-----------------------------------------
-- 9. ANNOUNCEMENTS
-----------------------------------------
CREATE TABLE IF NOT EXISTS public.announcements (
    id uuid default gen_random_uuid() primary key,
    club_id uuid references public.clubs on delete cascade not null,
    title text not null,
    content text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
ALTER TABLE public.announcements ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Announcements viewable by everyone" ON public.announcements FOR SELECT USING (true);
CREATE POLICY "Coordinators can manage announcements" ON public.announcements FOR ALL USING (
  EXISTS (SELECT 1 FROM public.club_coordinators WHERE club_id = public.announcements.club_id AND coordinator_id = auth.uid())
);

-----------------------------------------
-- DUMMY SEED DATA
-----------------------------------------
INSERT INTO public.club_categories (id, name, description) VALUES 
('ca7e90f0-1b5e-4b2a-8b3a-123456789012', 'Academic', 'Academic and educational clubs'),
('cb7e90f0-1b5e-4b2a-8b3a-123456789012', 'Cultural', 'Cultural and arts clubs');

INSERT INTO public.clubs (id, name, slug, description, category_id) VALUES 
('c17e90f0-1b5e-4b2a-8b3a-123456789012', 'Computer Science Society', 'css', 'The official CS club', 'ca7e90f0-1b5e-4b2a-8b3a-123456789012'),
('c27e90f0-1b5e-4b2a-8b3a-123456789012', 'Music Club', 'music', 'Singers and instruments', 'cb7e90f0-1b5e-4b2a-8b3a-123456789012');
