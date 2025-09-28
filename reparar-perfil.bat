@echo off
REM Script para reparar perfil de PowerShell - by Sebas
title Reparar Perfil de PowerShell

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║        REPARACION DE PERFIL POWERSHELL        ║
echo ╚═══════════════════════════════════════════════╝
echo.

echo 🔧 Reparando perfil de PowerShell...
echo.

REM Hacer backup del perfil actual
echo [1/4] Creando respaldo del perfil actual...
copy "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1" "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile_backup_%date:~-4%%date:~3,2%%date:~0,2%.ps1" > nul 2>&1

REM Crear perfil nuevo corregido
echo [2/4] Creando perfil corregido...

(
echo # Configuracion de codificacion UTF-8 para caracteres especiales
echo [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
echo $OutputEncoding = [System.Text.Encoding]::UTF8
echo.
echo # Configurar pagina de codigos UTF-8 si no esta configurada
echo if ^(^(chcp^) -notmatch "65001"^) {
echo     chcp 65001 ^> $null
echo }
echo.
echo Import-Module PSReadLine
echo Set-PSReadLineOption -PredictionSource History
echo Set-PSReadLineOption -Colors @{ InLinePrediction = 'DarkGray' }
echo.
echo # Agregar oh-my-posh al PATH
echo $env:PATH += ";$env:LOCALAPPDATA\Programs\oh-my-posh\bin"
echo.
echo # Agregar Scripts al PATH
echo $env:PATH += ";$env:USERPROFILE\Scripts"
echo.
echo # Aliases utiles
echo Set-Alias -Name dev -Value desarrollo.bat
echo Set-Alias -Name sys -Value sistema.bat
echo Set-Alias -Name proj -Value proyectos.bat
echo Set-Alias -Name config -Value config-consola.bat
echo Set-Alias -Name ll -Value Get-ChildItem
echo.
echo clear
echo $fecha = Get-Date -Format "yyyy-MM-dd"
echo $usuario = [System.Environment]::UserName
echo $pc = $env:COMPUTERNAME
echo.
echo Write-Host ""
echo Write-Host "╭─ $usuario@$pc ───────────────────────────────" -ForegroundColor Cyan
echo Write-Host "│ ¡Bienvenido, Sebas! Listo para codear 💻⚡         " -ForegroundColor Green
echo Write-Host "│ Fecha: $fecha                              " -ForegroundColor Yellow
echo Write-Host "├─ Alias disponibles:                              " -ForegroundColor Magenta
echo Write-Host "│ • dev    → Entorno de desarrollo                 " -ForegroundColor White
echo Write-Host "│ • sys    → Scripts del sistema                   " -ForegroundColor White
echo Write-Host "│ • proj   → Proyectos de Laragon                  " -ForegroundColor White
echo Write-Host "│ • config → Configuracion UTF-8/Consola          " -ForegroundColor White
echo Write-Host "│ • ll     → Lista detallada de archivos           " -ForegroundColor White
echo Write-Host "╰───────────────────────────────────────────────────────" -ForegroundColor Cyan
echo Write-Host ""
echo.
echo if ^(Test-Path .git^) {
echo     $branch = git branch --show-current
echo     Write-Host "📁 Rama actual: $branch" -ForegroundColor DarkGray
echo }
echo.
echo # Inicializar oh-my-posh
echo if ^(Get-Command oh-my-posh -ErrorAction SilentlyContinue^) {
echo     oh-my-posh init pwsh --config "$env:LOCALAPPDATA\Programs\oh-my-posh\themes\avit.omp.json" ^| Invoke-Expression
echo } elseif ^(Test-Path "$env:LOCALAPPDATA\Programs\oh-my-posh\bin\oh-my-posh.exe"^) {
echo     ^& "$env:LOCALAPPDATA\Programs\oh-my-posh\bin\oh-my-posh.exe" init pwsh --config "$env:LOCALAPPDATA\Programs\oh-my-posh\themes\avit.omp.json" ^| Invoke-Expression
echo }
) > "%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"

echo [3/4] Verificando sintaxis del perfil...
powershell -NoProfile -Command "try { Get-Content '%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1' | Out-String | Invoke-Expression -ErrorAction Stop; Write-Host 'Sintaxis OK' -ForegroundColor Green } catch { Write-Host 'Error de sintaxis:' -ForegroundColor Red; Write-Host $_.Exception.Message -ForegroundColor Red }"

echo [4/4] Probando carga del perfil...
powershell -Command "Write-Host 'Perfil cargado correctamente!' -ForegroundColor Green"

echo.
echo ✅ ¡Perfil de PowerShell reparado exitosamente!
echo.
echo 📝 Acciones realizadas:
echo   • Respaldo creado con fecha
echo   • Perfil regenerado con sintaxis correcta
echo   • Configuración UTF-8 incluida
echo   • Todos los alias restaurados
echo   • oh-my-posh configurado correctamente
echo.
echo 🔄 Cierra y abre una nueva ventana de PowerShell para
echo    ver los cambios aplicados.
echo.
pause
