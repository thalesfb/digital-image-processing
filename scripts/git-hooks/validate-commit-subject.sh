#!/usr/bin/env bash
set -euo pipefail

SUBJECT="${1:?usage: validate-commit-subject.sh '<subject line>'}"
LABEL="${VALIDATE_SUBJECT_LABEL:-commit subject}"

if LC_ALL=C printf '%s' "$SUBJECT" | grep -q '[^ -~]'; then
  echo "${LABEL}: must be ASCII-only" >&2
  echo "  use :shortcode: from docs/GIT_HOOKS.md (e.g. :books: :sparkles:)" >&2
  exit 1
fi

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export VALIDATE_SUBJECT_LABEL="$LABEL"
exec bash "$HOOK_DIR/validate-subject.sh" "$SUBJECT"
