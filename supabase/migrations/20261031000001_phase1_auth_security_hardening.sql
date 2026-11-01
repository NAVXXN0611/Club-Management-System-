-- =====================================================================
-- CCMS Migration: Phase 1 Authentication & Security Hardening (Final)
-- File: supabase/migrations/20261031000001_phase1_auth_security_hardening.sql
-- Description:
--   1. Dynamically purges all existing RLS policies on the 9 CCMS tables
--      using PostgreSQL catalog metadata (ensures zero leftover overrides).
--   2. Extends profiles table with optional metadata columns.
--   3. Introduces hardened SECURITY DEFINER helper functions (SET search_path = '').
--   4. Hardens handle_new_user() trigger to force role = 'student' unconditionally.
--   5. Cleans up any duplicate signup triggers on auth.users dynamically.
--   6. Introduces private_ccms schema and admin_bootstrap_tokens table
--      owned strictly by postgres to authorize the first-admin bootstrap atomically.
--   7. Adds before-update trigger on profiles to block unauthorized role changes,
--      verifying the private bootstrap token table if zero admins exist.
--   8. Adds dedicated bootstrap_first_admin(uuid) procedure (revoked from client roles).
--   9. Adds before-update trigger on club_memberships to ensure student_id & club_id
--      remain strictly immutable during coordinator status reviews.
--  10. Adds coordinator role sync triggers on club_coordinators.
--  11. Restricts club_coordinators SELECT to authenticated assigned coordinators & admins.
--  12. Establishes clean, non-recursive, least-privilege RLS policies.
-- Preserves all existing table data and foreign key relationships.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. PURGE ALL EXISTING POLICIES DYNAMICALLY VIA POSTGRES CATALOG
-- ---------------------------------------------------------------------
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT schemaname, tablename, policyname
        FROM pg_policies
        WHERE schemaname = 'public'
          AND tablename IN (
              'profiles',
              'club_categories',
              'clubs',
              'club_coordinators',
              'club_memberships',
              'events',
              'event_registrations',
              'attendance',
              'announcements'
          )
    ) LOOP
        EXECUTE pg_catalog.format(
            'DROP POLICY IF EXISTS %I ON %I.%I',
            r.policyname,
            r.schemaname,
            r.tablename
        );
    END LOOP;
END $$;

-- ---------------------------------------------------------------------
-- 2. EXTEND PROFILES TABLE WITH OPTIONAL METADATA COLUMNS
-- ---------------------------------------------------------------------
ALTER TABLE public.profiles
  ADD COLUMN IF NOT EXISTS student_id text,
  ADD COLUMN IF NOT EXISTS department text,
  ADD COLUMN IF NOT EXISTS year text,
  ADD COLUMN IF NOT EXISTS phone text,
  ADD COLUMN IF NOT EXISTS avatar_url text;

-- ---------------------------------------------------------------------
-- 3. HARDENED SECURITY DEFINER HELPER FUNCTIONS
-- ---------------------------------------------------------------------
-- Returns true if caller has the 'admin' role in public.profiles.
-- SET search_path = '' and fully qualified identifiers eliminate search-path injection.
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = ''
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.profiles
    WHERE id = auth.uid() AND role = 'admin'
  );
$$;

-- Returns true if caller is assigned as a coordinator for the given club.
CREATE OR REPLACE FUNCTION public.is_coordinator_for_club(club_uuid uuid)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path = ''
STABLE
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.club_coordinators
    WHERE club_id = club_uuid AND coordinator_id = auth.uid()
  );
$$;

-- Explicit ownership
ALTER FUNCTION public.is_admin() OWNER TO postgres;
ALTER FUNCTION public.is_coordinator_for_club(uuid) OWNER TO postgres;

-- Helper functions must be executable by authenticated and anon for RLS policy evaluation
REVOKE ALL ON FUNCTION public.is_admin() FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.is_admin() TO authenticated, anon;

