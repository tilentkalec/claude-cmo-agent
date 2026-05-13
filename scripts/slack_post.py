#!/usr/bin/env python3
"""Post a message to Slack via an incoming webhook.

Used by all agents per .claude/rules/slack-notifications.md.
Direct REST call — no MCP dependency. On failure, appends to
data/slack_failed_messages.log and exits non-zero.

Usage:
    python3 scripts/slack_post.py --agent CMO --message "..."
    echo "..." | python3 scripts/slack_post.py --agent CMO --stdin

Env: SLACK_WEBHOOK_URL (required) — sourced from .env at repo root.
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.request
import urllib.error


REPO = pathlib.Path(__file__).resolve().parent.parent
LOG = REPO / "data" / "slack_failed_messages.log"


def load_env():
    """Minimal .env loader so we don't depend on python-dotenv."""
    env_path = REPO / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def post(message: str, agent: str) -> bool:
    """POST to Slack webhook. Returns True on 2xx, False otherwise."""
    url = os.environ.get("SLACK_WEBHOOK_URL")
    if not url:
        return False
    # Prefix every message with the agent name in bold per the rule.
    text = f"*[{agent}]* {message}" if agent else message
    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return 200 <= resp.status < 300
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return False


def log_failure(agent: str, message: str, reason: str):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with LOG.open("a") as f:
        f.write(f"{ts} | {agent} | {reason} | {message}\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--agent", required=True, help="Agent name, e.g. 'CMO', 'Email'")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--message", help="Message body (without [Agent] prefix)")
    g.add_argument("--stdin", action="store_true", help="Read message from stdin")
    args = p.parse_args()

    load_env()
    message = sys.stdin.read().strip() if args.stdin else args.message
    if not message:
        print("empty message; nothing to post", file=sys.stderr)
        return 2

    if post(message, args.agent):
        return 0

    reason = "no SLACK_WEBHOOK_URL" if not os.environ.get("SLACK_WEBHOOK_URL") else "webhook post failed"
    log_failure(args.agent, message, reason)
    print(f"slack post failed ({reason}); logged to {LOG}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
