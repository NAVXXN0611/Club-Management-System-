-- ============================================================
-- FIX: Infinite recursion in profiles RLS policy
-- Run this entire script in your Supabase SQL Editor
-- ============================================================

-- 1. Drop the recursive policy that causes the infinite loop
DROP POLICY IF EXISTS "Admins can view all profiles" ON public.profiles;

-- 2. Replace it with a non-recursive version using auth.jwt()
--    which reads the role from the JWT token directly,
--    without querying the profiles table again.
CREATE POLICY "Admins can view all profiles"
  ON public.profiles
  FOR SELECT
  USING (
    (auth.jwt() ->> 'role') = 'admin'
    OR
    -- Fallback: check raw_user_meta_data on the auth.users side
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = auth.uid()
      AND auth.users.raw_user_meta_data ->> 'role' = 'admin'
    )
  );

-- 3. Ensure the basic self-select policy is clean
DROP POLICY IF EXISTS "Users can view own profile" ON public.profiles;
CREATE POLICY "Users can view own profile"
  ON public.profiles
  FOR SELECT
  USING (auth.uid() = id);

-- 4. Verify - this should return your policies without error
SELECT policyname, cmd, qual
FROM pg_policies
WHERE tablename = 'profiles';
