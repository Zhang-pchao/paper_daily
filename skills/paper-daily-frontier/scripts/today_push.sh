#!/usr/bin/env bash
set -euo pipefail

# Trigger command for: 今日推送
# Generates English report + JSON under ./reports

python3 "$(dirname "$0")/run_today_push.py" --top-k 1 --days 2 --out-dir "$(pwd)/reports"
