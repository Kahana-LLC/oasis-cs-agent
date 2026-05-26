import {
  sendTransactionalTemplate,
  firstNameFromUser,
  welcomeGreetingLine,
  type Sender,
} from "./brevo.ts";
import { wasTriggered, logOutreach } from "./outreach_log.ts";
import type { LifecycleUser } from "./users.ts";

export const PMF_DAY10_TRIGGER = "pmf_day10";

export async function sendPmfDay10Email(opts: {
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
    (await wasTriggered(opts.supabaseUrl, opts.serviceKey, user.user_id, PMF_DAY10_TRIGGER))
  ) {
    return {
      skipped: true,
      reason: "already_sent",
      user_id: user.user_id,
      trigger_name: PMF_DAY10_TRIGGER,
    };
  }

  const greeting = welcomeGreetingLine(user.name ?? null);
  const first = firstNameFromUser(user.name ?? null, user.email);
  const email = user.email.trim();

  if (opts.dryRun) {
    return {
      dry_run: true,
      trigger_name: PMF_DAY10_TRIGGER,
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
    tags: [PMF_DAY10_TRIGGER, "pmf_day10"],
  });

  await logOutreach(opts.supabaseUrl, opts.serviceKey, {
    user_id: user.user_id,
    trigger_name: PMF_DAY10_TRIGGER,
    message_preview: `Oasis PMF template ${opts.templateId} messageId=${messageId ?? ""}`,
  });

  return {
    sent: true,
    trigger_name: PMF_DAY10_TRIGGER,
    user_id: user.user_id,
    email,
    template_id: opts.templateId,
    message_id: messageId,
  };
}

export function envTemplateIdPmfDay10(): number {
  const raw = Deno.env.get("BREVO_TEMPLATE_ID_PMF_DAY10") ?? "";
  const id = parseInt(raw, 10);
  if (!id) {
    throw new Error("BREVO_TEMPLATE_ID_PMF_DAY10 must be set to Brevo SMTP template numeric id");
  }
  return id;
}
