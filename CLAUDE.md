# Claude Code context

See README.md for full project description and setup.

## Data source

API: `https://api.spot-hinta.fi/SmartMonitoring?PrivateKey=...`

Returns hourly relay records. Each row = one hour, with fields:
- `relenimi` — relay name (we filter for `"LVV"`)
- `relestatus` — bool, was the relay on during that hour
- `pvm` — timestamp (UTC)

## Key design decisions

**Scheduling:** Single cron at `1 0 * * *` UTC. Checks *yesterday's* data so GitHub's cron delays (often from 30–90 min up to several hours) don't matter — the data is always complete by then. No DST handling needed.

**Debug mode:** Set GitHub Actions Variable `NOTIFY_ALWAYS=true` to receive a notification even when LVV was on (prefixed with "OK (debug):"). Set back to `false` when done testing.
