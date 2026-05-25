/** Brevo transactional send (SMTP template API). */

export type Sender = { email: string; name: string };

export async function sendTransactionalTemplate(opts: {
  apiKey: string;
  templateId: number;
  toEmail: string;
  toName: string;
  params?: Record<string, string>;
  sender: Sender;
  tags?: string[];
}): Promise<{ messageId?: string }> {
  const res = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST",
    headers: {
      "api-key": opts.apiKey,
      "content-type": "application/json",
      accept: "application/json",
    },
    body: JSON.stringify({
      templateId: opts.templateId,
      to: [{ email: opts.toEmail, name: opts.toName }],
      params: opts.params ?? {},
      sender: opts.sender,
      tags: opts.tags ?? [],
    }),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(`Brevo ${res.status}: ${JSON.stringify(body)}`);
  }
  return { messageId: (body as { messageId?: string }).messageId };
}

export function firstNameFromUser(name: string | null, email: string): string {
  if (name?.trim()) {
    return name.trim().split(/\s+/)[0]!;
  }
  const local = email.split("@")[0] ?? "there";
  return (
    local.replace(/[._]/g, " ").split(/\s+/)[0]?.replace(/\b\w/g, (c) => c.toUpperCase()) ||
    "there"
  );
}
