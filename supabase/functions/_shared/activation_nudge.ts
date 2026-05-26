import {
  sendTransactionalTemplate,
  firstNameFromUser,
  welcomeGreetingLine,
  type Sender,
} from "./brevo.ts";
import { userHasLlmUsage } from "./lifecycle_checks.ts";
import { wasTriggered, logOutreach } from "./outreach_log.ts";
import type { LifecycleUser } from "./users.ts";

export const ACTIVATION_NUDGE_TRIGGER = "activation_nudge_24h";

export async function sendActivationNudgeEmail(opts: {
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
    (await wasTriggered(opts.supabaseUrl, opts.serviceKey, user.user_id, ACTIVATION_NUDGE_TRIGGER))
  ) {
    return {
      skipped: true,
      reason: "already_sent",
      user_id: user.user_id,
      trigger_name: ACTIVATION_NUDGE_TRIGGER,
    };
  }

  const hasPrompt = await userHasLlmUsage(
    opts.supabaseUrl,
    opts.serviceKey,
    user.user_id,
  );
  if (hasPrompt) {
    return {
      skipped: true,
      reason: "has_first_prompt",
      user_id: user.user_id,
      trigger_name: ACTIVATION_NUDGE_TRIGGER,
    };
  }

  const greeting = welcomeGreetingLine(user.name ?? null);
  const first = firstNameFromUser(user.name ?? null, user.email);
  if (opts.dryRun) {
    return {
      dry_run: true,
      trigger_name: ACTIVATION_NUDGE_TRIGGER,
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
    tags: [ACTIVATION_NUDGE_TRIGGER, "activation_nudge"],
  });

  await logOutreach(opts.supabaseUrl, opts.serviceKey, {
    user_id: user.user_id,
    trigger_name: ACTIVATION_NUDGE_TRIGGER,
    message_preview: `Oasis Activation Nudge template ${opts.templateId} messageId=${messageId ?? ""}`,
  });

  return {
    sent: true,
    trigger_name: ACTIVATION_NUDGE_TRIGGER,
    user_id: user.user_id,
    email: user.email,
    template_id: opts.templateId,
    message_id: messageId,
  };
}

export function envTemplateIdActivationNudge(): number {
  const raw = Deno.env.get("BREVO_TEMPLATE_ID_ACTIVATION_NUDGE") ?? "";
  const id = parseInt(raw, 10);
  if (!id) {
    throw new Error(
      "BREVO_TEMPLATE_ID_ACTIVATION_NUDGE must be set to Brevo SMTP template numeric id",
    );
  }
  return id;
}
