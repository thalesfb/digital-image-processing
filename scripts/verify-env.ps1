# Verifica ambiente Python + kernel Jupyter
# Uso (com .venv ativo): . .\scripts\activate.ps1; .\scripts\verify-env.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"

Write-Host "[INFO] Verificando ambiente em $Root"

if (-not $env:VIRTUAL_ENV) {
    Write-Host "[AVISO] .venv NAO esta ativo nesta sessao." -ForegroundColor Yellow
    Write-Host "        Ative com: . .\scripts\activate.ps1" -ForegroundColor Yellow
} elseif ($env:VIRTUAL_ENV -ne (Resolve-Path (Join-Path $Root ".venv")).Path) {
    Write-Host "[AVISO] Outro venv ativo: $env:VIRTUAL_ENV" -ForegroundColor Yellow
    Write-Host "        Este projeto exige: $Root\.venv" -ForegroundColor Yellow
} else {
    Write-Host "[OK] .venv ativo nesta sessao"
}

if (-not (Test-Path $Python)) {
    Write-Host "[ERRO] .venv nao encontrado. Execute: .\scripts\setup.ps1" -ForegroundColor Red
    exit 1
}

& $Python -c @"
import sys
mods = ['cv2', 'numpy', 'matplotlib', 'PIL', 'ipykernel']
missing = []
for m in mods:
    try:
        __import__(m)
    except ImportError:
        missing.append(m)
if missing:
    print('[ERRO] Modulos faltando:', ', '.join(missing))
    sys.exit(1)
import cv2, numpy as np
print('[OK] Python', sys.version.split()[0])
print('[OK] opencv', cv2.__version__, '| numpy', np.__version__)
"@

if ($LASTEXITCODE -ne 0) { exit 1 }

$kernel = jupyter kernelspec list 2>$null | Select-String "pd-images"
if ($kernel) {
    Write-Host "[OK] Kernel Jupyter: pd-images"
} else {
    Write-Host "[AVISO] Kernel pd-images nao registrado. Execute setup.ps1 novamente." -ForegroundColor Yellow
}

Write-Host "[OK] Ambiente pronto para executar os notebooks."