REVOKE ALL ON FUNCTION public.is_coordinator_for_club(uuid) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.is_coordinator_for_club(uuid) TO authenticated, anon;

-- ---------------------------------------------------------------------
-- 4. HARDENED SIGNUP TRIGGER (NEVER TRUSTS CLIENT METADATA FOR ROLES)
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, email, role)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data ->> 'full_name', ''),
    NEW.email,
    'student' -- Public registration ALWAYS creates a student profile
  )
  ON CONFLICT (id) DO UPDATE
  SET
    full_name = EXCLUDED.full_name,
    email = EXCLUDED.email,
    -- Intentionally omitting role: existing role can NEVER be overwritten by signup metadata
    updated_at = pg_catalog.timezone('utc', pg_catalog.now());

  RETURN NEW;
END;
$$;

ALTER FUNCTION public.handle_new_user() OWNER TO postgres;
REVOKE ALL ON FUNCTION public.handle_new_user() FROM PUBLIC, anon, authenticated;

-- Dynamically drop any confirmed triggers explicitly calling public.handle_new_user on auth.users
-- Strictly targets only triggers invoking public.handle_new_user to preserve unrelated audit or application triggers
DO $$
DECLARE
    t RECORD;
BEGIN
    FOR t IN (
        SELECT tr.tgname
        FROM pg_trigger tr
        JOIN pg_class c ON c.oid = tr.tgrelid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        JOIN pg_proc p ON p.oid = tr.tgfoid
        JOIN pg_namespace np ON np.oid = p.pronamespace
        WHERE n.nspname = 'auth'
          AND c.relname = 'users'
          AND np.nspname = 'public'
          AND p.proname = 'handle_new_user'
          AND tr.tgisinternal = false
    ) LOOP
        EXECUTE pg_catalog.format('DROP TRIGGER IF EXISTS %I ON auth.users', t.tgname);
    END LOOP;
END $$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Backfill any existing auth users who lack a profile
INSERT INTO public.profiles (id, full_name, email, role)
SELECT
  u.id,
  COALESCE(u.raw_user_meta_data ->> 'full_name', ''),
  u.email,
  'student'
FROM auth.users u
LEFT JOIN public.profiles p ON p.id = u.id
WHERE p.id IS NULL
ON CONFLICT (id) DO NOTHING;

-- ---------------------------------------------------------------------
-- 5. PRIVATE BOOTSTRAP AUTHORIZATION SCHEMA & TABLE
-- ---------------------------------------------------------------------
-- A private schema and table owned strictly by postgres to manage atomic,
-- database-side first-admin bootstrap tokens. Inaccessible to client roles.
CREATE SCHEMA IF NOT EXISTS private_ccms;
ALTER SCHEMA private_ccms OWNER TO postgres;
REVOKE ALL ON SCHEMA private_ccms FROM PUBLIC, anon, authenticated;

CREATE TABLE IF NOT EXISTS private_ccms.admin_bootstrap_tokens (
    target_user_id uuid PRIMARY KEY,
    backend_pid integer NOT NULL DEFAULT pg_catalog.pg_backend_pid(),
    created_at timestamp with time zone DEFAULT pg_catalog.timezone('utc', pg_catalog.now()),
    is_singleton boolean NOT NULL DEFAULT true CHECK (is_singleton = true) UNIQUE
);
ALTER TABLE private_ccms.admin_bootstrap_tokens OWNER TO postgres;
REVOKE ALL ON TABLE private_ccms.admin_bootstrap_tokens FROM PUBLIC, anon, authenticated;

