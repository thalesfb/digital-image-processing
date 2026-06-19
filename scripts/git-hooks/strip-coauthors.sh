#!/usr/bin/env bash
# Remove AI tool co-authorship trailers (Cursor, Copilot, Claude, etc.).

set -euo pipefail

MSG_FILE="${1:?usage: strip-coauthors.sh <commit-msg-file>}"
[[ -f "$MSG_FILE" ]] || exit 0

TMP="${MSG_FILE}.no-coauthor"
grep -viE '^Co-authored-by:[[:space:]]*(Cursor|Composer|Copilot|Claude|GitHub Copilot)([[:space:]]|<|$)' "$MSG_FILE" \
  | grep -viE 'cursoragent@cursor\.com' >"$TMP" || true
mv "$TMP" "$MSG_FILE"
