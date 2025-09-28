@echo off
REM Configurar consola para UTF-8 - by Sebas
title Configuracion de Consola UTF-8

echo.
echo ╔════════════════════════════════════════════╗
echo ║        CONFIGURACION DE CONSOLA UTF-8      ║
echo ╚════════════════════════════════════════════╝
echo.
echo Este script configurará tu consola para mostrar
echo correctamente los caracteres especiales y UTF-8.
echo.
echo [1] Aplicar configuración completa (recomendado)
echo [2] Solo cambiar página de códigos a UTF-8
echo [3] Configurar fuente de consola
echo [4] Restaurar configuración predeterminada
echo [5] Ver configuración actual
echo [0] Salir
echo.
set /p opcion="Selecciona una opción: "

if "%opcion%"=="1" goto completa
if "%opcion%"=="2" goto utf8only
if "%opcion%"=="3" goto fuente
if "%opcion%"=="4" goto restaurar
if "%opcion%"=="5" goto ver
if "%opcion%"=="0" goto salir
goto menu

:completa
echo.
echo ⚙️ Aplicando configuración completa...
echo.

REM Cambiar a página de códigos UTF-8
echo [1/4] Configurando página de códigos UTF-8...
chcp 65001 > nul

REM Configurar fuente para mejor soporte UTF-8
echo [2/4] Configurando fuente de consola...
powershell -Command "Set-ItemProperty -Path 'HKCU:\Console' -Name 'FontFamily' -Value 54"
powershell -Command "Set-ItemProperty -Path 'HKCU:\Console' -Name 'FontSize' -Value 1048576"
powershell -Command "Set-ItemProperty -Path 'HKCU:\Console' -Name 'FontWeight' -Value 400"

REM Configurar opciones adicionales
echo [3/4] Configurando opciones adicionales...
powershell -Command "Set-ItemProperty -Path 'HKCU:\Console' -Name 'CodePage' -Value 65001"
powershell -Command "Set-ItemProperty -Path 'HKCU:\Console' -Name 'CurrentCodePage' -Value 65001"

REM Configurar PowerShell específicamente
echo [4/4] Configurando PowerShell...
powershell -Command "$OutputEncoding = [System.Text.Encoding]::UTF8"
powershell -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8"

echo.
echo ✅ ¡Configuración completa aplicada!
echo.
echo 📝 Cambios aplicados:
echo   • Página de códigos: UTF-8 (65001)
echo   • Fuente: Consolas/Cascadia Code
echo   • Codificación de salida: UTF-8
echo.
echo ⚠️  IMPORTANTE: Cierra y abre una nueva consola para que
echo    todos los cambios surtan efecto.
echo.
pause
goto menu

:utf8only
echo.
echo ⚙️ Cambiando solo la página de códigos...
chcp 65001
powershell -Command "$OutputEncoding = [System.Text.Encoding]::UTF8"
echo.
echo ✅ Página de códigos cambiada a UTF-8
pause
goto menu

:fuente
echo.
echo ⚙️ Configurando fuente de consola...
echo.
echo Fuentes recomendadas para UTF-8:
echo [1] Cascadia Code (recomendada)
echo [2] Consolas
echo [3] Cascadia Mono
echo [4] JetBrains Mono
echo.
set /p fuente="Selecciona fuente (1-4): "

if "%fuente%"=="1" (
    powershell -Command "Set-ItemProperty -Path 'HKCU:\Console' -Name 'FaceName' -Value 'Cascadia Code'"
    echo ✅ Fuente configurada: Cascadia Code
)
if "%fuente%"=="2" (
    powershell -Command "Set-ItemProperty -Path 'HKCU:\Console' -Name 'FaceName' -Value 'Consolas'"
    echo ✅ Fuente configurada: Consolas
)
if "%fuente%"=="3" (
    powershell -Command "Set-ItemProperty -Path 'HKCU:\Console' -Name 'FaceName' -Value 'Cascadia Mono'"
    echo ✅ Fuente configurada: Cascadia Mono
)
if "%fuente%"=="4" (
    powershell -Command "Set-ItemProperty -Path 'HKCU:\Console' -Name 'FaceName' -Value 'JetBrains Mono'"
    echo ✅ Fuente configurada: JetBrains Mono
)

echo.
echo ⚠️ Cierra y abre una nueva consola para ver los cambios.
pause
goto menu

:restaurar
echo.
echo ⚙️ Restaurando configuración predeterminada...
powershell -Command "Remove-ItemProperty -Path 'HKCU:\Console' -Name 'CodePage' -ErrorAction SilentlyContinue"
powershell -Command "Remove-ItemProperty -Path 'HKCU:\Console' -Name 'FontFamily' -ErrorAction SilentlyContinue"
powershell -Command "Remove-ItemProperty -Path 'HKCU:\Console' -Name 'FontSize' -ErrorAction SilentlyContinue"
powershell -Command "Remove-ItemProperty -Path 'HKCU:\Console' -Name 'FaceName' -ErrorAction SilentlyContinue"
chcp 850 > nul
echo ✅ Configuración restaurada
pause
goto menu

:ver
echo.
echo 📊 CONFIGURACIÓN ACTUAL:
echo ========================
echo.
echo Página de códigos activa:
chcp
echo.
echo Configuración del registro:
powershell -Command "Get-ItemProperty -Path 'HKCU:\Console' | Format-List CodePage, FontFamily, FontSize, FontWeight, FaceName"
echo.
echo Codificación de PowerShell:
powershell -Command "Write-Host 'OutputEncoding:' $OutputEncoding.EncodingName"
powershell -Command "Write-Host 'Console.OutputEncoding:' [Console]::OutputEncoding.EncodingName"
echo.
pause
goto menu

:salir
echo.
echo 👋 ¡Hasta luego!
exit

:menu
cls
echo.
echo ╔════════════════════════════════════════════╗
echo ║        CONFIGURACION DE CONSOLA UTF-8      ║
echo ╚════════════════════════════════════════════╝
echo.
echo [1] Aplicar configuración completa (recomendado)
echo [2] Solo cambiar página de códigos a UTF-8
echo [3] Configurar fuente de consola
echo [4] Restaurar configuración predeterminada
echo [5] Ver configuración actual
echo [0] Salir
echo.
set /p opcion="Selecciona una opción: "

if "%opcion%"=="1" goto completa
if "%opcion%"=="2" goto utf8only
if "%opcion%"=="3" goto fuente
if "%opcion%"=="4" goto restaurar
if "%opcion%"=="5" goto ver
if "%opcion%"=="0" goto salir
goto menu