-- ---------------------------------------------------------------------
-- 6. PROFILE ROLE PROTECTION TRIGGER & FIRST-ADMIN BOOTSTRAP
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.protect_profile_role()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  -- If role is being changed, ensure caller is an authorized admin
  IF OLD.role IS DISTINCT FROM NEW.role THEN
    IF NOT public.is_admin() THEN
      -- Secure bootstrap check: allowed ONLY when an active bootstrap authorization token
      -- exists in private_ccms.admin_bootstrap_tokens for NEW.id and current backend PID,
      -- AND there are currently ZERO administrators in the system.
      -- Unrestricted auth.uid() IS NULL and client-settable GUCs are strictly prohibited.
      IF EXISTS (
        SELECT 1 FROM private_ccms.admin_bootstrap_tokens abt
        WHERE abt.target_user_id = NEW.id
          AND abt.backend_pid = pg_catalog.pg_backend_pid()
      ) AND NOT EXISTS (
        SELECT 1 FROM public.profiles p
        WHERE p.role = 'admin'
      ) THEN
        RETURN NEW;
      END IF;

      RAISE EXCEPTION 'Unauthorized: Only administrators can modify user roles (current: %, attempted: %)', OLD.role, NEW.role;
    END IF;
  END IF;
  RETURN NEW;
END;
$$;

ALTER FUNCTION public.protect_profile_role() OWNER TO postgres;
REVOKE ALL ON FUNCTION public.protect_profile_role() FROM PUBLIC, anon, authenticated;

DROP TRIGGER IF EXISTS tr_protect_profile_role ON public.profiles;
CREATE TRIGGER tr_protect_profile_role
BEFORE UPDATE ON public.profiles
FOR EACH ROW EXECUTE FUNCTION public.protect_profile_role();

-- Dedicated one-time bootstrap procedure for the project administrator
-- Executable ONLY by the trusted database owner (postgres) in direct SQL sessions.
-- Serialized via transaction-level advisory lock to eliminate any concurrent race condition.
CREATE OR REPLACE FUNCTION public.bootstrap_first_admin(target_user_id uuid)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
  -- Dedicated 64-bit advisory lock key for CCMS administrator bootstrap serialization
  k_bootstrap_lock_id CONSTANT bigint := 847291837461928374;
BEGIN
  -- 1. Acquire transaction-level exclusive advisory lock FIRST.
  -- pg_advisory_xact_lock() blocks any concurrent caller until this transaction finishes (COMMIT or ROLLBACK).
  PERFORM pg_catalog.pg_advisory_xact_lock(k_bootstrap_lock_id);

  -- 2. Verify AFTER acquiring lock that no administrator exists.
  -- Because the lock is held across the transaction, any concurrent caller that committed an admin will be visible.
  IF EXISTS (SELECT 1 FROM public.profiles WHERE role = 'admin') THEN
    RAISE EXCEPTION 'Bootstrap denied: The system already has one or more administrators configured.';
  END IF;

  -- 3. Verify target user exists in profiles
  IF NOT EXISTS (SELECT 1 FROM public.profiles WHERE id = bootstrap_first_admin.target_user_id) THEN
    RAISE EXCEPTION 'User with ID % does not exist in public.profiles.', bootstrap_first_admin.target_user_id;
  END IF;

  -- 4. Atomically issue authorization token in private schema (inaccessible to PUBLIC/anon/authenticated)
  INSERT INTO private_ccms.admin_bootstrap_tokens (target_user_id, backend_pid)
  VALUES (bootstrap_first_admin.target_user_id, pg_catalog.pg_backend_pid())
  ON CONFLICT (target_user_id) DO UPDATE
  SET backend_pid = pg_catalog.pg_backend_pid(),
      created_at = pg_catalog.timezone('utc', pg_catalog.now());

  -- 5. Execute the update with guaranteed cleanup via exception handling
  BEGIN
    UPDATE public.profiles
    SET role = 'admin', updated_at = pg_catalog.timezone('utc', pg_catalog.now())
    WHERE id = bootstrap_first_admin.target_user_id;

    -- Clean up authorization token immediately after successful role promotion
    DELETE FROM private_ccms.admin_bootstrap_tokens
    WHERE admin_bootstrap_tokens.target_user_id = bootstrap_first_admin.target_user_id;
  EXCEPTION
    WHEN OTHERS THEN
      -- Clean up token on failure and re-raise
      DELETE FROM private_ccms.admin_bootstrap_tokens
      WHERE admin_bootstrap_tokens.target_user_id = bootstrap_first_admin.target_user_id;
      RAISE;
  END;
