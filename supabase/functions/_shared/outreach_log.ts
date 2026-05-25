/** cs_outreach_log via PostgREST (service role). */

export async function wasTriggered(
  supabaseUrl: string,
  serviceKey: string,
  userId: string,
  triggerName: string,
): Promise<boolean> {
  const url = new URL(`${supabaseUrl}/rest/v1/cs_outreach_log`);
  url.searchParams.set("select", "id");
  url.searchParams.set("user_id", `eq.${userId}`);
  url.searchParams.set("trigger_name", `eq.${triggerName}`);
  url.searchParams.set("limit", "1");
  const res = await fetch(url.toString(), {
    headers: {
      apikey: serviceKey,
      Authorization: `Bearer ${serviceKey}`,
    },
  });
  if (res.status === 404) {
    throw new Error(
      "cs_outreach_log table missing — apply migration 20260525140000_cs_outreach_log.sql",
    );
  }
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`outreach_log read ${res.status}: ${err}`);
  }
  const rows = await res.json();
  return Array.isArray(rows) && rows.length > 0;
}

export async function logOutreach(
  supabaseUrl: string,
  serviceKey: string,
  row: {
    user_id: string;
    trigger_name: string;
    channel?: string;
    message_preview?: string;
    provider?: string;
  },
): Promise<void> {
  const res = await fetch(`${supabaseUrl}/rest/v1/cs_outreach_log`, {
    method: "POST",
    headers: {
      apikey: serviceKey,
      Authorization: `Bearer ${serviceKey}`,
      "content-type": "application/json",
      Prefer: "return=minimal",
    },
    body: JSON.stringify({
      channel: "email",
      provider: "brevo",
      ...row,
    }),
  });
  if (res.status === 409) return;
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`outreach_log insert ${res.status}: ${err}`);
  }
}
