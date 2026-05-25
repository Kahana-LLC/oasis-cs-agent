-- CS agent / lifecycle email dedup (see PLAN.md, docs/SUPABASE_LIFECYCLE_EMAIL_PLAN.md)
create table if not exists public.cs_outreach_log (
  id               uuid primary key default gen_random_uuid(),
  user_id          uuid not null,
  trigger_name     text not null,
  channel          text not null default 'email',
  sent_at          timestamptz not null default now(),
  message_preview  text,
  provider         text default 'brevo'
);

create unique index if not exists cs_outreach_log_user_trigger_uidx
  on public.cs_outreach_log (user_id, trigger_name);

create index if not exists cs_outreach_log_sent_at_idx
  on public.cs_outreach_log (sent_at desc);

comment on table public.cs_outreach_log is
  'One row per (user_id, trigger_name) — lifecycle and CS agent email dedup.';
