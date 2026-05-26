-- Phase 2+ lifecycle cohorts: bucket helpers, limit-hitter, at-risk, dead, return, enterprise

-- Consumer email domains (mirror pipeline/metrics.py fallback)
create or replace function public.lifecycle_is_consumer_email(p_email text)
returns boolean
language sql
immutable
as $$
  select lower(split_part(trim(p_email), '@', 2)) in (
    'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'hotmail.co.uk',
    'icloud.com', 'protonmail.com', 'protonmail.ch', 'me.com', 'mac.com',
    'live.com', 'live.co.uk', 'yahoo.co.uk', 'googlemail.com', 'msn.com',
    'aol.com', 'mail.com', 'zoho.com', 'yandex.com', 'gmx.com'
  );
$$;

create or replace function public.lifecycle_is_company_email(p_email text)
returns boolean
language sql
immutable
as $$
  select p_email is not null
    and position('@' in trim(p_email)) > 1
    and not public.lifecycle_is_consumer_email(p_email);
$$;

create or replace function public.lifecycle_user_has_active_paid_plan(p_user_id uuid)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.user_plans up
    where up.user_id = p_user_id
      and coalesce(up.is_active, false) = true
      and up.start_date::date >= date '2026-05-24'
  );
$$;

-- Daily token cap: users.plan_id → plan.limit_daily (Free default 100k per PLAN.md).
-- plan_override table is optional; not referenced here so migration works without it.
create or replace function public.lifecycle_user_effective_daily_limit(p_user_id uuid)
returns bigint
language sql
stable
security definer
set search_path = public
as $$
  select coalesce(
    (
      select p.limit_daily::bigint
      from public.users u
      join public.plan p on p.plan_id = u.plan_id
      where u.user_id = p_user_id
      limit 1
    ),
    100000::bigint
  );
$$;

-- Activity dates = union(llm_usage dates, session dates)
create or replace function public.lifecycle_user_bucket(p_user_id uuid, p_as_of date default current_date)
returns text
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  active_today boolean;
  first_ever date;
  last_prev date;
  gap_days int;
  has_prior_7 boolean;
  has_prior_6 boolean;
  has_days_7_29 boolean;
begin
  select exists (
    select 1
    from (
      select (lu.timestamp at time zone 'utc')::date as d
      from public.llm_usage lu
      where lu.user_id = p_user_id
      union
      select (s.started_at at time zone 'utc')::date as d
      from public.sessions s
      where s.user_id = p_user_id
    ) ad
    where ad.d = p_as_of
  ) into active_today;

  if active_today then
    select min(ad.d) into first_ever
    from (
      select (lu.timestamp at time zone 'utc')::date as d
      from public.llm_usage lu
      where lu.user_id = p_user_id
      union
      select (s.started_at at time zone 'utc')::date as d
      from public.sessions s
      where s.user_id = p_user_id
    ) ad;

    if first_ever is null then
      return 'dead';
    end if;
    if p_as_of = first_ever then
      return 'new';
    end if;

    select max(ad.d) into last_prev
    from (
      select (lu.timestamp at time zone 'utc')::date as d
      from public.llm_usage lu
      where lu.user_id = p_user_id
      union
      select (s.started_at at time zone 'utc')::date as d
      from public.sessions s
      where s.user_id = p_user_id
    ) ad
    where ad.d < p_as_of;

    if last_prev is null then
      return 'new';
    end if;

    gap_days := p_as_of - last_prev;
    if gap_days >= 30 then
      return 'resurrected';
    end if;
    if gap_days >= 7 then
      return 'reactivated';
    end if;

    select exists (
      select 1
      from (
        select (lu.timestamp at time zone 'utc')::date as d
        from public.llm_usage lu
        where lu.user_id = p_user_id
        union
        select (s.started_at at time zone 'utc')::date as d
        from public.sessions s
        where s.user_id = p_user_id
      ) ad
      where ad.d between p_as_of - 7 and p_as_of - 1
    ) into has_prior_7;

    if has_prior_7 then
      return 'current';
    end if;
    return 'current';
  end if;

  select exists (
    select 1
    from (
      select (lu.timestamp at time zone 'utc')::date as d
      from public.llm_usage lu
      where lu.user_id = p_user_id
      union
      select (s.started_at at time zone 'utc')::date as d
      from public.sessions s
      where s.user_id = p_user_id
    ) ad
    where ad.d between p_as_of - 6 and p_as_of - 1
  ) into has_prior_6;
  if has_prior_6 then
    return 'at_risk_wau';
  end if;

  select exists (
    select 1
    from (
      select (lu.timestamp at time zone 'utc')::date as d
      from public.llm_usage lu
      where lu.user_id = p_user_id
      union
      select (s.started_at at time zone 'utc')::date as d
      from public.sessions s
      where s.user_id = p_user_id
    ) ad
    where ad.d between p_as_of - 29 and p_as_of - 7
  ) into has_days_7_29;
  if has_days_7_29 then
    return 'at_risk_mau';
  end if;

  return 'dead';
