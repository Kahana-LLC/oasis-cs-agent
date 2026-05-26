/**
 * Daily cron: run lifecycle cohorts and send via Brevo.
 *
 * POST { "dry_run"?: bool, "limit"?: number, "triggers"?: string[] }
 * Auth: Authorization: Bearer <service_role>
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
import {
  sendNpsDay3Email,
  NPS_DAY3_TRIGGER,
  envTemplateIdNpsDay3,
} from "../_shared/nps_day3.ts";
import {
  sendPmfDay10Email,
  PMF_DAY10_TRIGGER,
  envTemplateIdPmfDay10,
} from "../_shared/pmf_day10.ts";
import {
  cohortActivationCsCalendar,
  cohortActivationNudge24h,
  cohortNpsDay3,
  cohortPmfDay10,
  callLifecycleCohortRpc,
} from "../_shared/cohort.ts";
import { PHASE2_CRON_TRIGGERS } from "../_shared/phase2_emails.ts";
import { envSender } from "../_shared/welcome.ts";
import type { LifecycleUser } from "../_shared/users.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type",
};

const PHASE1_TRIGGERS = [
  ACTIVATION_NUDGE_TRIGGER,
  ACTIVATION_CS_CALENDAR_TRIGGER,
  NPS_DAY3_TRIGGER,
  PMF_DAY10_TRIGGER,
];

const DEFAULT_TRIGGERS = [
  ...PHASE1_TRIGGERS,
  ...PHASE2_CRON_TRIGGERS.map((t) => t.trigger),
];

async function runTriggerBatch(
  triggerName: string,
  cohort: LifecycleUser[],
  sendFn: (opts: {
    user: LifecycleUser;
    supabaseUrl: string;
    serviceKey: string;
    brevoApiKey: string;
    templateId: number;
    sender: ReturnType<typeof envSender>;
    dryRun: boolean;
  }) => Promise<Record<string, unknown>>,
  opts: {
    supabaseUrl: string;
    serviceKey: string;
    brevoKey: string;
    templateId: number;
    sender: ReturnType<typeof envSender>;
    dryRun: boolean;
  },
): Promise<{ trigger_name: string; cohort_size: number; outcomes: unknown[] }> {
  const batch: unknown[] = [];
  for (const user of cohort) {
    batch.push(
      await sendFn({
        user,
        supabaseUrl: opts.supabaseUrl,
        serviceKey: opts.serviceKey,
        brevoApiKey: opts.brevoKey,
        templateId: opts.templateId,
        sender: opts.sender,
        dryRun: opts.dryRun,
      }),
    );
  }
  return { trigger_name: triggerName, cohort_size: cohort.length, outcomes: batch };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: cors });
  }
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "POST only" }), { status: 405, headers: cors });
  }

  const supabaseUrl = Deno.env.get("SUPABASE_URL") ?? "";
  if (!supabaseUrl || !(await authorizeServiceRole(req, supabaseUrl))) {
    return new Response(JSON.stringify({ error: "Unauthorized" }), {
      status: 401,
      headers: { ...cors, "content-type": "application/json" },
    });
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

  let body: Record<string, unknown> = {};
  try {
    const text = await req.text();
    if (text.trim()) body = JSON.parse(text);
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON" }), { status: 400, headers: cors });
  }

  const dryRun = Boolean(body.dry_run);
  const limit = Math.min(500, Math.max(1, Number(body.limit) || 500));
  const triggers = Array.isArray(body.triggers)
    ? body.triggers.map(String)
    : DEFAULT_TRIGGERS;

  const sender = envSender();
  const summary: Record<string, unknown> = { dry_run: dryRun, limit, triggers, results: [] as unknown[] };
  const runOpts = { supabaseUrl, serviceKey, brevoKey, sender, dryRun };

  try {
    if (triggers.includes(ACTIVATION_NUDGE_TRIGGER)) {
      const cohort = await cohortActivationNudge24h(supabaseUrl, serviceKey, limit);
      (summary.results as unknown[]).push(
        await runTriggerBatch(
          ACTIVATION_NUDGE_TRIGGER,
          cohort,
          sendActivationNudgeEmail,
          { ...runOpts, templateId: envTemplateIdActivationNudge() },
        ),
      );
    }

    if (triggers.includes(ACTIVATION_CS_CALENDAR_TRIGGER)) {
      const cohort = await cohortActivationCsCalendar(supabaseUrl, serviceKey, limit);
      (summary.results as unknown[]).push(
        await runTriggerBatch(
          ACTIVATION_CS_CALENDAR_TRIGGER,
          cohort,
          sendActivationCsCalendarEmail,
          { ...runOpts, templateId: envTemplateIdActivationCsCalendar() },
        ),
      );
    }

    if (triggers.includes(NPS_DAY3_TRIGGER)) {
      const cohort = await cohortNpsDay3(supabaseUrl, serviceKey, limit);
      (summary.results as unknown[]).push(
        await runTriggerBatch(
          NPS_DAY3_TRIGGER,
          cohort,
          sendNpsDay3Email,
          { ...runOpts, templateId: envTemplateIdNpsDay3() },
        ),
      );
    }

    if (triggers.includes(PMF_DAY10_TRIGGER)) {
      const cohort = await cohortPmfDay10(supabaseUrl, serviceKey, limit);
      (summary.results as unknown[]).push(
        await runTriggerBatch(
          PMF_DAY10_TRIGGER,
          cohort,
          sendPmfDay10Email,
          { ...runOpts, templateId: envTemplateIdPmfDay10() },
        ),
      );
    }

    for (const phase2 of PHASE2_CRON_TRIGGERS) {
      if (!triggers.includes(phase2.trigger)) continue;
      const cohortLimit = phase2.trigger === "dead_resurrection_d0"
        ? Math.min(limit, 20)
        : limit;
      let templateId: number;
      try {
        templateId = phase2.envTemplateId();
      } catch (e) {
        (summary.results as unknown[]).push({
          trigger_name: phase2.trigger,
          skipped: true,
          reason: "missing_template_env",
          error: String(e),
        });
        continue;
      }
      const cohort = await callLifecycleCohortRpc(
        phase2.rpc,
        supabaseUrl,
        serviceKey,
        cohortLimit,
      );
      (summary.results as unknown[]).push(
        await runTriggerBatch(phase2.trigger, cohort, phase2.send, {
          ...runOpts,
          templateId,
        }),
      );
    }

    return new Response(JSON.stringify(summary), {
      status: 200,
      headers: { ...cors, "content-type": "application/json" },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e), partial: summary }), {
      status: 500,
      headers: { ...cors, "content-type": "application/json" },
    });
  }
});
