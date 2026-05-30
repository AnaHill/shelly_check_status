# Project context for Claude Code

## What this project does

Daily check: did the Shelly smart relay named **LVV** turn on today?
If not → send a push notification via ntfy.sh.
Runs every day at **21:15 Helsinki local time** via GitHub Actions.

## Key files

| File | Purpose |
|------|---------|
| `check_lvv.py` | Main script: fetches data, checks LVV, sends notification |
| `get_data_from_shelly_api.py` | Fetches relay history from the SmartMonitoring API |
| `.github/workflows/check_lvv.yml` | GitHub Actions cron job |
| `.env.example` | Template for local API key (copy to `.env`) |

## Data source

API: `https://api.spot-hinta.fi/SmartMonitoring?PrivateKey=...`

Returns hourly relay records. Each row = one hour, with fields:
- `relenimi` — relay name (we filter for `"LVV"`)
- `relestatus` — bool, was the relay on during that hour
- `pvm` — timestamp (UTC)

## Important design decisions

**DST handling:** GitHub Actions cron is always UTC, so two cron entries are used:
- `15 18 * * *` UTC = 21:15 EEST (summer, UTC+3)
- `15 19 * * *` UTC = 21:15 EET (winter, UTC+2)

The script guards with `datetime.now(Helsinki).hour == 21` and silently skips the run that lands at the wrong hour.

**Notifications:** [ntfy.sh](https://ntfy.sh) — free, no account needed to publish. Install the ntfy phone app and subscribe to your topic.

**Debug mode:** GitHub Actions Variable `NOTIFY_ALWAYS=true` makes the script send a notification even when LVV was on (prefixed with "OK (debug):"). Set it back to `false` when done testing.

## GitHub Actions setup needed

In the repo: **Settings → Secrets and variables → Actions**

| Type | Name | Notes |
|------|------|-------|
| Secret | `SMART_MONITORING_KEY` | SmartMonitoring API key |
| Secret | `NTFY_TOPIC` | ntfy.sh topic name |
| Variable | `NOTIFY_ALWAYS` | Set `false` normally, `true` for testing |

## Local development

```bash
cp .env.example .env   # add your API key
pip install -r requirements.txt
python check_lvv.py    # note: skips if local time is not 21:xx Helsinki
```
