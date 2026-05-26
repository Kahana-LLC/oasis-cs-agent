import {
  sendTransactionalTemplate,
  firstNameFromUser,
  welcomeGreetingLine,
  type Sender,
} from "./brevo.ts";
import { wasTriggered, logOutreach } from "./outreach_log.ts";
import { userHasActivePaidPlan } from "./lifecycle_checks.ts";
import type { LifecycleUser } from "./users.ts";

export async function sendLifecycleTemplateEmail(opts: {
  user: LifecycleUser;
  triggerName: string;
  supabaseUrl: string;
  serviceKey: string;
  brevoApiKey: string;
  templateId: number;
  sender: Sender;
  dryRun?: boolean;
  force?: boolean;
  brevoTags?: string[];
  logLabel?: string;
  requireActive?: boolean;
  skipIfPaid?: boolean;
  extraParams?: Record<string, string>;
}): Promise<Record<string, unknown>> {
  const { user, triggerName } = opts;
  if (!user.email?.trim()) {
    throw new Error("User record missing email");
  }
  if (opts.requireActive !== false && user.status && user.status !== "active") {
    return { skipped: true, reason: "user_not_active", user_id: user.user_id };
  }
  if (
    opts.skipIfPaid &&
    (await userHasActivePaidPlan(opts.supabaseUrl, opts.serviceKey, user.user_id))
  ) {
    return { skipped: true, reason: "user_is_paid", user_id: user.user_id, trigger_name: triggerName };
  }

  if (
    !opts.force &&
    (await wasTriggered(opts.supabaseUrl, opts.serviceKey, user.user_id, triggerName))
  ) {
    return {
      skipped: true,
      reason: "already_sent",
      user_id: user.user_id,
      trigger_name: triggerName,
    };
  }

  const greeting = welcomeGreetingLine(user.name ?? null);
  const first = firstNameFromUser(user.name ?? null, user.email);
  const email = user.email.trim();

  if (opts.dryRun) {
    return {
      dry_run: true,
      trigger_name: triggerName,
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
      ...opts.extraParams,
    },
    sender: opts.sender,
    tags: opts.brevoTags ?? [triggerName],
  });

  const label = opts.logLabel ?? triggerName;
  await logOutreach(opts.supabaseUrl, opts.serviceKey, {
    user_id: user.user_id,
    trigger_name: triggerName,
    message_preview: `${label} template ${opts.templateId} messageId=${messageId ?? ""}`,
  });

  return {
    sent: true,
    trigger_name: triggerName,
    user_id: user.user_id,
    email,
    template_id: opts.templateId,
    message_id: messageId,
  };
}

export function envTemplateId(envVar: string, label: string): number {
  const raw = Deno.env.get(envVar) ?? "";
  const id = parseInt(raw, 10);
  if (!id) {
    throw new Error(`${envVar} must be set to Brevo SMTP template numeric id (${label})`);
  }
  return id;
}
