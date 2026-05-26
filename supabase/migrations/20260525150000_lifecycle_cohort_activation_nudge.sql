-- Cohort for lifecycle-daily-cron: activation nudge at T+24h, no first prompt
create or replace function public.lifecycle_cohort_activation_nudge_24h(p_limit integer default 500)
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
    and u.created_at <= now() - interval '24 hours'
    and not exists (
      select 1 from public.llm_usage lu where lu.user_id = u.user_id
    )
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name = 'activation_nudge_24h'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

comment on function public.lifecycle_cohort_activation_nudge_24h(integer) is
  'Users eligible for activation_nudge_24h: active, signed up ≥24h ago, no llm_usage, not yet nudged.';

grant execute on function public.lifecycle_cohort_activation_nudge_24h(integer) to service_role;
