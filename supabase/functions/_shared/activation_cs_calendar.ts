import {
  sendTransactionalTemplate,
  firstNameFromUser,
  welcomeGreetingLine,
  type Sender,
} from "./brevo.ts";
import { userHasFeedbackEvents, userHasLlmUsage } from "./lifecycle_checks.ts";
import { wasTriggered, logOutreach } from "./outreach_log.ts";
import type { LifecycleUser } from "./users.ts";

export const ACTIVATION_CS_CALENDAR_TRIGGER = "activation_cs_calendar";

export async function sendActivationCsCalendarEmail(opts: {
  user: LifecycleUser;
  supabaseUrl: string;
  serviceKey: string;
  brevoApiKey: string;
  templateId: number;
  sender: Sender;
  dryRun?: boolean;
  force?: boolean;
}): Promise<Record<string, unknown>> {
  const { user } = opts;
  if (!user.email?.trim()) {
    throw new Error("User record missing email");
  }
  if (user.status && user.status !== "active") {
    return { skipped: true, reason: "user_not_active", user_id: user.user_id };
  }

  if (
    !opts.force &&
    (await wasTriggered(opts.supabaseUrl, opts.serviceKey, user.user_id, ACTIVATION_CS_CALENDAR_TRIGGER))
  ) {
    return {
      skipped: true,
      reason: "already_sent",
      user_id: user.user_id,
      trigger_name: ACTIVATION_CS_CALENDAR_TRIGGER,
    };
  }

  if (await userHasLlmUsage(opts.supabaseUrl, opts.serviceKey, user.user_id)) {
    return {
      skipped: true,
      reason: "has_first_prompt",
      user_id: user.user_id,
      trigger_name: ACTIVATION_CS_CALENDAR_TRIGGER,
    };
  }

  if (await userHasFeedbackEvents(opts.supabaseUrl, opts.serviceKey, user.user_id)) {
    return {
      skipped: true,
      reason: "has_training",
      user_id: user.user_id,
      trigger_name: ACTIVATION_CS_CALENDAR_TRIGGER,
    };
  }

  const greeting = welcomeGreetingLine(user.name ?? null);
  const first = firstNameFromUser(user.name ?? null, user.email);
  if (opts.dryRun) {
    return {
      dry_run: true,
      trigger_name: ACTIVATION_CS_CALENDAR_TRIGGER,
      user_id: user.user_id,
      email: user.email,
      template_id: opts.templateId,
      first_name: first,
      greeting,
    };
  }

  const { messageId } = await sendTransactionalTemplate({
    apiKey: opts.brevoApiKey,
    templateId: opts.templateId,
    toEmail: user.email,
    toName: user.name?.trim() ? first : "there",
    params: { GREETING: greeting, FIRSTNAME: first, first_name: first },
    sender: opts.sender,
    tags: [ACTIVATION_CS_CALENDAR_TRIGGER, "activation_cs_calendar"],
  });

  await logOutreach(opts.supabaseUrl, opts.serviceKey, {
    user_id: user.user_id,
    trigger_name: ACTIVATION_CS_CALENDAR_TRIGGER,
    message_preview: `Oasis Activation CS Calendar template ${opts.templateId} messageId=${messageId ?? ""}`,
  });

  return {
    sent: true,
    trigger_name: ACTIVATION_CS_CALENDAR_TRIGGER,
    user_id: user.user_id,
    email: user.email,
    template_id: opts.templateId,
    message_id: messageId,
  };
}

export function envTemplateIdActivationCsCalendar(): number {
  const raw = Deno.env.get("BREVO_TEMPLATE_ID_ACTIVATION_CS_CALENDAR") ?? "";
  const id = parseInt(raw, 10);
  if (!id) {
    throw new Error(
      "BREVO_TEMPLATE_ID_ACTIVATION_CS_CALENDAR must be set to Brevo SMTP template numeric id",
    );
  }
  return id;
}
