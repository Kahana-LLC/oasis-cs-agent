/**
 * POST { "trigger_name": <any shipped lifecycle trigger>, "user_id" | "email", ... }
 *
 * Auth: Authorization: Bearer <service_role key>
 */
import { authorizeServiceRole, bearerToken } from "../_shared/auth.ts";
import {
  sendActivationCsCalendarEmail,
  ACTIVATION_CS_CALENDAR_TRIGGER,
  envTemplateIdActivationCsCalendar,
} from "../_shared/activation_cs_calendar.ts";
import {
  sendActivationNudgeEmail,
  ACTIVATION_NUDGE_TRIGGER,
  envTemplateIdActivationNudge,
} from "../_shared/activation_nudge.ts";
import { sendNpsDay3Email, NPS_DAY3_TRIGGER, envTemplateIdNpsDay3 } from "../_shared/nps_day3.ts";
import { sendPmfDay10Email, PMF_DAY10_TRIGGER, envTemplateIdPmfDay10 } from "../_shared/pmf_day10.ts";
import {
  PHASE2_CRON_TRIGGERS,
  cancelledWinback,
  CANCELLED_WINBACK_TRIGGER,
  upgradeThankYou,
  UPGRADE_THANK_YOU_TRIGGER,
} from "../_shared/phase2_emails.ts";
import { sendWelcomeEmail, WELCOME_TRIGGER, envSender, envTemplateIdWelcome } from "../_shared/welcome.ts";
import { loadUser } from "../_shared/users.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type",
};

const PHASE2_BY_TRIGGER = new Map(
  PHASE2_CRON_TRIGGERS.map((t) => [t.trigger, t]),
);
PHASE2_BY_TRIGGER.set(UPGRADE_THANK_YOU_TRIGGER, upgradeThankYou);
PHASE2_BY_TRIGGER.set(CANCELLED_WINBACK_TRIGGER, cancelledWinback);

const IMPLEMENTED = [
  WELCOME_TRIGGER,
  ACTIVATION_NUDGE_TRIGGER,
  ACTIVATION_CS_CALENDAR_TRIGGER,
  NPS_DAY3_TRIGGER,
  PMF_DAY10_TRIGGER,
  ...PHASE2_BY_TRIGGER.keys(),
];

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: cors });
  }
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "POST only" }), { status: 405, headers: cors });
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
  if (!supabaseUrl || !(await authorizeServiceRole(req, supabaseUrl))) {
    return new Response(
      JSON.stringify({
        error: "Unauthorized",
        hint: "Use Authorization: Bearer <service_role_key> from Dashboard → API.",
      }),
      { status: 401, headers: { ...cors, "content-type": "application/json" } },
    );
  }
  const serviceKey =
    (Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "").trim() || bearerToken(req);
  const brevoKey = Deno.env.get("BREVO_API_KEY") ?? "";
  if (!brevoKey) {
    return new Response(JSON.stringify({ error: "Missing BREVO_API_KEY" }), {
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
  if (!IMPLEMENTED.includes(triggerName)) {
    return new Response(
      JSON.stringify({
        error: "not_implemented",
        message: `Unknown trigger_name. Implemented: ${IMPLEMENTED.join(", ")}`,
        implemented: [...IMPLEMENTED],
      }),
      { status: 501, headers: { ...cors, "content-type": "application/json" } },
    );
  }

  const dryRun = Boolean(body.dry_run);
  const force = Boolean(body.force);
  const userId = body.user_id ? String(body.user_id) : "";
  const email = body.email ? String(body.email) : "";
  if (!userId && !email) {
    return new Response(JSON.stringify({ error: "Provide user_id or email" }), {
      status: 400,
      headers: { ...cors, "content-type": "application/json" },
    });
  }

  const user = await loadUser(supabaseUrl, serviceKey, {
    user_id: userId || undefined,
    email: email || undefined,
  });
  if (!user) {
    return new Response(JSON.stringify({ error: "user_not_found", user_id: userId, email }), {
      status: 404,
      headers: { ...cors, "content-type": "application/json" },
    });
  }

  const sender = envSender();
  try {
    let result: Record<string, unknown>;
    if (triggerName === WELCOME_TRIGGER) {
      result = await sendWelcomeEmail({
        user,
        supabaseUrl,
        serviceKey,
        brevoApiKey: brevoKey,
        templateId: envTemplateIdWelcome(),
        sender,
        dryRun,
        force,
      });
    } else if (triggerName === ACTIVATION_NUDGE_TRIGGER) {
      result = await sendActivationNudgeEmail({
        user,
        supabaseUrl,
        serviceKey,
        brevoApiKey: brevoKey,
        templateId: envTemplateIdActivationNudge(),
        sender,
        dryRun,
        force,
      });
    } else if (triggerName === ACTIVATION_CS_CALENDAR_TRIGGER) {
      result = await sendActivationCsCalendarEmail({
        user,
        supabaseUrl,
        serviceKey,
        brevoApiKey: brevoKey,
        templateId: envTemplateIdActivationCsCalendar(),
        sender,
        dryRun,
        force,
      });
    } else if (triggerName === NPS_DAY3_TRIGGER) {
      result = await sendNpsDay3Email({
        user,
        supabaseUrl,
        serviceKey,
        brevoApiKey: brevoKey,
        templateId: envTemplateIdNpsDay3(),
        sender,
        dryRun,
        force,
      });
    } else if (triggerName === PMF_DAY10_TRIGGER) {
      result = await sendPmfDay10Email({
        user,
        supabaseUrl,
        serviceKey,
        brevoApiKey: brevoKey,
        templateId: envTemplateIdPmfDay10(),
        sender,
        dryRun,
        force,
      });
    } else {
      const phase2 = PHASE2_BY_TRIGGER.get(triggerName);
      if (!phase2) {
        throw new Error(`Phase 2 trigger not configured: ${triggerName}`);
      }
      result = await phase2.send({
        user,
        supabaseUrl,
        serviceKey,
        brevoApiKey: brevoKey,
        templateId: phase2.envTemplateId(),
        sender,
        dryRun,
        force,
      });
    }
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