END;
$$;

ALTER FUNCTION public.bootstrap_first_admin(uuid) OWNER TO postgres;
REVOKE ALL ON FUNCTION public.bootstrap_first_admin(uuid) FROM PUBLIC, anon, authenticated;

-- ---------------------------------------------------------------------
-- 7. IMMUTABLE MEMBERSHIP FIELDS TRIGGER
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.protect_club_membership_immutable_fields()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  -- Student ID and Club ID cannot be reassigned during updates
  IF OLD.student_id IS DISTINCT FROM NEW.student_id THEN
    RAISE EXCEPTION 'Unauthorized: student_id on a club membership is immutable';
  END IF;

  IF OLD.club_id IS DISTINCT FROM NEW.club_id THEN
    RAISE EXCEPTION 'Unauthorized: club_id on a club membership is immutable';
  END IF;

  -- Ensure status is a valid lifecycle state
  IF NEW.status NOT IN ('pending', 'approved', 'rejected') THEN
    RAISE EXCEPTION 'Invalid membership status: %', NEW.status;
  END IF;

  RETURN NEW;
END;
$$;

ALTER FUNCTION public.protect_club_membership_immutable_fields() OWNER TO postgres;
REVOKE ALL ON FUNCTION public.protect_club_membership_immutable_fields() FROM PUBLIC, anon, authenticated;

DROP TRIGGER IF EXISTS tr_protect_club_membership ON public.club_memberships;
CREATE TRIGGER tr_protect_club_membership
BEFORE UPDATE ON public.club_memberships
FOR EACH ROW EXECUTE FUNCTION public.protect_club_membership_immutable_fields();

-- ---------------------------------------------------------------------
-- 8. COORDINATOR ROLE AUTOMATION TRIGGERS
-- ---------------------------------------------------------------------
-- Automatically set profile role to 'coordinator' when assigned to a club
CREATE OR REPLACE FUNCTION public.sync_coordinator_role_on_assign()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  UPDATE public.profiles
  SET role = 'coordinator', updated_at = pg_catalog.timezone('utc', pg_catalog.now())
  WHERE id = NEW.coordinator_id AND role = 'student';
  RETURN NEW;
END;
$$;

ALTER FUNCTION public.sync_coordinator_role_on_assign() OWNER TO postgres;
REVOKE ALL ON FUNCTION public.sync_coordinator_role_on_assign() FROM PUBLIC, anon, authenticated;

DROP TRIGGER IF EXISTS tr_sync_coordinator_role_assign ON public.club_coordinators;
CREATE TRIGGER tr_sync_coordinator_role_assign
AFTER INSERT ON public.club_coordinators
FOR EACH ROW EXECUTE FUNCTION public.sync_coordinator_role_on_assign();

-- Automatically revert role to 'student' when unassigned (if no other clubs assigned)
CREATE OR REPLACE FUNCTION public.sync_coordinator_role_on_unassign()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM public.club_coordinators WHERE coordinator_id = OLD.coordinator_id) THEN
    UPDATE public.profiles
    SET role = 'student', updated_at = pg_catalog.timezone('utc', pg_catalog.now())
    WHERE id = OLD.coordinator_id AND role = 'coordinator';
  END IF;
  RETURN OLD;
END;
$$;

ALTER FUNCTION public.sync_coordinator_role_on_unassign() OWNER TO postgres;
REVOKE ALL ON FUNCTION public.sync_coordinator_role_on_unassign() FROM PUBLIC, anon, authenticated;

DROP TRIGGER IF EXISTS tr_sync_coordinator_role_unassign ON public.club_coordinators;
CREATE TRIGGER tr_sync_coordinator_role_unassign
AFTER DELETE ON public.club_coordinators
FOR EACH ROW EXECUTE FUNCTION public.sync_coordinator_role_on_unassign();

