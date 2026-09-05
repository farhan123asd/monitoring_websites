"""
Configuration for uptime monitor.
"""

TARGETS = [
    "https://www.google.com",
    "https://www.github.com",
    "https://httpstat.us/500",   # this one always fails — proves alerting works
]

CHECK_INTERVAL_SECONDS = 10
LATENCY_ALERT_THRESHOLD_MS = 1000  # alert if a site takes longer than this
LOG_FILE = "uptime_log.csv"
