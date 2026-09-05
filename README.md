# Uptime Monitor

A small script that checks a list of websites on a schedule, times each
response, and prints an alert when a site is down or too slow. Built to
practice the core idea behind SRE monitoring: define a signal, define a
threshold, and get notified when reality crosses it.

## Run it

```bash
pip install -r requirements.txt
python monitor.py
```

You'll see output like:

```
✅ https://www.google.com is healthy (142.3ms)
✅ https://www.github.com is healthy (210.1ms)
🚨 ALERT: https://httpstat.us/500 is DOWN (status=500, error=None)
```

Every check is also appended to `uptime_log.csv`, so you have a history
to look back on.

## How it maps to real monitoring systems

| This project | Real-world equivalent |
|---|---|
| `check_url()` | A health check / synthetic probe |
| `LATENCY_ALERT_THRESHOLD_MS` | An alerting rule's threshold |
| `alert()` | PagerDuty, Slack webhook, email |
| `uptime_log.csv` | Time-series data in Prometheus/Datadog |

## Ideas to extend it (optional)

- Add a `/status` Flask endpoint that shows the latest results as JSON.
- Send real Slack alerts using a webhook URL instead of printing.
- Track consecutive failures and only alert after 3 in a row (avoids noise from one-off blips).
