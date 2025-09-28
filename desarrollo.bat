@echo off
REM Script de desarrollo rapido - by Sebas
title Herramientas de Desarrollo

:menu
cls
echo.
echo ╔══════════════════════════════════════════╗
echo ║        HERRAMIENTAS DE DESARROLLO        ║
echo ╚══════════════════════════════════════════╝
echo.
echo [1] Abrir VS Code en directorio actual
echo [2] Inicializar proyecto Git
echo [3] Instalar dependencias Node.js
echo [4] Crear estructura proyecto Python
echo [5] Lanzar servidor local (Python)
echo [6] Abrir PowerShell en directorio
echo [7] Ver estado Git
echo [8] Push rapido a Git
echo [9] Limpiar cache npm/yarn
echo [0] Salir
echo.
set /p opcion="Selecciona una opcion: "

if "%opcion%"=="1" goto vscode
if "%opcion%"=="2" goto initgit
if "%opcion%"=="3" goto npm
if "%opcion%"=="4" goto python
if "%opcion%"=="5" goto server
if "%opcion%"=="6" goto powershell
if "%opcion%"=="7" goto gitstatus
if "%opcion%"=="8" goto gitpush
if "%opcion%"=="9" goto cleancache
if "%opcion%"=="0" goto salir

goto menu

:vscode
code .
goto menu

:initgit
git init
git add .
git commit -m "Initial commit"
pause
goto menu

:npm
echo [1] npm install
echo [2] yarn install
set /p pkg="Selecciona gestor: "
if "%pkg%"=="1" npm install
if "%pkg%"=="2" yarn install
pause
goto menu

:python
mkdir src tests docs
echo # Proyecto Python > README.md
echo # Dependencias > requirements.txt
echo from src import main > main.py
pause
goto menu

:server
echo [1] Python HTTP Server (puerto 8000)
echo [2] Node.js Express (puerto 3000)
set /p srv="Selecciona: "
if "%srv%"=="1" python -m http.server 8000
if "%srv%"=="2" npx create-react-app . --template typescript
pause
goto menu

:powershell
start powershell -NoExit -Command "cd '%cd%'"
goto menu

:gitstatus
git status
git log --oneline -5
pause
goto menu

:gitpush
set /p msg="Mensaje del commit: "
git add .
git commit -m "%msg%"
git push
pause
goto menu

:cleancache
echo Limpiando cache...
npm cache clean --force 2>nul
yarn cache clean 2>nul
echo Cache limpiado!
pause
goto menu

:salir
exit
