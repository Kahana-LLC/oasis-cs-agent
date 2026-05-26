/**
 * Database webhook: public.user_plans INSERT/UPDATE → upgrade thank-you or cancelled win-back
 */
import { authorizeServiceRole, bearerToken } from "../_shared/auth.ts";
import {
  cancelledWinback,
  CANCELLED_WINBACK_TRIGGER,
  upgradeThankYou,
  UPGRADE_THANK_YOU_TRIGGER,
} from "../_shared/phase2_emails.ts";
import { envSender } from "../_shared/welcome.ts";
import { loadUser } from "../_shared/users.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type",
};

type WebhookPayload = {
  type?: string;
  table?: string;
  record?: {
    user_id?: string;
    is_active?: boolean | null;
    start_date?: string;
  };
  old_record?: {
    is_active?: boolean | null;
  };
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: cors });
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
  const brevoKey = Deno.env.get("BREVO_API_KEY") ?? "";
  if (!supabaseUrl || !brevoKey) {
    return new Response(JSON.stringify({ error: "Missing env secrets" }), { status: 500, headers: cors });
  }

  if (!(await authorizeServiceRole(req, supabaseUrl))) {
    return new Response(JSON.stringify({ error: "Unauthorized" }), {
      status: 401,
      headers: { ...cors, "content-type": "application/json" },
    });
  }

  const serviceKey =
    (Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "").trim() || bearerToken(req);
  let payload: WebhookPayload;
  try {
    payload = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON" }), { status: 400, headers: cors });
  }

  if (payload.table !== "user_plans" || !payload.record?.user_id) {
    return new Response(JSON.stringify({ skipped: true, reason: "not_user_plans" }), {
      status: 200,
      headers: { ...cors, "content-type": "application/json" },
    });
  }

  const userId = String(payload.record.user_id);
  const isActive = payload.record.is_active === true;
  const wasActive = payload.old_record?.is_active === true;
  const eventType = payload.type ?? "";

  let triggerName: string | null = null;
  if (eventType === "INSERT" && isActive) {
    triggerName = UPGRADE_THANK_YOU_TRIGGER;
  } else if (eventType === "UPDATE" && wasActive && payload.record.is_active === false) {
    triggerName = CANCELLED_WINBACK_TRIGGER;
  } else if (eventType === "UPDATE" && isActive && !wasActive) {
    triggerName = UPGRADE_THANK_YOU_TRIGGER;
  }

  if (!triggerName) {
    return new Response(JSON.stringify({ skipped: true, reason: "no_matching_transition" }), {
      status: 200,
      headers: { ...cors, "content-type": "application/json" },
    });
  }

  const user = await loadUser(supabaseUrl, serviceKey, { user_id: userId });
  if (!user) {
    return new Response(JSON.stringify({ error: "user_not_found", user_id: userId }), {
      status: 404,
      headers: { ...cors, "content-type": "application/json" },
    });
  }

  const sender = envSender();
  try {
    let result: Record<string, unknown>;
    if (triggerName === UPGRADE_THANK_YOU_TRIGGER) {
      result = await upgradeThankYou.send({
        user,
        supabaseUrl,
        serviceKey,
        brevoApiKey: brevoKey,
        templateId: upgradeThankYou.envTemplateId(),
        sender,
      });
    } else {
      result = await cancelledWinback.send({
        user,
        supabaseUrl,
        serviceKey,
        brevoApiKey: brevoKey,
        templateId: cancelledWinback.envTemplateId(),
        sender,
      });
    }
    return new Response(JSON.stringify({ trigger_name: triggerName, ...result }), {
      status: 200,
      headers: { ...cors, "content-type": "application/json" },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e), trigger_name: triggerName }), {
      status: 500,
      headers: { ...cors, "content-type": "application/json" },
    });
  }
});