-- ---------------------------------------------------------------------
-- 9. ENABLE ROW LEVEL SECURITY EXPLICITLY ON ALL 9 TABLES
-- ---------------------------------------------------------------------
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.club_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.clubs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.club_coordinators ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.club_memberships ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.event_registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.announcements ENABLE ROW LEVEL SECURITY;

-- ---------------------------------------------------------------------
-- 10. RE-ESTABLISH POLICIES WITH LEAST PRIVILEGE
-- ---------------------------------------------------------------------

-- === TABLE: public.profiles ===
CREATE POLICY "profiles_select_policy"
  ON public.profiles FOR SELECT
  USING (
    auth.uid() = id
    OR public.is_admin()
    OR EXISTS (
      SELECT 1 FROM public.club_memberships cm
      WHERE cm.student_id = public.profiles.id
        AND public.is_coordinator_for_club(cm.club_id)
    )
    OR EXISTS (
      SELECT 1 FROM public.event_registrations er
      JOIN public.events ev ON ev.id = er.event_id
      WHERE er.student_id = public.profiles.id
        AND public.is_coordinator_for_club(ev.club_id)
    )
  );

CREATE POLICY "profiles_insert_policy"
  ON public.profiles FOR INSERT
  WITH CHECK (
    (auth.uid() = id AND role = 'student')
    OR public.is_admin()
  );

CREATE POLICY "profiles_update_policy"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id OR public.is_admin())
  WITH CHECK (auth.uid() = id OR public.is_admin());

CREATE POLICY "profiles_delete_policy"
  ON public.profiles FOR DELETE
  USING (public.is_admin());


-- === TABLE: public.club_categories ===
CREATE POLICY "categories_select_policy"
  ON public.club_categories FOR SELECT
  USING (true);

CREATE POLICY "categories_insert_policy"
  ON public.club_categories FOR INSERT
  WITH CHECK (public.is_admin());

CREATE POLICY "categories_update_policy"
  ON public.club_categories FOR UPDATE
  USING (public.is_admin())
  WITH CHECK (public.is_admin());

CREATE POLICY "categories_delete_policy"
  ON public.club_categories FOR DELETE
  USING (public.is_admin());


-- === TABLE: public.clubs ===
CREATE POLICY "clubs_select_policy"
  ON public.clubs FOR SELECT
  USING (true);

CREATE POLICY "clubs_insert_policy"
  ON public.clubs FOR INSERT
  WITH CHECK (public.is_admin());

CREATE POLICY "clubs_update_policy"
  ON public.clubs FOR UPDATE
  USING (public.is_coordinator_for_club(id) OR public.is_admin())
  WITH CHECK (public.is_coordinator_for_club(id) OR public.is_admin());

CREATE POLICY "clubs_delete_policy"
  ON public.clubs FOR DELETE
  USING (public.is_admin());


-- === TABLE: public.club_coordinators ===
CREATE POLICY "coordinators_select_policy"
  ON public.club_coordinators FOR SELECT
  TO authenticated
  USING (coordinator_id = auth.uid() OR public.is_admin());

CREATE POLICY "coordinators_insert_policy"
  ON public.club_coordinators FOR INSERT
  WITH CHECK (public.is_admin());

CREATE POLICY "coordinators_update_policy"
  ON public.club_coordinators FOR UPDATE
  USING (public.is_admin())
  WITH CHECK (public.is_admin());

CREATE POLICY "coordinators_delete_policy"
  ON public.club_coordinators FOR DELETE
  USING (public.is_admin());


-- === TABLE: public.club_memberships ===
CREATE POLICY "memberships_select_policy"
  ON public.club_memberships FOR SELECT
  USING (
    student_id = auth.uid()
    OR public.is_coordinator_for_club(club_id)
    OR public.is_admin()
  );

CREATE POLICY "memberships_insert_policy"
  ON public.club_memberships FOR INSERT
  WITH CHECK (
    (student_id = auth.uid() AND status = 'pending')
    OR public.is_admin()
  );

