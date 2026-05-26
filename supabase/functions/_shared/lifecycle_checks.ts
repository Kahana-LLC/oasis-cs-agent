/** Product eligibility checks for lifecycle cohorts (PostgREST). */

const PAID_TRACKING_START = "2026-05-24";

export async function userHasActivePaidPlan(
  supabaseUrl: string,
  serviceKey: string,
  userId: string,
): Promise<boolean> {
  const url = new URL(`${supabaseUrl}/rest/v1/user_plans`);
  url.searchParams.set("select", "user_plan_id");
  url.searchParams.set("user_id", `eq.${userId}`);
  url.searchParams.set("is_active", "eq.true");
  url.searchParams.set("start_date", `gte.${PAID_TRACKING_START}`);
  url.searchParams.set("limit", "1");
  const res = await fetch(url.toString(), {
    headers: { apikey: serviceKey, Authorization: `Bearer ${serviceKey}` },
  });
  if (res.status === 404) return false;
  if (!res.ok) throw new Error(`user_plans read ${res.status}: ${await res.text()}`);
  const rows = await res.json();
  return Array.isArray(rows) && rows.length > 0;
}

export async function userHasLlmUsage(
  supabaseUrl: string,
  serviceKey: string,
  userId: string,
): Promise<boolean> {
  const url = new URL(`${supabaseUrl}/rest/v1/llm_usage`);
  url.searchParams.set("select", "usage_id");
  url.searchParams.set("user_id", `eq.${userId}`);
  url.searchParams.set("limit", "1");
  const res = await fetch(url.toString(), {
    headers: { apikey: serviceKey, Authorization: `Bearer ${serviceKey}` },
  });
  if (!res.ok) throw new Error(`llm_usage read ${res.status}: ${await res.text()}`);
  const rows = await res.json();
  return Array.isArray(rows) && rows.length > 0;
}

export async function userHasFeedbackEvents(
  supabaseUrl: string,
  serviceKey: string,
  userId: string,
): Promise<boolean> {
  const url = new URL(`${supabaseUrl}/rest/v1/feedback_events`);
  url.searchParams.set("select", "feedback_id");
  url.searchParams.set("user_id", `eq.${userId}`);
  url.searchParams.set("limit", "1");
  const res = await fetch(url.toString(), {
    headers: { apikey: serviceKey, Authorization: `Bearer ${serviceKey}` },
  });
  if (!res.ok) throw new Error(`feedback_events read ${res.status}: ${await res.text()}`);
  const rows = await res.json();
  return Array.isArray(rows) && rows.length > 0;
}
