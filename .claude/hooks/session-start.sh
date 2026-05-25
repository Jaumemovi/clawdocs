#!/usr/bin/env bash
# SessionStart hook for Clawdocs
# Materializes the Google Cloud Service Account credentials from the
# GOOGLE_SA_JSON env var so Sheets/Drive tooling works in Claude Cloud sessions.

set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-false}" != "true" ]; then
  exit 0
fi

if [ -z "${GOOGLE_SA_JSON:-}" ]; then
  echo "[session-start] GOOGLE_SA_JSON not set; skipping SA setup" >&2
  exit 0
fi

SA_PATH="/root/.secrets/claude-cloud-sa.json"
mkdir -p "$(dirname "$SA_PATH")"
chmod 700 "$(dirname "$SA_PATH")"

printf '%s' "$GOOGLE_SA_JSON" > "$SA_PATH"
chmod 600 "$SA_PATH"

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "GOOGLE_APPLICATION_CREDENTIALS=$SA_PATH" >> "$CLAUDE_ENV_FILE"
else
  export GOOGLE_APPLICATION_CREDENTIALS="$SA_PATH"
fi

if ! python3 -c "import gspread, google.auth" 2>/dev/null; then
  pip install --quiet --disable-pip-version-check gspread google-auth >&2 || {
    echo "[session-start] pip install failed" >&2
    exit 0
  }
fi

echo "[session-start] SA credentials ready at $SA_PATH" >&2
