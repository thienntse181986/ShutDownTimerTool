# PowerShell build script for Shutdown Timer
# Usage: In PowerShell (with venv activated): .\build.ps1

param(
    [switch]$onefile = $true,
    [switch]$noconsole = $true
)

# Ensure icon exists
if (-not (Test-Path .\shutdown_icon.png)) {
    Write-Host "shutdown_icon.png not found, generating..."
    & python .\make_icon.py
}

$icon = (Resolve-Path .\shutdown_icon.png).Path

# Find python in venv if available
$venvPython = Join-Path (Get-Location) ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonExe = (Resolve-Path $venvPython).Path
} else {
    $pythonExe = "python"
}

$pyArgs = @()
if ($onefile) { $pyArgs += '--onefile' }
if ($noconsole) { $pyArgs += '--noconsole' }
$pyArgs += "--icon=$icon"
$pyArgs += '--name=ShutdownTimer'
$pyArgs += 'main.py'

Write-Host "Running: $pythonExe -m PyInstaller $($pyArgs -join ' ')"
& $pythonExe -m PyInstaller @pyArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build succeeded. Output in dist\ShutdownTimer.exe"
} else {
    Write-Host "Build failed with exit code $LASTEXITCODE"
}
