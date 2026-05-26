-- Cohort for lifecycle-daily-cron: activation CS calendar ~day 3, no prompt or training
create or replace function public.lifecycle_cohort_activation_cs_calendar(p_limit integer default 500)
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
      select 1 from public.llm_usage lu where lu.user_id = u.user_id
    )
    and not exists (
      select 1 from public.feedback_events fe where fe.user_id = u.user_id
    )
    and not exists (
      select 1 from public.cs_outreach_log o
      where o.user_id = u.user_id
        and o.trigger_name = 'activation_cs_calendar'
    )
  order by u.created_at asc
  limit greatest(1, least(coalesce(p_limit, 500), 500));
$$;

comment on function public.lifecycle_cohort_activation_cs_calendar(integer) is
  'Users eligible for activation_cs_calendar: active, signup day 3–5 window, no llm_usage, no feedback_events, not yet sent.';

grant execute on function public.lifecycle_cohort_activation_cs_calendar(integer) to service_role;
