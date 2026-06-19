#!/usr/bin/env bash
# Setup do ambiente virtual — Linux / macOS
# Executar na raiz do repositório: bash scripts/setup.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "[INFO] Criando ambiente virtual em .venv ..."
python3 -m venv .venv

echo "[INFO] Instalando dependencias ..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

echo "[INFO] Registrando kernel Jupyter ..."
.venv/bin/python -m ipykernel install --user --name=pd-images --display-name="PDI (.venv)"

if command -v npm >/dev/null 2>&1; then
  echo "[INFO] Instalando commitlint e git hooks ..."
  npm install --no-fund --no-audit
  bash scripts/git-hooks/install.sh
else
  echo "[AVISO] npm nao encontrado — hooks de commit opcionais (ver docs/GIT_HOOKS.md)"
fi

echo "[OK] Ambiente pronto."
echo ""
echo "  SEMPRE antes de trabalhar:"
echo "    source .venv/bin/activate"
echo "    python -c \"import sys; assert '.venv' in sys.executable\""
echo ""
echo "  Notebook: experiment/Aula 2/notebook.ipynb (kernel PDI (.venv))"
echo "  Guia: docs/EXECUTION.md"
