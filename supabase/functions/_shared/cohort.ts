import type { LifecycleUser } from "./users.ts";

export async function callLifecycleCohortRpc(
  rpcName: string,
  supabaseUrl: string,
  serviceKey: string,
  limit: number,
): Promise<LifecycleUser[]> {
  const res = await fetch(`${supabaseUrl}/rest/v1/rpc/${rpcName}`, {
    method: "POST",
    headers: {
      apikey: serviceKey,
      Authorization: `Bearer ${serviceKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ p_limit: limit }),
  });
  if (res.status === 404) {
    throw new Error(`RPC ${rpcName} missing — apply lifecycle phase 2 migration`);
  }
  if (!res.ok) {
    throw new Error(`cohort rpc ${rpcName} ${res.status}: ${await res.text()}`);
  }
  const rows = await res.json();
  if (!Array.isArray(rows)) return [];
  return rows.map((r: Record<string, unknown>) => ({
    user_id: String(r.user_id),
    email: String(r.email),
    name: (r.name as string | null) ?? null,
    status: (r.status as string | null) ?? null,
  }));
}

export async function cohortActivationNudge24h(
  supabaseUrl: string,
  serviceKey: string,
  limit: number,
): Promise<LifecycleUser[]> {
  const res = await fetch(`${supabaseUrl}/rest/v1/rpc/lifecycle_cohort_activation_nudge_24h`, {
    method: "POST",
    headers: {
      apikey: serviceKey,
      Authorization: `Bearer ${serviceKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ p_limit: limit }),
  });
  if (res.status === 404) {
    throw new Error(
      "RPC lifecycle_cohort_activation_nudge_24h missing — apply migration 20260525150000_lifecycle_cohort_activation_nudge.sql",
    );
  }
  if (!res.ok) {
    throw new Error(`cohort rpc ${res.status}: ${await res.text()}`);
  }
  const rows = await res.json();
  if (!Array.isArray(rows)) return [];
  return rows.map((r: Record<string, unknown>) => ({
    user_id: String(r.user_id),
    email: String(r.email),
    name: (r.name as string | null) ?? null,
    status: (r.status as string | null) ?? null,
  }));
}

export async function cohortActivationCsCalendar(
  supabaseUrl: string,
  serviceKey: string,
  limit: number,
): Promise<LifecycleUser[]> {
  const res = await fetch(`${supabaseUrl}/rest/v1/rpc/lifecycle_cohort_activation_cs_calendar`, {
    method: "POST",
    headers: {
      apikey: serviceKey,
      Authorization: `Bearer ${serviceKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ p_limit: limit }),
  });
  if (res.status === 404) {
    throw new Error(
      "RPC lifecycle_cohort_activation_cs_calendar missing — apply migration 20260525210000_lifecycle_cohort_activation_cs_calendar.sql",
    );
  }
  if (!res.ok) {
    throw new Error(`cohort rpc ${res.status}: ${await res.text()}`);
  }
  const rows = await res.json();
  if (!Array.isArray(rows)) return [];
  return rows.map((r: Record<string, unknown>) => ({
    user_id: String(r.user_id),
    email: String(r.email),
    name: (r.name as string | null) ?? null,
    status: (r.status as string | null) ?? null,
  }));
}

export async function cohortNpsDay3(
  supabaseUrl: string,
  serviceKey: string,
  limit: number,
): Promise<LifecycleUser[]> {
  const res = await fetch(`${supabaseUrl}/rest/v1/rpc/lifecycle_cohort_nps_day3`, {
    method: "POST",
    headers: {
      apikey: serviceKey,
      Authorization: `Bearer ${serviceKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ p_limit: limit }),
  });
  if (res.status === 404) {
    throw new Error(
      "RPC lifecycle_cohort_nps_day3 missing — apply migration 20260525220000_lifecycle_cohort_nps_day3.sql",
    );
  }
  if (!res.ok) {
    throw new Error(`cohort rpc ${res.status}: ${await res.text()}`);
  }
  const rows = await res.json();
  if (!Array.isArray(rows)) return [];
  return rows.map((r: Record<string, unknown>) => ({
    user_id: String(r.user_id),
    email: String(r.email),
    name: (r.name as string | null) ?? null,
    status: (r.status as string | null) ?? null,
  }));
}

export async function cohortPmfDay10(
  supabaseUrl: string,
  serviceKey: string,
  limit: number,
): Promise<LifecycleUser[]> {
  const res = await fetch(`${supabaseUrl}/rest/v1/rpc/lifecycle_cohort_pmf_day10`, {
    method: "POST",
    headers: {
      apikey: serviceKey,
      Authorization: `Bearer ${serviceKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({ p_limit: limit }),
  });
  if (res.status === 404) {
    throw new Error(
      "RPC lifecycle_cohort_pmf_day10 missing — apply migration 20260525230000_lifecycle_cohort_pmf_day10.sql",
    );
  }
  if (!res.ok) {
    throw new Error(`cohort rpc ${res.status}: ${await res.text()}`);
  }
  const rows = await res.json();
  if (!Array.isArray(rows)) return [];
  return rows.map((r: Record<string, unknown>) => ({
    user_id: String(r.user_id),
    email: String(r.email),
    name: (r.name as string | null) ?? null,
    status: (r.status as string | null) ?? null,
  }));
}
