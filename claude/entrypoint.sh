#!/bin/sh
# Retry with a delay instead of letting Docker restart in a tight loop
# (e.g. before the first login or while Remote Control is unavailable).
while true; do
    claude remote-control "$@"
    echo "claude remote-control exited with code $?, retrying in 60s"
    sleep 60
done
