# Shelly LVV status check

Checks daily whether a Shelly smart relay (LVV) was on the previous day, and sends a push notification if it wasn't.

Runs automatically every morning at **6:00 UTC (8–9 AM Helsinki)** via GitHub Actions, checking yesterday's data. Notifications are delivered via [ntfy.sh](https://ntfy.sh) — free, no account needed.

## How it works

1. GitHub Actions fetches relay data from the [SmartMonitoring API](https://spot-hinta.fi)
2. Checks if the LVV relay was active at any point yesterday (Helsinki timezone)
3. If not → sends a push notification: `LVV not on yesterday!`

## Setup

### 1. Clone

```bash
git clone <your-repo-url>
```

### 2. Set up push notifications (ntfy.sh)

- Install the **ntfy** app on your phone ([iOS](https://apps.apple.com/app/ntfy/id1625396347) / [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy))
- Choose a unique topic name, e.g. `lvv-check-yourname`
- Subscribe to that topic in the app

### 3. Add GitHub Actions secrets and variables

In your repo: **Settings → Secrets and variables → Actions**

| Type | Name | Value |
|------|------|-------|
| Secret | `SMART_MONITORING_KEY` | Your SmartMonitoring API key |
| Secret | `NTFY_TOPIC` | Your ntfy topic name |
| Variable | `NOTIFY_ALWAYS` | `false` (set to `true` to test notifications even when LVV was on) |

### 4. Push to GitHub

Once the repo is pushed, GitHub Actions will run automatically every morning. You can also trigger it manually via **Actions → Check LVV daily → Run workflow**.

## Configuration

| Environment variable | Default | Description |
|----------------------|---------|-------------|
| `SMART_MONITORING_KEY` | *(required)* | SmartMonitoring API key |
| `NTFY_TOPIC` | *(required)* | ntfy.sh topic to send notifications to |
| `RELAY_NAME` | `LVV` | Relay name to check (as it appears in the API) |
| `NOTIFY_ALWAYS` | `false` | Set to `true` to always send a notification (for testing) |
