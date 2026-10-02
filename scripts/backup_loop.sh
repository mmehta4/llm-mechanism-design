#!/bin/sh
# Every 3 hours: copy the project (minus the Python setup, secrets and caches) to a
# folder iCloud never touches, commit any change, and push it to the PRIVATE GitHub
# repository github.com/mmehta4/llm-mechanism-design, branch snapshot-2026-10-02.
#
# Why a separate copy: iCloud offloaded the project's own git history on 2026-10-01,
# so the main repository could not be pushed. This keeps every result backed up
# regardless. Started by experiments/launch_stage2.py; safe to start twice (it exits
# if another copy is already running). Log: results/logs/backup.log
SRC="$(cd "$(dirname "$0")/.." && pwd)"
SNAP="$HOME/llm-mechanism-design-snapshot"
LOCK="$SNAP/.backup-loop.pid"
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK")" 2>/dev/null; then exit 0; fi
echo $$ > "$LOCK"
while true; do
  rsync -a --delete --exclude venv --exclude venv.nosync --exclude 'venv 2' --exclude .git \
        --exclude __pycache__ --exclude .env --exclude .pytest_cache \
        --exclude .gitignore --exclude .backup-loop.pid "$SRC/" "$SNAP/" 2>/dev/null
  cd "$SNAP" || exit 1
  # never back up a key, even by accident
  if grep -rIqE "gsk_[A-Za-z0-9]{20,}|nvapi-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,}|AQ\.[A-Za-z0-9_-]{30,}|sk-ant-[A-Za-z0-9_-]{20,}" --exclude-dir=.git .; then
    echo "$(date '+%F %T') STOPPED: something that looks like an API key is in the project" >> "$SRC/results/logs/backup.log"
  else
    git add -A >/dev/null 2>&1
    if ! git diff --cached --quiet; then
      git commit -q -m "Automatic backup $(date '+%F %H:%M')" && \
      git push -q origin snapshot-2026-10-02 >/dev/null 2>&1 && \
      echo "$(date '+%F %T') backed up" >> "$SRC/results/logs/backup.log" || \
      echo "$(date '+%F %T') push failed, will retry" >> "$SRC/results/logs/backup.log"
    fi
  fi
  # the main repository too, now that iCloud keeps it local ("Keep Downloaded"): new
  # results go into the real history on branch main
  cd "$SRC" && git add results/raw results/analysis >/dev/null 2>&1
  if ! git diff --cached --quiet 2>/dev/null; then
    git commit -q -m "Automatic backup: results $(date '+%F %H:%M')" && \
    git push -q origin main >/dev/null 2>&1 && \
    echo "$(date '+%F %T') results pushed to main" >> "$SRC/results/logs/backup.log"
  fi
  sleep 10800
done