CREATE POLICY "memberships_update_policy"
  ON public.club_memberships FOR UPDATE
  USING (public.is_coordinator_for_club(club_id) OR public.is_admin())
  WITH CHECK (public.is_coordinator_for_club(club_id) OR public.is_admin());

CREATE POLICY "memberships_delete_policy"
  ON public.club_memberships FOR DELETE
  USING (
    student_id = auth.uid()
    OR public.is_coordinator_for_club(club_id)
    OR public.is_admin()
  );


-- === TABLE: public.events ===
CREATE POLICY "events_select_policy"
  ON public.events FOR SELECT
  USING (true);

CREATE POLICY "events_insert_policy"
  ON public.events FOR INSERT
  WITH CHECK (public.is_coordinator_for_club(club_id) OR public.is_admin());

CREATE POLICY "events_update_policy"
  ON public.events FOR UPDATE
  USING (public.is_coordinator_for_club(club_id) OR public.is_admin())
  WITH CHECK (public.is_coordinator_for_club(club_id) OR public.is_admin());

CREATE POLICY "events_delete_policy"
  ON public.events FOR DELETE
  USING (public.is_coordinator_for_club(club_id) OR public.is_admin());


-- === TABLE: public.event_registrations ===
CREATE POLICY "registrations_select_policy"
  ON public.event_registrations FOR SELECT
  USING (
    student_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM public.events ev
      WHERE ev.id = public.event_registrations.event_id
        AND (public.is_coordinator_for_club(ev.club_id) OR public.is_admin())
    )
  );

CREATE POLICY "registrations_insert_policy"
  ON public.event_registrations FOR INSERT
  WITH CHECK (student_id = auth.uid() OR public.is_admin());

CREATE POLICY "registrations_delete_policy"
  ON public.event_registrations FOR DELETE
  USING (
    student_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM public.events ev
      WHERE ev.id = public.event_registrations.event_id
        AND (public.is_coordinator_for_club(ev.club_id) OR public.is_admin())
    )
  );


-- === TABLE: public.attendance ===
CREATE POLICY "attendance_select_policy"
  ON public.attendance FOR SELECT
  USING (
    student_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM public.events ev
      WHERE ev.id = public.attendance.event_id
        AND (public.is_coordinator_for_club(ev.club_id) OR public.is_admin())
    )
  );

CREATE POLICY "attendance_insert_policy"
  ON public.attendance FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.events ev
      WHERE ev.id = public.attendance.event_id
        AND (public.is_coordinator_for_club(ev.club_id) OR public.is_admin())
    )
  );

CREATE POLICY "attendance_update_policy"
  ON public.attendance FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM public.events ev
      WHERE ev.id = public.attendance.event_id
        AND (public.is_coordinator_for_club(ev.club_id) OR public.is_admin())
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.events ev
      WHERE ev.id = public.attendance.event_id
        AND (public.is_coordinator_for_club(ev.club_id) OR public.is_admin())
    )
  );

CREATE POLICY "attendance_delete_policy"
  ON public.attendance FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM public.events ev
      WHERE ev.id = public.attendance.event_id
        AND (public.is_coordinator_for_club(ev.club_id) OR public.is_admin())
    )
  );


-- === TABLE: public.announcements ===
CREATE POLICY "announcements_select_policy"
  ON public.announcements FOR SELECT
  USING (true);

CREATE POLICY "announcements_insert_policy"
  ON public.announcements FOR INSERT
  WITH CHECK (public.is_coordinator_for_club(club_id) OR public.is_admin());

CREATE POLICY "announcements_update_policy"
  ON public.announcements FOR UPDATE
  USING (public.is_coordinator_for_club(club_id) OR public.is_admin())
  WITH CHECK (public.is_coordinator_for_club(club_id) OR public.is_admin());

CREATE POLICY "announcements_delete_policy"
  ON public.announcements FOR DELETE
  USING (public.is_coordinator_for_club(club_id) OR public.is_admin());
