import {
  sendTransactionalTemplate,
  firstNameFromUser,
  welcomeGreetingLine,
  type Sender,
} from "./brevo.ts";
import { wasTriggered, logOutreach } from "./outreach_log.ts";
import type { LifecycleUser } from "./users.ts";

export const NPS_DAY3_TRIGGER = "nps_day3";

export async function sendNpsDay3Email(opts: {
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
    (await wasTriggered(opts.supabaseUrl, opts.serviceKey, user.user_id, NPS_DAY3_TRIGGER))
  ) {
    return {
      skipped: true,
      reason: "already_sent",
      user_id: user.user_id,
      trigger_name: NPS_DAY3_TRIGGER,
    };
  }

  const greeting = welcomeGreetingLine(user.name ?? null);
  const first = firstNameFromUser(user.name ?? null, user.email);
  const email = user.email.trim();

  if (opts.dryRun) {
    return {
      dry_run: true,
      trigger_name: NPS_DAY3_TRIGGER,
      user_id: user.user_id,
      email,
      template_id: opts.templateId,
      first_name: first,
      greeting,
    };
  }

  const { messageId } = await sendTransactionalTemplate({
    apiKey: opts.brevoApiKey,
    templateId: opts.templateId,
    toEmail: email,
    toName: user.name?.trim() ? first : "there",
    params: {
      GREETING: greeting,
      FIRSTNAME: first,
      first_name: first,
      EMAIL: email,
    },
    sender: opts.sender,
    tags: [NPS_DAY3_TRIGGER, "nps_day3"],
  });

  await logOutreach(opts.supabaseUrl, opts.serviceKey, {
    user_id: user.user_id,
    trigger_name: NPS_DAY3_TRIGGER,
    message_preview: `Oasis NPS template ${opts.templateId} messageId=${messageId ?? ""}`,
  });

  return {
    sent: true,
    trigger_name: NPS_DAY3_TRIGGER,
    user_id: user.user_id,
    email,
    template_id: opts.templateId,
    message_id: messageId,
  };
}

export function envTemplateIdNpsDay3(): number {
  const raw = Deno.env.get("BREVO_TEMPLATE_ID_NPS_DAY3") ?? "";
  const id = parseInt(raw, 10);
  if (!id) {
    throw new Error("BREVO_TEMPLATE_ID_NPS_DAY3 must be set to Brevo SMTP template numeric id");
  }
  return id;
}
