/**
 * POST { "trigger_name": "welcome_email", "user_id": "<uuid>", "dry_run"?: bool, "force"?: bool }
 * Or { "trigger_name": "welcome_email", "email": "...", ... }
 *
 * Auth: Authorization: Bearer <SUPABASE_SERVICE_ROLE_KEY>
 */
import { sendWelcomeEmail, WELCOME_TRIGGER, envSender, envTemplateIdWelcome } from "../_shared/welcome.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: cors });
  }
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "POST only" }), { status: 405, headers: cors });
  }

  const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
  const auth = req.headers.get("Authorization") ?? "";
  if (!serviceKey || auth !== `Bearer ${serviceKey}`) {
    return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401, headers: cors });
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
  const brevoKey = Deno.env.get("BREVO_API_KEY") ?? "";
  if (!supabaseUrl || !brevoKey) {
    return new Response(JSON.stringify({ error: "Missing SUPABASE_URL or BREVO_API_KEY" }), {
      status: 500,
      headers: cors,
    });
  }

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON" }), { status: 400, headers: cors });
  }

  const triggerName = String(body.trigger_name ?? "");
  if (triggerName !== WELCOME_TRIGGER) {
    return new Response(
      JSON.stringify({
        error: "not_implemented",
        message: "Only welcome_email is implemented. Next: activation_nudge_24h.",
        implemented: [WELCOME_TRIGGER],
      }),
      { status: 501, headers: { ...cors, "content-type": "application/json" } },
    );
  }

  const dryRun = Boolean(body.dry_run);
  const force = Boolean(body.force);
  const userId = body.user_id ? String(body.user_id) : "";
  const email = body.email ? String(body.email) : "";

  let user: { user_id: string; email: string; name?: string | null; status?: string | null };
  if (userId) {
    const res = await fetch(
      `${supabaseUrl}/rest/v1/users?user_id=eq.${userId}&select=user_id,email,name,status&limit=1`,
      {
        headers: { apikey: serviceKey, Authorization: `Bearer ${serviceKey}` },
      },
    );
    if (!res.ok) {
      return new Response(await res.text(), { status: res.status, headers: cors });
    }
    const rows = await res.json();
    if (!Array.isArray(rows) || !rows.length) {
      return new Response(JSON.stringify({ error: "user_not_found", user_id: userId }), {
        status: 404,
        headers: { ...cors, "content-type": "application/json" },
      });
    }
    user = rows[0];
  } else if (email) {
    const res = await fetch(
      `${supabaseUrl}/rest/v1/users?email=eq.${encodeURIComponent(email)}&select=user_id,email,name,status&limit=1`,
      {
        headers: { apikey: serviceKey, Authorization: `Bearer ${serviceKey}` },
      },
    );
    if (!res.ok) {
      return new Response(await res.text(), { status: res.status, headers: cors });
    }
    const rows = await res.json();
    if (!Array.isArray(rows) || !rows.length) {
      return new Response(JSON.stringify({ error: "user_not_found", email }), {
        status: 404,
        headers: { ...cors, "content-type": "application/json" },
      });
    }
    user = rows[0];
  } else {
    return new Response(JSON.stringify({ error: "Provide user_id or email" }), {
      status: 400,
      headers: { ...cors, "content-type": "application/json" },
    });
  }

  try {
    const result = await sendWelcomeEmail({
      user,
      supabaseUrl,
      serviceKey,
      brevoApiKey: brevoKey,
      templateId: envTemplateIdWelcome(),
      sender: envSender(),
      dryRun,
      force,
    });
    return new Response(JSON.stringify(result), {
      status: 200,
      headers: { ...cors, "content-type": "application/json" },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), {
      status: 500,
      headers: { ...cors, "content-type": "application/json" },
    });
  }
});
