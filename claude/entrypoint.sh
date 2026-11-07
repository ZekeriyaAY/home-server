#!/bin/sh
# Free capacity slots held by idle sessions; they resume when a message arrives.
# A loop instead of cron: cron needs root and the container runs as claude.
(while true; do sleep 3600; idle-reaper.py --max-idle-hours 24; done) &

# Retry with a delay instead of letting Docker restart in a tight loop
# (e.g. before the first login or while Remote Control is unavailable).
while true; do
    claude remote-control "$@"
    echo "claude remote-control exited with code $?, retrying in 60s"
    sleep 60
done
