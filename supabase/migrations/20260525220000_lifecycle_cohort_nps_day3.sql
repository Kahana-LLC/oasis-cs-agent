-- Cohort for lifecycle-daily-cron: NPS ~day 3 (all active signups in window)
create or replace function public.lifecycle_cohort_nps_day3(p_limit integer default 500)
returns table (
  user_id uuid,
  email character varying,
  name character varying,
  status character varying
)
language sql
stable
security definer
set search_path = public
as $$
  select u.user_id, u.email, u.name, u.status
  from public.users u
  where u.status = 'active'
    and u.email is not null
    and trim(u.email) <> ''
    and u.created_at <= now() - interval '3 days'
    and u.created_at > now() - interval '5 days'
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name = 'nps_day3'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

comment on function public.lifecycle_cohort_nps_day3(integer) is
  'Users eligible for nps_day3: active, signup day 3–5 window, not yet sent.';

grant execute on function public.lifecycle_cohort_nps_day3(integer) to service_role;
