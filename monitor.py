"""
Uptime Monitor — checks a list of URLs on a schedule, logs their status
and response time, and prints an alert when something's down or slow.

This is a tiny version of what real monitoring systems (like Prometheus
Alertmanager, PagerDuty, or Datadog) do: check a signal, compare it
against a threshold, and notify when the threshold is crossed.

Usage:
    python monitor.py
"""

import time
import csv
import os
from datetime import datetime

import requests
from config import TARGETS, CHECK_INTERVAL_SECONDS, LATENCY_ALERT_THRESHOLD_MS, LOG_FILE


def check_url(url: str) -> dict:
    """Ping one URL and return what happened."""
    start = time.time()
    try:
        response = requests.get(url, timeout=5)
        latency_ms = (time.time() - start) * 1000
        return {
            "url": url,
            "status_code": response.status_code,
            "up": response.status_code < 400,
            "latency_ms": round(latency_ms, 1),
            "error": None,
        }
    except requests.RequestException as e:
        latency_ms = (time.time() - start) * 1000
        return {
            "url": url,
            "status_code": None,
            "up": False,
            "latency_ms": round(latency_ms, 1),
            "error": str(e),
        }


def log_result(result: dict):
    """Append one check result to a CSV file, so you have a history to look back on."""
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "url", "status_code", "up", "latency_ms", "error"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"timestamp": datetime.utcnow().isoformat(), **result})


def alert(message: str):
    """
    This is a stand-in for a real alert (Slack, PagerDuty, email).
    In production, this function is where you'd call a webhook instead of printing.
    """
    print(f"🚨 ALERT: {message}")


def run_check_cycle():
    for url in TARGETS:
        result = check_url(url)
        log_result(result)

        if not result["up"]:
            alert(f"{url} is DOWN (status={result['status_code']}, error={result['error']})")
        elif result["latency_ms"] > LATENCY_ALERT_THRESHOLD_MS:
            alert(f"{url} is SLOW ({result['latency_ms']}ms, threshold is {LATENCY_ALERT_THRESHOLD_MS}ms)")
        else:
            print(f"✅ {url} is healthy ({result['latency_ms']}ms)")


if __name__ == "__main__":
    print(f"Starting uptime monitor. Checking {len(TARGETS)} targets every {CHECK_INTERVAL_SECONDS}s.")
    print(f"Logging results to {LOG_FILE}. Press Ctrl+C to stop.\n")
    try:
        while True:
            run_check_cycle()
            print("-" * 40)
            time.sleep(CHECK_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nStopped.")