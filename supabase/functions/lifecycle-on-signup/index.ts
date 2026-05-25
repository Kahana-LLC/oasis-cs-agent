/**
 * Database webhook: public.users INSERT → welcome_email
 *
 * Configure in Supabase: Database → Webhooks → users INSERT → this function URL
 * Header: Authorization: Bearer <service role> (or use webhook secret + verify)
 */
import { sendWelcomeEmail, envSender, envTemplateIdWelcome } from "../_shared/welcome.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type",
};

type WebhookPayload = {
  type?: string;
  table?: string;
  schema?: string;
  record?: {
    user_id?: string;
    email?: string;
    name?: string | null;
    status?: string | null;
  };
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: cors });
  }

  const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
  const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
  const brevoKey = Deno.env.get("BREVO_API_KEY") ?? "";
  if (!serviceKey || !supabaseUrl || !brevoKey) {
    return new Response(JSON.stringify({ error: "Missing env secrets" }), { status: 500, headers: cors });
  }

  let payload: WebhookPayload;
  try {
    payload = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON" }), { status: 400, headers: cors });
  }

  if (payload.type !== "INSERT" || payload.table !== "users") {
    return new Response(JSON.stringify({ skipped: true, reason: "not_users_insert" }), {
      status: 200,
      headers: { ...cors, "content-type": "application/json" },
    });
  }

  const record = payload.record;
  if (!record?.user_id || !record?.email) {
    return new Response(JSON.stringify({ error: "record missing user_id or email" }), {
      status: 400,
      headers: { ...cors, "content-type": "application/json" },
    });
  }

  try {
    const result = await sendWelcomeEmail({
      user: {
        user_id: String(record.user_id),
        email: String(record.email),
        name: record.name ?? null,
        status: record.status ?? null,
      },
      supabaseUrl,
      serviceKey,
      brevoApiKey: brevoKey,
      templateId: envTemplateIdWelcome(),
      sender: envSender(),
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
