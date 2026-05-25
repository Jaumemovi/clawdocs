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

SYSTEM_CA="/etc/ssl/certs/ca-certificates.crt"

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "GOOGLE_APPLICATION_CREDENTIALS=$SA_PATH" >> "$CLAUDE_ENV_FILE"
  # gRPC ignora SSL_CERT_FILE/REQUESTS_CA_BUNDLE; necessita el seu propi var
  # perquè la CA del proxy d'egress de Claude Cloud sigui acceptada
  # (afecta google-ads, qualsevol client basat en gRPC).
  echo "GRPC_DEFAULT_SSL_ROOTS_FILE_PATH=$SYSTEM_CA" >> "$CLAUDE_ENV_FILE"
else
  export GOOGLE_APPLICATION_CREDENTIALS="$SA_PATH"
  export GRPC_DEFAULT_SSL_ROOTS_FILE_PATH="$SYSTEM_CA"
fi

if ! python3 -c "import cryptography" 2>/dev/null || ! python3 -c "from cryptography.hazmat.bindings._rust import exceptions" 2>/dev/null; then
  pip install --quiet --ignore-installed cryptography cffi >&2 || true
fi

if ! python3 -c "import gspread, google.auth" 2>/dev/null; then
  pip install --quiet --disable-pip-version-check gspread google-auth >&2 || {
    echo "[session-start] pip install failed (gspread/google-auth)" >&2
    exit 0
  }
fi

if [ -n "${GOOGLE_ADS_DEVELOPER_TOKEN:-}" ] && ! python3 -c "import google.ads.googleads" 2>/dev/null; then
  pip install --quiet --disable-pip-version-check google-ads >&2 || {
    echo "[session-start] pip install failed (google-ads)" >&2
  }
fi

echo "[session-start] SA credentials ready at $SA_PATH" >&2
