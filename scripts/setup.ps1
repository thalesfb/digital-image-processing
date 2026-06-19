# Setup do ambiente virtual - Windows PowerShell
# Executar na raiz do repositorio: .\scripts\setup.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "[INFO] Criando ambiente virtual em .venv ..."
python -m venv .venv

Write-Host "[INFO] Instalando dependencias ..."
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\pip.exe install -r requirements.txt

Write-Host "[INFO] Registrando kernel Jupyter ..."
& .\.venv\Scripts\python.exe -m ipykernel install --user --name=pd-images --display-name="PDI (.venv)"

Write-Host "[INFO] Instalando git hooks ..."
& (Join-Path $Root "scripts\git-hooks\install.ps1")

if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "[INFO] Instalando commitlint (npm) ..."
    npm install --no-fund --no-audit
} else {
    Write-Host "[AVISO] npm nao encontrado - commitlint usara npx no hook"
}

Write-Host "[OK] Ambiente pronto."
Write-Host ""
Write-Host "  SEMPRE antes de trabalhar:" -ForegroundColor Cyan
Write-Host "    . .\scripts\activate.ps1"
Write-Host "    .\scripts\verify-env.ps1"
Write-Host ""
Write-Host "  Notebook: experiment\Aula 2\notebook.ipynb (kernel PDI (.venv))"
Write-Host "  Guia: docs\EXECUTION.md"
