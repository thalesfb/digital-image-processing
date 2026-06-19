# Ativa o ambiente virtual nesta sessão do PowerShell.
# Uso: . .\scripts\activate.ps1   (note o ponto e espaço no início)

$Root = Split-Path -Parent $PSScriptRoot
$Activate = Join-Path $Root ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $Activate)) {
    Write-Error "[ERRO] .venv nao encontrado. Execute primeiro: .\scripts\setup.ps1"
}

. $Activate
Write-Host "[OK] Ambiente virtual ativo (.venv)" -ForegroundColor Green
Write-Host "  python: $(Get-Command python | Select-Object -ExpandProperty Source)"
Write-Host "  Use o kernel PDI (.venv) nos notebooks."
