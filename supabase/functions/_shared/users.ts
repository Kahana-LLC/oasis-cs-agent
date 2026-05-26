/** Load public.users rows via PostgREST. */

export type LifecycleUser = {
  user_id: string;
  email: string;
  name?: string | null;
  status?: string | null;
};

export async function loadUser(
  supabaseUrl: string,
  serviceKey: string,
  opts: { user_id?: string; email?: string },
): Promise<LifecycleUser | null> {
  if (opts.user_id) {
    const res = await fetch(
      `${supabaseUrl}/rest/v1/users?user_id=eq.${opts.user_id}&select=user_id,email,name,status&limit=1`,
      { headers: { apikey: serviceKey, Authorization: `Bearer ${serviceKey}` } },
    );
    if (!res.ok) throw new Error(`users read ${res.status}: ${await res.text()}`);
    const rows = await res.json();
    return Array.isArray(rows) && rows.length ? rows[0] : null;
  }
  if (opts.email) {
    const res = await fetch(
      `${supabaseUrl}/rest/v1/users?email=eq.${encodeURIComponent(opts.email)}&select=user_id,email,name,status&limit=1`,
      { headers: { apikey: serviceKey, Authorization: `Bearer ${serviceKey}` } },
    );
    if (!res.ok) throw new Error(`users read ${res.status}: ${await res.text()}`);
    const rows = await res.json();
    return Array.isArray(rows) && rows.length ? rows[0] : null;
  }
  return null;
}
