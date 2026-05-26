/** Product eligibility checks for lifecycle cohorts (PostgREST). */

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
