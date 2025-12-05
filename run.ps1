# Script de lancement pour Logger NI
# Windows PowerShell

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Logger NI - Lancement de l'application" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Naviguer vers le dossier du script
Set-Location $PSScriptRoot

# Vérifier si l'environnement virtuel existe
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Erreur: Environnement virtuel non trouve" -ForegroundColor Red
    Write-Host "Veuillez d'abord executer l'installation" -ForegroundColor Yellow
    pause
    exit 1
}

# Lancer l'application avec l'environnement virtuel
Write-Host "Demarrage de l'application..." -ForegroundColor Green
Write-Host ""

& ".\.venv\Scripts\python.exe" main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "Une erreur s'est produite" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    pause
}
