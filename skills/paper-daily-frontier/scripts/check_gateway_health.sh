#!/usr/bin/env bash
set -euo pipefail

# Check OpenClaw gateway status and print a restart recommendation.
# This script is advisory: it does not restart by default.

status_output="$(openclaw gateway status 2>&1 || true)"
echo "$status_output"

echo ""
if echo "$status_output" | grep -Eiq "running|healthy|active"; then
  echo "Assessment: HEALTHY"
  echo "Recommendation: No restart required."
else
  echo "Assessment: DEGRADED_OR_DOWN"
  echo "Recommendation: Run 'openclaw gateway restart'."
  echo "If unresolved, run 'openclaw gateway stop && openclaw gateway start', then re-check status."
fi
