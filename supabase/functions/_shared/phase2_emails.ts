import { envTemplateId, sendLifecycleTemplateEmail } from "./lifecycle_template_send.ts";
import type { Sender } from "./brevo.ts";
import type { LifecycleUser } from "./users.ts";

type SendOpts = {
  user: LifecycleUser;
  supabaseUrl: string;
  serviceKey: string;
  brevoApiKey: string;
  templateId: number;
  sender: Sender;
  dryRun?: boolean;
  force?: boolean;
};

function makeSender(
  triggerName: string,
  envVar: string,
  label: string,
  opts?: { skipIfPaid?: boolean; requireActive?: boolean },
) {
  return {
    trigger: triggerName,
    envTemplateId: () => envTemplateId(envVar, label),
    send: (o: SendOpts) =>
      sendLifecycleTemplateEmail({
        ...o,
        triggerName,
        brevoTags: [triggerName],
        logLabel: label,
        skipIfPaid: opts?.skipIfPaid,
        requireActive: opts?.requireActive,
      }),
  };
}

export const LIMIT_HITTER_UPGRADE_TRIGGER = "limit_hitter_upgrade";
export const limitHitterUpgrade = makeSender(
  LIMIT_HITTER_UPGRADE_TRIGGER,
  "BREVO_TEMPLATE_ID_LIMIT_HITTER_D0",
  "Oasis Limit Hitter D0",
  { skipIfPaid: true },
);

export const LIMIT_HITTER_UPGRADE_D7_TRIGGER = "limit_hitter_upgrade_d7";
export const limitHitterUpgradeD7 = makeSender(
  LIMIT_HITTER_UPGRADE_D7_TRIGGER,
  "BREVO_TEMPLATE_ID_LIMIT_HITTER_D7",
  "Oasis Limit Hitter D7",
  { skipIfPaid: true },
);

export const AT_RISK_NURTURE_D0_TRIGGER = "at_risk_nurture_d0";
export const atRiskNurtureD0 = makeSender(
  AT_RISK_NURTURE_D0_TRIGGER,
  "BREVO_TEMPLATE_ID_AT_RISK_D0",
  "Oasis At-risk D0",
  { skipIfPaid: true },
);

export const AT_RISK_NURTURE_D7_TRIGGER = "at_risk_nurture_d7";
export const atRiskNurtureD7 = makeSender(
  AT_RISK_NURTURE_D7_TRIGGER,
  "BREVO_TEMPLATE_ID_AT_RISK_D7",
  "Oasis At-risk D7",
);

export const AT_RISK_NURTURE_D14_TRIGGER = "at_risk_nurture_d14";
export const atRiskNurtureD14 = makeSender(
  AT_RISK_NURTURE_D14_TRIGGER,
  "BREVO_TEMPLATE_ID_AT_RISK_D14",
  "Oasis At-risk D14",
);

export const AT_RISK_NURTURE_D21_TRIGGER = "at_risk_nurture_d21";
export const atRiskNurtureD21 = makeSender(
  AT_RISK_NURTURE_D21_TRIGGER,
  "BREVO_TEMPLATE_ID_AT_RISK_D21",
  "Oasis At-risk D21",
);

export const DEAD_RESURRECTION_D0_TRIGGER = "dead_resurrection_d0";
export const deadResurrectionD0 = makeSender(
  DEAD_RESURRECTION_D0_TRIGGER,
  "BREVO_TEMPLATE_ID_DEAD_D0",
  "Oasis Dead Resurrection D0",
);

export const DEAD_RESURRECTION_D14_TRIGGER = "dead_resurrection_d14";
export const deadResurrectionD14 = makeSender(
  DEAD_RESURRECTION_D14_TRIGGER,
  "BREVO_TEMPLATE_ID_DEAD_D14",
  "Oasis Dead Resurrection D14",
);

export const RETURN_REINFORCEMENT_TRIGGER = "return_reinforcement";
export const returnReinforcement = makeSender(
  RETURN_REINFORCEMENT_TRIGGER,
  "BREVO_TEMPLATE_ID_RETURN_REINFORCEMENT",
  "Oasis Return Reinforcement",
);

export const ENTERPRISE_FOUNDER_TRIGGER = "enterprise_founder";
export const enterpriseFounder = makeSender(
  ENTERPRISE_FOUNDER_TRIGGER,
  "BREVO_TEMPLATE_ID_ENTERPRISE_FOUNDER",
  "Oasis Enterprise Founder",
);

export const ENTERPRISE_EXPANSION_TRIGGER = "enterprise_expansion";
export const enterpriseExpansion = makeSender(
  ENTERPRISE_EXPANSION_TRIGGER,
  "BREVO_TEMPLATE_ID_ENTERPRISE_EXPANSION",
  "Oasis Enterprise Expansion",
);