end;
$$;

comment on function public.lifecycle_user_bucket(uuid, date) is
  'DAU bucket for one user on p_as_of (mirrors reporting/dau_model.classify_user_bucket).';

-- Limit-hitter D0: activated free user who hit daily cap, not yet emailed
create or replace function public.lifecycle_cohort_limit_hitter_upgrade(p_limit integer default 500)
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
    and not public.lifecycle_user_has_active_paid_plan(u.user_id)
    and exists (select 1 from public.llm_usage lu where lu.user_id = u.user_id)
    and exists (
      select 1
      from public.llm_daily_usage ld
      where ld.user_id = u.user_id
        and ld.total_tokens >= public.lifecycle_user_effective_daily_limit(u.user_id)
    )
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'limit_hitter_upgrade'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

-- Limit-hitter D7: D0 sent ≥7d ago, still free
create or replace function public.lifecycle_cohort_limit_hitter_upgrade_d7(p_limit integer default 500)
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
    and not public.lifecycle_user_has_active_paid_plan(u.user_id)
    and exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name = 'limit_hitter_upgrade'
        and o.sent_at <= now() - interval '7 days'
    )
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'limit_hitter_upgrade_d7'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

-- At-risk nurture touches
create or replace function public.lifecycle_cohort_at_risk_nurture_d0(p_limit integer default 500)
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
    and not public.lifecycle_user_has_active_paid_plan(u.user_id)
    and public.lifecycle_user_bucket(u.user_id, current_date) in ('at_risk_wau', 'at_risk_mau')
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'at_risk_nurture_d0'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

create or replace function public.lifecycle_cohort_at_risk_nurture_d7(p_limit integer default 500)
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
    and public.lifecycle_user_bucket(u.user_id, current_date) in ('at_risk_wau', 'at_risk_mau')
    and exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name = 'at_risk_nurture_d0'
        and o.sent_at <= now() - interval '7 days'
    )
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'at_risk_nurture_d7'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

create or replace function public.lifecycle_cohort_at_risk_nurture_d14(p_limit integer default 500)
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
    and public.lifecycle_user_bucket(u.user_id, current_date) in ('at_risk_wau', 'at_risk_mau')
    and exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name = 'at_risk_nurture_d0'
        and o.sent_at <= now() - interval '14 days'
    )
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'at_risk_nurture_d14'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

create or replace function public.lifecycle_cohort_at_risk_nurture_d21(p_limit integer default 500)
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
    and public.lifecycle_user_bucket(u.user_id, current_date) in ('at_risk_wau', 'at_risk_mau')
    and exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name = 'at_risk_nurture_d0'
        and o.sent_at <= now() - interval '21 days'
    )
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'at_risk_nurture_d21'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

