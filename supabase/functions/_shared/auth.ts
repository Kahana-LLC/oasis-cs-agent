/** Authorize admin callers: Bearer token must work as Supabase service role against REST. */

export function bearerToken(req: Request): string {
  const auth = (req.headers.get("Authorization") ?? "").trim();
  if (auth.toLowerCase().startsWith("bearer ")) {
    return auth.slice(7).trim();
  }
  return auth;
}

export async function authorizeServiceRole(
  req: Request,
  supabaseUrl: string,
): Promise<boolean> {
  const token = bearerToken(req);
  if (!token) return false;

  // Optional dedicated secret (set via: supabase secrets set LIFECYCLE_INVOKE_SECRET=...)
  const invokeSecret = (Deno.env.get("LIFECYCLE_INVOKE_SECRET") ?? "").trim();
  if (invokeSecret && token === invokeSecret) return true;

  // Accept any key that can read users (service role or matching injected secret)
  const res = await fetch(`${supabaseUrl}/rest/v1/users?select=user_id&limit=1`, {
    headers: {
      apikey: token,
      Authorization: `Bearer ${token}`,
    },
  });
  return res.ok;
}
