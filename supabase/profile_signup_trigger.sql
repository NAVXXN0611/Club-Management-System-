-- Creates a profile automatically whenever a Supabase Auth user is created.
-- Run this in the Supabase SQL Editor for the production project.

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, full_name, email, role)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', ''),
    new.email,
    coalesce(nullif(new.raw_user_meta_data ->> 'role', ''), 'student')
  )
  on conflict (id) do update
  set
    full_name = excluded.full_name,
    email = excluded.email,
    role = excluded.role,
    updated_at = timezone('utc'::text, now());

  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;

create trigger on_auth_user_created
after insert on auth.users
for each row execute function public.handle_new_user();

insert into public.profiles (id, full_name, email, role)
select
  users.id,
  coalesce(users.raw_user_meta_data ->> 'full_name', ''),
  users.email,
  coalesce(nullif(users.raw_user_meta_data ->> 'role', ''), 'student')
from auth.users
left join public.profiles on profiles.id = users.id
where profiles.id is null;
