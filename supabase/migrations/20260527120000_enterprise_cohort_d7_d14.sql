-- Enterprise founder/expansion: day 7–8 and 14–15 (was 55–56 / 85–86); lower session bars for early feedback.

create or replace function public.lifecycle_cohort_enterprise_founder(p_limit integer default 500)
returns table (user_id uuid, email character varying, name character varying, status character varying)
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
    and public.lifecycle_is_company_email(u.email)
    and (current_date - (u.created_at at time zone 'utc')::date) between 7 and 8
    and (select count(*)::int from public.sessions s where s.user_id = u.user_id) >= 2
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'enterprise_founder'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

create or replace function public.lifecycle_cohort_enterprise_expansion(p_limit integer default 500)
returns table (user_id uuid, email character varying, name character varying, status character varying)
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
    and public.lifecycle_is_company_email(u.email)
    and (current_date - (u.created_at at time zone 'utc')::date) between 14 and 15
    and (select count(*)::int from public.sessions s where s.user_id = u.user_id) >= 4
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'enterprise_expansion'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;
