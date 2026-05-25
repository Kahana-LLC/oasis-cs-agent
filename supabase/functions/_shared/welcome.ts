import { sendTransactionalTemplate, firstNameFromUser, type Sender } from "./brevo.ts";
import { wasTriggered, logOutreach } from "./outreach_log.ts";

export const WELCOME_TRIGGER = "welcome_email";

export type WelcomeUser = {
  user_id: string;
  email: string;
  name?: string | null;
  status?: string | null;
};

export async function sendWelcomeEmail(opts: {
  user: WelcomeUser;
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

  if (!opts.force && (await wasTriggered(opts.supabaseUrl, opts.serviceKey, user.user_id, WELCOME_TRIGGER))) {
    return {
      skipped: true,
      reason: "already_sent",
      user_id: user.user_id,
      trigger_name: WELCOME_TRIGGER,
    };
  }

  const first = firstNameFromUser(user.name ?? null, user.email);
  if (opts.dryRun) {
    return {
      dry_run: true,
      trigger_name: WELCOME_TRIGGER,
      user_id: user.user_id,
      email: user.email,
      template_id: opts.templateId,
      first_name: first,
    };
  }

  const { messageId } = await sendTransactionalTemplate({
    apiKey: opts.brevoApiKey,
    templateId: opts.templateId,
    toEmail: user.email,
    toName: first,
    params: { FIRSTNAME: first, first_name: first },
    sender: opts.sender,
    tags: [WELCOME_TRIGGER, "welcome"],
  });

  await logOutreach(opts.supabaseUrl, opts.serviceKey, {
    user_id: user.user_id,
    trigger_name: WELCOME_TRIGGER,
    message_preview: `Oasis Welcome template ${opts.templateId} messageId=${messageId ?? ""}`,
  });

  return {
    sent: true,
    trigger_name: WELCOME_TRIGGER,
    user_id: user.user_id,
    email: user.email,
    template_id: opts.templateId,
    message_id: messageId,
  };
}

export function envSender(): Sender {
  const email = Deno.env.get("LIFECYCLE_SENDER_EMAIL") ?? Deno.env.get("FROM_EMAIL") ?? "";
  const name =
    Deno.env.get("LIFECYCLE_SENDER_NAME") ??
    Deno.env.get("FROM_NAME") ??
    "Adam from Oasis";
  if (!email) throw new Error("LIFECYCLE_SENDER_EMAIL or FROM_EMAIL required");
  return { email, name };
}

export function envTemplateIdWelcome(): number {
  const raw = Deno.env.get("BREVO_TEMPLATE_ID_WELCOME") ?? "";
  const id = parseInt(raw, 10);
  if (!id) {
    throw new Error("BREVO_TEMPLATE_ID_WELCOME must be set to Brevo SMTP template numeric id");
  }
  return id;
}