-- Dead resurrection (cap 20 new D0 per calendar month)
create or replace function public.lifecycle_cohort_dead_resurrection_d0(p_limit integer default 20)
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
    and public.lifecycle_user_bucket(u.user_id, current_date) = 'dead'
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name in ('dead_resurrection_d0', 'dead_resurrection_d14')
        and o.sent_at >= now() - interval '30 days'
    )
    and (
      select count(*)::int
      from public.cs_outreach_log o
      where o.trigger_name = 'dead_resurrection_d0'
        and o.sent_at >= date_trunc('month', now())
    ) < 20
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'dead_resurrection_d0'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 20), 500));
$$;

create or replace function public.lifecycle_cohort_dead_resurrection_d14(p_limit integer default 500)
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
    and public.lifecycle_user_bucket(u.user_id, current_date) = 'dead'
    and exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name = 'dead_resurrection_d0'
        and o.sent_at <= now() - interval '14 days'
    )
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'dead_resurrection_d14'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

-- Return reinforcement: first day in reactivated or resurrected bucket
create or replace function public.lifecycle_cohort_return_reinforcement(p_limit integer default 500)
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
    and public.lifecycle_user_bucket(u.user_id, current_date) in ('reactivated', 'resurrected')
    and public.lifecycle_user_bucket(u.user_id, current_date - 1) not in ('reactivated', 'resurrected')
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'return_reinforcement'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

-- Enterprise founder (day 55–56) and expansion (day 85–86)
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
    and (current_date - (u.created_at at time zone 'utc')::date) between 55 and 56
    and (select count(*)::int from public.sessions s where s.user_id = u.user_id) >= 8
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
    and (current_date - (u.created_at at time zone 'utc')::date) between 85 and 86
    and (select count(*)::int from public.sessions s where s.user_id = u.user_id) >= 10
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'enterprise_expansion'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

-- Cancelled win-back D14 (D0 handled by webhook)
create or replace function public.lifecycle_cohort_cancelled_winback_d14(p_limit integer default 500)
returns table (user_id uuid, email character varying, name character varying, status character varying)
language sql
stable
security definer
set search_path = public
as $$
  select u.user_id, u.email, u.name, u.status
  from public.users u
  where u.email is not null
    and trim(u.email) <> ''
    and not public.lifecycle_user_has_active_paid_plan(u.user_id)
    and exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name = 'cancelled_winback'
        and o.sent_at <= now() - interval '14 days'
    )
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id and o.trigger_name = 'cancelled_winback_d14'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

grant execute on function public.lifecycle_is_consumer_email(text) to service_role;
grant execute on function public.lifecycle_is_company_email(text) to service_role;
grant execute on function public.lifecycle_user_has_active_paid_plan(uuid) to service_role;
grant execute on function public.lifecycle_user_effective_daily_limit(uuid) to service_role;
grant execute on function public.lifecycle_user_bucket(uuid, date) to service_role;
grant execute on function public.lifecycle_cohort_limit_hitter_upgrade(integer) to service_role;
grant execute on function public.lifecycle_cohort_limit_hitter_upgrade_d7(integer) to service_role;
grant execute on function public.lifecycle_cohort_at_risk_nurture_d0(integer) to service_role;
grant execute on function public.lifecycle_cohort_at_risk_nurture_d7(integer) to service_role;
grant execute on function public.lifecycle_cohort_at_risk_nurture_d14(integer) to service_role;
grant execute on function public.lifecycle_cohort_at_risk_nurture_d21(integer) to service_role;
grant execute on function public.lifecycle_cohort_dead_resurrection_d0(integer) to service_role;
grant execute on function public.lifecycle_cohort_dead_resurrection_d14(integer) to service_role;
grant execute on function public.lifecycle_cohort_return_reinforcement(integer) to service_role;
grant execute on function public.lifecycle_cohort_enterprise_founder(integer) to service_role;
grant execute on function public.lifecycle_cohort_enterprise_expansion(integer) to service_role;
grant execute on function public.lifecycle_cohort_cancelled_winback_d14(integer) to service_role;
