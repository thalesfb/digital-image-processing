#!/usr/bin/env bash
# Shared validator: ASCII gitmoji shortcode + Conventional Commits + English subject.

set -euo pipefail

SUBJECT="${1:?usage: validate-subject.sh '<subject line>'}"
LABEL="${VALIDATE_SUBJECT_LABEL:-subject}"

ALLOWED_TYPES='feat|fix|security|config|docs|style|refactor|perf|test|build|ci|chore|revert|hotfix|raw|cleanup|remove|init'

ALLOWED_EMOJI_CODES=(
  ':sparkles:' ':bug:' ':ambulance:' ':lock:' ':memo:' ':recycle:' ':zap:'
  ':white_check_mark:' ':arrow_up:' ':wrench:' ':rocket:' ':gear:'
  ':globe_with_meridians:' ':broom:' ':bookmark_tabs:' ':fire:' ':books:'
  ':ok_hand:' ':package:' ':bricks:' ':card_file_box:' ':wastebasket:'
  ':lipstick:' ':closed_lock_with_key:' ':test_tube:' ':heavy_plus_sign:'
  ':heavy_minus_sign:' ':hammer:' ':truck:' ':tada:'
)

fail() {
  echo "${LABEL}: $1" >&2
  safe_subject="$SUBJECT"
  if LC_ALL=C printf '%s' "$SUBJECT" | grep -q '[^ -~]'; then
    safe_subject="<non-ASCII subject omitted>"
  fi
  echo "  subject: $safe_subject" >&2
  echo "  see docs/GIT_HOOKS.md" >&2
  exit 1
}

is_dependabot_subject() {
  [[ "$SUBJECT" =~ ^Bump\  ]] && return 0
  [[ "$SUBJECT" =~ ^:arrow_up:\ chore ]] && return 0
  [[ "$SUBJECT" =~ \(deps[a-zA-Z0-9_-]*\): ]] && return 0
  return 1
}

if is_dependabot_subject; then
  [[ ${#SUBJECT} -le 160 ]] || fail "dependabot subject must be at most 160 characters"
  exit 0
fi

if LC_ALL=C printf '%s' "$SUBJECT" | grep -q '[^ -~]'; then
  fail "must be ASCII-only - use :shortcode: gitmoji (never Unicode emoji in PowerShell)"
fi

EMOJI_TOKEN=""
rest="$SUBJECT"

if [[ "$rest" =~ ^:([a-z0-9_+-]+):[[:space:]]+(.*)$ ]]; then
  EMOJI_TOKEN=":${BASH_REMATCH[1]}:"
  rest="${BASH_REMATCH[2]}"
else
  fail "must start with :shortcode: gitmoji (e.g. :books: docs: ...)"
fi

type_re="^(${ALLOWED_TYPES})(\\([^)]+\\))?:[[:space:]]+(.+)$"
if ! [[ "$rest" =~ $type_re ]]; then
  fail "expected '<emoji> type[(scope)]: description' (Conventional Commits)"
fi

DESCRIPTION="${BASH_REMATCH[3]}"

ok=0
for code in "${ALLOWED_EMOJI_CODES[@]}"; do
  if [[ "$EMOJI_TOKEN" == "$code" ]]; then
    ok=1
    break
  fi
done
[[ "$ok" -eq 1 ]] || fail "gitmoji '${EMOJI_TOKEN}' is not in the allowlist"

[[ -n "$DESCRIPTION" ]] || fail "description must not be empty"
[[ ${#DESCRIPTION} -ge 4 ]] || fail "description too short (min 4 characters)"
[[ ! "$DESCRIPTION" =~ \.$ ]] || fail "remove trailing period from subject"
[[ ${#SUBJECT} -le 72 ]] || fail "must be at most 72 characters (current: ${#SUBJECT})"

PT_WORDS='corrigir|adicionar|remover|atualizar|implementar|ajuste|quando|durante|configuração|catalogo|usuario|erro|suíte'
if echo "$DESCRIPTION" | grep -Eiq "\b(${PT_WORDS})\b"; then
  fail "description must be English (Portuguese wording detected)"
fi

exit 0
