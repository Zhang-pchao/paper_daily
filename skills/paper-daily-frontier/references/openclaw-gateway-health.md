# OpenClaw Gateway Health & Restart Recommendation

## Objective

Keep the paper-daily workflow reliable by detecting gateway failures early and suggesting safe recovery actions.

## Check command

```bash
openclaw gateway status
```

## Status interpretation

- **Healthy**: gateway service is running and responsive.
- **Degraded**: service runs but errors/reconnects/timeouts are visible.
- **Down**: service is stopped, crashed, or not responding.

## Recommended recovery sequence

1. First attempt:

```bash
openclaw gateway restart
```

2. If not recovered:

```bash
openclaw gateway stop
openclaw gateway start
```

3. Validate again:

```bash
openclaw gateway status
```

## Reporting template (English)

- Gateway status before action:
- Action taken:
- Gateway status after action:
- Impact on daily paper report:
- Follow-up recommendation:

## Safety notes

- Prefer restart over repeated stop/start loops.
- Do not claim recovery without post-action verification.
- If still unhealthy after one recovery cycle, escalate to manual diagnosis.
