#!/usr/bin/env bash
# Push main to canonical (analytics) then Kahana mirror (origin). AdamKershner wins on conflict.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BRANCH="${1:-main}"

if ! git remote get-url analytics &>/dev/null; then
  echo "Missing remote 'analytics'. Add: git remote add analytics https://github.com/AdamKershner/oasis-analytics.git" >&2
  exit 1
fi
if ! git remote get-url origin &>/dev/null; then
  echo "Missing remote 'origin'. Add: git remote add origin https://github.com/Kahana-LLC/oasis-cs-agent.git" >&2
  exit 1
fi

echo "→ analytics (canonical / Vercel) …"
git push analytics "$BRANCH"

echo "→ origin (Kahana-LLC mirror) …"
git push origin "$BRANCH"

echo "Done. Verify:"
git fetch analytics origin 2>/dev/null || true
echo "  analytics/main $(git rev-parse analytics/main 2>/dev/null || echo '?')"
echo "  origin/main    $(git rev-parse origin/main 2>/dev/null || echo '?')"
