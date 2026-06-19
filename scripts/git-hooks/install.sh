#!/usr/bin/env bash
# Install git hooks into this repository (idempotent).
# Usage: bash scripts/git-hooks/install.sh [REPO_ROOT]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="${1:-$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || pwd)}"

if ! git -C "$REPO_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  echo "ERROR: not a git repository: $REPO_ROOT" >&2
  exit 1
fi

mkdir -p "$REPO_ROOT/.githooks/lib"
cp "$SCRIPT_DIR/strip-coauthors.sh" "$REPO_ROOT/.githooks/lib/"
cp "$SCRIPT_DIR/validate-subject.sh" "$REPO_ROOT/.githooks/lib/"
cp "$SCRIPT_DIR/validate-commit-subject.sh" "$REPO_ROOT/.githooks/lib/"
cp "$SCRIPT_DIR/commit-msg" "$REPO_ROOT/.githooks/"
cp "$SCRIPT_DIR/prepare-commit-msg" "$REPO_ROOT/.githooks/"
chmod +x "$REPO_ROOT/.githooks/commit-msg" \
  "$REPO_ROOT/.githooks/prepare-commit-msg" \
  "$REPO_ROOT/.githooks/lib/"*.sh

git -C "$REPO_ROOT" config core.hooksPath .githooks
echo "OK: hooks installed in $REPO_ROOT (core.hooksPath=.githooks)"
echo "TIP: run 'npm install' for fast local commitlint (npx fallback works without it)"
