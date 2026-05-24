-- Daily compact baseline metrics for KPI deltas (analytics dashboard).
-- Apply via Supabase SQL editor or: supabase db push / MCP apply_migration

CREATE TABLE IF NOT EXISTS public.baseline_metric_history (
    snapshot_date date PRIMARY KEY,
    metrics jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE public.baseline_metric_history IS
    'One row per calendar day of compact Oasis baseline metrics for delta comparisons.';

ALTER TABLE public.baseline_metric_history ENABLE ROW LEVEL SECURITY;

-- No policies: only service role (bypasses RLS) may read/write.

CREATE INDEX IF NOT EXISTS baseline_metric_history_updated_at_idx
    ON public.baseline_metric_history (updated_at DESC);