export const CANCELLED_WINBACK_D14_TRIGGER = "cancelled_winback_d14";
export const cancelledWinbackD14 = makeSender(
  CANCELLED_WINBACK_D14_TRIGGER,
  "BREVO_TEMPLATE_ID_CANCELLED_D14",
  "Oasis Cancelled Win-back D14",
  { requireActive: false },
);

export const UPGRADE_THANK_YOU_TRIGGER = "upgrade_thank_you";
export const upgradeThankYou = makeSender(
  UPGRADE_THANK_YOU_TRIGGER,
  "BREVO_TEMPLATE_ID_UPGRADE_THANK_YOU",
  "Oasis Paid Zen Welcome",
  { requireActive: false },
);

export const CANCELLED_WINBACK_TRIGGER = "cancelled_winback";
export const cancelledWinback = makeSender(
  CANCELLED_WINBACK_TRIGGER,
  "BREVO_TEMPLATE_ID_CANCELLED_D0",
  "Oasis Cancelled Win-back D0",
  { requireActive: false },
);

export type Phase2CronTrigger = {
  trigger: string;
  rpc: string;
  send: (o: SendOpts) => Promise<Record<string, unknown>>;
  envTemplateId: () => number;
};

/** Daily-cron batch triggers (RPC cohort → send). */
export const PHASE2_CRON_TRIGGERS: Phase2CronTrigger[] = [
  {
    trigger: LIMIT_HITTER_UPGRADE_TRIGGER,
    rpc: "lifecycle_cohort_limit_hitter_upgrade",
    send: limitHitterUpgrade.send,
    envTemplateId: limitHitterUpgrade.envTemplateId,
  },
  {
    trigger: LIMIT_HITTER_UPGRADE_D7_TRIGGER,
    rpc: "lifecycle_cohort_limit_hitter_upgrade_d7",
    send: limitHitterUpgradeD7.send,
    envTemplateId: limitHitterUpgradeD7.envTemplateId,
  },
  {
    trigger: AT_RISK_NURTURE_D0_TRIGGER,
    rpc: "lifecycle_cohort_at_risk_nurture_d0",
    send: atRiskNurtureD0.send,
    envTemplateId: atRiskNurtureD0.envTemplateId,
  },
  {
    trigger: AT_RISK_NURTURE_D7_TRIGGER,
    rpc: "lifecycle_cohort_at_risk_nurture_d7",
    send: atRiskNurtureD7.send,
    envTemplateId: atRiskNurtureD7.envTemplateId,
  },
  {
    trigger: AT_RISK_NURTURE_D14_TRIGGER,
    rpc: "lifecycle_cohort_at_risk_nurture_d14",
    send: atRiskNurtureD14.send,
    envTemplateId: atRiskNurtureD14.envTemplateId,
  },
  {
    trigger: AT_RISK_NURTURE_D21_TRIGGER,
    rpc: "lifecycle_cohort_at_risk_nurture_d21",
    send: atRiskNurtureD21.send,
    envTemplateId: atRiskNurtureD21.envTemplateId,
  },
  {
    trigger: DEAD_RESURRECTION_D0_TRIGGER,
    rpc: "lifecycle_cohort_dead_resurrection_d0",
    send: deadResurrectionD0.send,
    envTemplateId: deadResurrectionD0.envTemplateId,
  },
  {
    trigger: DEAD_RESURRECTION_D14_TRIGGER,
    rpc: "lifecycle_cohort_dead_resurrection_d14",
    send: deadResurrectionD14.send,
    envTemplateId: deadResurrectionD14.envTemplateId,
  },
  {
    trigger: RETURN_REINFORCEMENT_TRIGGER,
    rpc: "lifecycle_cohort_return_reinforcement",
    send: returnReinforcement.send,
    envTemplateId: returnReinforcement.envTemplateId,
  },
  {
    trigger: ENTERPRISE_FOUNDER_TRIGGER,
    rpc: "lifecycle_cohort_enterprise_founder",
    send: enterpriseFounder.send,
    envTemplateId: enterpriseFounder.envTemplateId,
  },
  {
    trigger: ENTERPRISE_EXPANSION_TRIGGER,
    rpc: "lifecycle_cohort_enterprise_expansion",
    send: enterpriseExpansion.send,
    envTemplateId: enterpriseExpansion.envTemplateId,
  },
  {
    trigger: CANCELLED_WINBACK_D14_TRIGGER,
    rpc: "lifecycle_cohort_cancelled_winback_d14",
    send: cancelledWinbackD14.send,
    envTemplateId: cancelledWinbackD14.envTemplateId,
  },
];
