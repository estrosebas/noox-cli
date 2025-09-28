@echo off
REM Script de instalación de NooxCLI - Windows
title Instalación de NooxCLI

echo.
echo ╔═══════════════════════════════════════════╗
echo ║             INSTALACIÓN NOOXCLI           ║
echo ╚═══════════════════════════════════════════╝
echo.
echo 🚀 Instalando NooxCLI - CLI Moderna
echo.

echo [1/3] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo    Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo ✅ Python %PYTHON_VERSION% encontrado

echo.
echo [2/3] Instalando dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas

echo.
echo [3/3] Instalando NooxCLI...
pip install -e .
if errorlevel 1 (
    echo ❌ Error instalando NooxCLI
    pause
    exit /b 1
)
echo ✅ NooxCLI instalado correctamente

echo.
echo ╔═══════════════════════════════════════════╗
echo ║          INSTALACIÓN COMPLETADA           ║
echo ╚═══════════════════════════════════════════╝
echo.
echo 🎉 ¡NooxCLI se ha instalado correctamente!
echo.
echo 📌 Para usar NooxCLI:
echo    • Ejecuta: python -m noox_cli.main
echo    • O desde cualquier lugar: noox (si está en PATH)
echo.
echo 🔧 Para desinstalar:
echo    • Ejecuta: pip uninstall noox-cli
echo.
echo 📚 Documentación y ayuda:
echo    • GitHub: https://github.com/tu-usuario/noox-cli
echo    • Ayuda: python -m noox_cli.main (luego selecciona Ayuda)
echo.
pause
