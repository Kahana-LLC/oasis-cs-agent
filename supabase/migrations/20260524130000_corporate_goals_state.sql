-- Shared state for corporate goals (e.g. locked DAU launch-week baseline).

CREATE TABLE IF NOT EXISTS public.corporate_goals_state (
    id int PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    state jsonb NOT NULL DEFAULT '{}'::jsonb,
    updated_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE public.corporate_goals_state IS
    'Single-row JSON state for Oasis corporate goals (DAU baseline, etc.).';

ALTER TABLE public.corporate_goals_state ENABLE ROW LEVEL SECURITY;

INSERT INTO public.corporate_goals_state (id, state)
VALUES (1, '{}'::jsonb)
ON CONFLICT (id) DO NOTHING;
