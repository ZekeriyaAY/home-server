#!/usr/bin/env python3
"""SIGTERM idle Claude session processes so the bridge frees their capacity slot.

Sessions stay on the server (viewable, resumed when a message arrives).
Usage: idle-reaper.py [--max-idle-hours 12] [--dry-run]
"""
import argparse
import glob
import json
import os
import signal
import time

SESSIONS_DIR = os.path.expanduser("~/.claude/sessions")

ap = argparse.ArgumentParser()
ap.add_argument("--max-idle-hours", type=float, default=12)
ap.add_argument("--dry-run", action="store_true")
args = ap.parse_args()

now = time.time() * 1000
for path in sorted(glob.glob(f"{SESSIONS_DIR}/*.json")):
    try:
        s = json.load(open(path))
        pid = s["pid"]
        with open(f"/proc/{pid}/stat") as f:
            start = f.read().rsplit(")", 1)[1].split()[19]
        with open(f"/proc/{pid}/cmdline") as f:
            cmd = f.read()
    except (OSError, ValueError, KeyError, IndexError):
        continue
    # pid may have been reused: require same start time and a bridge-spawned session
    if start != str(s.get("procStart")) or "--sdk-url" not in cmd:
        continue
    idle_h = (now - s["statusUpdatedAt"]) / 3.6e6
    if s["status"] != "idle" or idle_h < args.max_idle_hours:
        continue
    print(f"{'would stop' if args.dry_run else 'stop'} pid={pid} {s['bridgeSessionId']} idle={idle_h:.1f}h")
    if not args.dry_run:
        os.kill(pid, signal.SIGTERM)
