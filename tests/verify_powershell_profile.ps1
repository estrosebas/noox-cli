# Script para verificar la sintaxis del perfil de PowerShell generado por NooxCLI

# Configuracion de codificacion UTF-8 para caracteres especiales
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Configurar pagina de codigos UTF-8 si no esta configurada
if ((chcp) -notmatch "65001") {
    chcp 65001 > $null
}

Import-Module PSReadLine
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -Colors @{ InLinePrediction = 'DarkGray' }

# Agregar oh-my-posh al PATH
$env:PATH += ";$env:LOCALAPPDATA\Programs\oh-my-posh\bin"

# Agregar Scripts al PATH
$env:PATH += ";$env:USERPROFILE\Scripts"

# Aliases utiles
Set-Alias -Name dev -Value desarrollo.bat
Set-Alias -Name sys -Value sistema.bat
Set-Alias -Name proj -Value proyectos.bat
Set-Alias -Name config -Value config-consola.bat
Set-Alias -Name ll -Value Get-ChildItem

clear
$fecha = Get-Date -Format "yyyy-MM-dd"
$usuario = [System.Environment]::UserName
$pc = $env:COMPUTERNAME

Write-Host ""
Write-Host "╭─ $usuario@$pc ───────────────────────────────" -ForegroundColor Cyan
Write-Host "│ ¡Bienvenido, Sebas! Listo para codear 💻⚡         " -ForegroundColor Green
Write-Host "│ Fecha: $fecha                              " -ForegroundColor Yellow
Write-Host "├─ Alias disponibles:                              " -ForegroundColor Magenta
Write-Host "│ • dev    → Entorno de desarrollo                 " -ForegroundColor White
Write-Host "│ • sys    → Scripts del sistema                   " -ForegroundColor White
Write-Host "│ • proj   → Proyectos de Laragon                  " -ForegroundColor White
Write-Host "│ • config → Configuracion UTF-8/Consola          " -ForegroundColor White
Write-Host "│ • ll     → Lista detallada de archivos           " -ForegroundColor White
Write-Host "╰───────────────────────────────────────────────────────" -ForegroundColor Cyan
Write-Host ""

if (Test-Path .git) {
    $branch = git branch --show-current 2>$null
    if ($branch) {
        Write-Host "Git - Rama actual: $branch" -ForegroundColor DarkGray
    }
}

# Inicializar oh-my-posh
if (Get-Command oh-my-posh -ErrorAction SilentlyContinue) {
    oh-my-posh init pwsh --config "$env:LOCALAPPDATA\Programs\oh-my-posh\themes\avit.omp.json" | Invoke-Expression
} elseif (Test-Path "$env:LOCALAPPDATA\Programs\oh-my-posh\bin\oh-my-posh.exe") {
    & "$env:LOCALAPPDATA\Programs\oh-my-posh\bin\oh-my-posh.exe" init pwsh --config "$env:LOCALAPPDATA\Programs\oh-my-posh\themes\avit.omp.json" | Invoke-Expression
}

Write-Host "OK - Perfil cargado correctamente!" -ForegroundColor Green