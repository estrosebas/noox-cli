@echo off
setlocal EnableDelayedExpansion
REM Script de gestion de proyectos Laragon - by Sebas
title Proyectos de Laragon

:menu
cls
echo.
echo ╔═════════════════════════════════════════╗
echo ║       PROYECTOS DE LARAGON (PHP)       ║
echo ╚═════════════════════════════════════════╝
echo.
echo 📁 Proyectos disponibles en C:\laragonzo\www:
echo.

REM Verificar si existe el directorio de Laragon
if not exist "C:\laragonzo\www" (
echo ❌ No se encontró el directorio de Laragon: C:\laragonzo\www
    echo.
    echo [0] Salir
    set /p opcion="Presiona cualquier tecla para salir: "
    goto salir
)

REM Cambiar al directorio de Laragon
cd /d "C:\laragonzo\www"

REM Mostrar proyectos con numeración
set count=0
for /d %%i in (*) do (
    set /a count+=1
    set "proyecto!count!=%%i"
    echo [!count!] 🚀 %%i
)

echo.
echo [A] 📂 Abrir carpeta de Laragon
echo [N] ➕ Crear nuevo proyecto PHP
echo [G] 🔄 Gestión avanzada
echo [0] 🚪 Salir
echo.
set /p opcion="Selecciona un proyecto o opción: "

REM Comprobar si es un número (proyecto)
if "%opcion%" geq "1" if "%opcion%" leq "99" (
    if defined proyecto%opcion% (
        call :abrirProyecto "!proyecto%opcion%!"
        goto menu
    ) else (
        echo Proyecto no válido.
        pause
        goto menu
    )
)

REM Comprobar opciones especiales
if /i "%opcion%"=="A" goto abrirCarpeta
if /i "%opcion%"=="N" goto nuevoPHP
if /i "%opcion%"=="G" goto gestion
if "%opcion%"=="0" goto salir

goto menu

REM Función para abrir un proyecto
:abrirProyecto
set proyectoNombre=%~1
cd /d "C:\laragonzo\www\%proyectoNombre%"
echo.
echo 🚀 Abriendo proyecto: %proyectoNombre%
echo.
echo [1] 📝 Abrir en VS Code
echo [2] 💻 Abrir terminal aquí
echo [3] 🌐 Abrir en navegador (localhost/%proyectoNombre%)
echo [4] 📁 Abrir carpeta en explorador
echo [0] ⬅️ Volver
echo.
set /p accion="¿Qué quieres hacer?: "

if "%accion%"=="1" start code .
if "%accion%"=="2" start powershell -NoExit -Command "cd '%cd%'"
if "%accion%"=="3" start http://localhost/%proyectoNombre%
if "%accion%"=="4" start explorer .
if "%accion%"=="0" goto :eof

echo.
echo ✨ ¡Acción ejecutada!
pause
goto :eof

:abrirCarpeta
start explorer "C:\laragonzo\www"
echo 📂 Carpeta de Laragon abierta.
pause
goto menu

:nuevoPHP
cls
echo.
echo ➕ CREAR NUEVO PROYECTO PHP
echo =============================
echo.
set /p nombrePHP="Nombre del proyecto: "

if "%nombrePHP%"=="" (
    echo ❌ El nombre no puede estar vacío.
    pause
    goto menu
)

cd /d "C:\laragonzo\www"
if exist "%nombrePHP%" (
    echo ❌ Ya existe un proyecto con ese nombre.
    pause
    goto menu
)

mkdir "%nombrePHP%"
cd "%nombrePHP%"

echo ^<?php > index.php
echo echo "^<h1^>Bienvenido a %nombrePHP%^</h1^>"; >> index.php
echo echo "^<p^>Proyecto creado el: " . date('Y-m-d H:i:s'); >> index.php
echo ?^> >> index.php

echo ^<!DOCTYPE html^> > README.md
echo # %nombrePHP% >> README.md
echo. >> README.md
echo Proyecto PHP creado con Laragon >> README.md
echo. >> README.md
echo ## Cómo usar >> README.md
echo 1. Abre http://localhost/%nombrePHP% >> README.md

echo.
echo ✨ ¡Proyecto %nombrePHP% creado exitosamente!
echo 🔗 Puedes acceder en: http://localhost/%nombrePHP%
echo.
echo ¿Quieres abrirlo ahora?
echo [1] Sí, abrir en VS Code
echo [2] Sí, abrir en navegador
echo [0] No, volver al menú
set /p abrir="Selección: "

if "%abrir%"=="1" start code .
if "%abrir%"=="2" start http://localhost/%nombrePHP%

pause
goto menu

:gestion
cls
echo.
echo 🔄 GESTIÓN AVANZADA DE PROYECTOS
echo ================================
echo.
echo [1] Crear nuevo proyecto avanzado
echo [2] Clonar repositorio Git
echo [3] Backup de proyecto
echo [4] Comprimir proyecto
echo [5] Deploy a servidor
echo [6] Ejecutar tests
echo [7] Build de producción
echo [8] Docker operations
echo [0] Volver
echo.
set /p gestionOpcion="Selección: "

if "%gestionOpcion%"=="1" goto nuevo
if "%gestionOpcion%"=="2" goto clonar
if "%gestionOpcion%"=="3" goto backup
if "%gestionOpcion%"=="4" goto comprimir
if "%gestionOpcion%"=="5" goto deploy
if "%gestionOpcion%"=="6" goto tests
if "%gestionOpcion%"=="7" goto build
if "%gestionOpcion%"=="8" goto docker
if "%gestionOpcion%"=="0" goto menu
goto gestion

:nuevo
set /p nombre="Nombre del proyecto: "
set /p tipo="Tipo [web/python/node/react]: "

mkdir "%nombre%"
cd "%nombre%"

if /i "%tipo%"=="web" goto web
if /i "%tipo%"=="python" goto py
if /i "%tipo%"=="node" goto node
if /i "%tipo%"=="react" goto react

:web
echo ^<!DOCTYPE html^> > index.html
echo ^<html^>^<head^>^<title^>%nombre%^</title^>^</head^> >> index.html
echo ^<body^>^<h1^>Proyecto %nombre%^</h1^>^</body^>^</html^> >> index.html
echo body { font-family: Arial; } > style.css
echo console.log('Proyecto %nombre% iniciado'); > script.js
goto proyectoCreado

:py
python -m venv venv
echo flask > requirements.txt
echo from flask import Flask > app.py
echo app = Flask(__name__) >> app.py
echo. >> app.py
echo @app.route('/') >> app.py
echo def home(): >> app.py
echo     return 'Proyecto %nombre%' >> app.py
goto proyectoCreado

:node
npm init -y
npm install express
echo const express = require('express'); > index.js
echo const app = express(); >> index.js
echo app.get('/', (req, res) =^> res.send('Proyecto %nombre%')); >> index.js
echo app.listen(3000, () =^> console.log('Server running on port 3000')); >> index.js
goto proyectoCreado

:react
npx create-react-app . --template typescript
goto proyectoCreado

:proyectoCreado
git init
git add .
git commit -m "Initial commit for %nombre%"
echo Proyecto %nombre% creado exitosamente!
pause
cd ..
goto menu

:abrir
echo Proyectos disponibles:
echo.
dir /b /ad
echo.
set /p proyecto="Nombre del proyecto a abrir: "
if exist "%proyecto%" (
    cd "%proyecto%"
    start code .
    start powershell -NoExit -Command "cd '%cd%'"
) else (
    echo Proyecto no encontrado!
    pause
)
goto menu

:clonar
set /p repo="URL del repositorio: "
set /p carpeta="Nombre de la carpeta (opcional): "
if "%carpeta%"=="" (
    git clone %repo%
) else (
    git clone %repo% %carpeta%
)
pause
goto menu

:recientes
echo === PROYECTOS RECIENTES ===
forfiles /m *.* /c "cmd /c if @isdir==TRUE echo @path - @fdate @ftime" 2>nul | sort /r
pause
goto menu

:backup
set /p proyecto="Proyecto a respaldar: "
if exist "%proyecto%" (
    set fecha=%date:~-4%-%date:~3,2%-%date:~0,2%
    powershell Compress-Archive -Path "%proyecto%" -DestinationPath "backup_%proyecto%_%fecha%.zip"
    echo Backup creado: backup_%proyecto%_%fecha%.zip
) else (
    echo Proyecto no encontrado!
)
pause
goto menu

:comprimir
set /p proyecto="Proyecto a comprimir: "
if exist "%proyecto%" (
    powershell Compress-Archive -Path "%proyecto%" -DestinationPath "%proyecto%.zip" -Force
    echo Proyecto comprimido: %proyecto%.zip
) else (
    echo Proyecto no encontrado!
)
pause
goto menu

:deploy
echo [1] Deploy via FTP
echo [2] Deploy via SSH
echo [3] Deploy via Git
set /p dep="Selecciona método: "
if "%dep%"=="1" echo Configurar FTP deploy...
if "%dep%"=="2" echo Configurar SSH deploy...
if "%dep%"=="3" (
    git add .
    set /p msg="Commit message: "
    git commit -m "%msg%"
    git push origin main
)
pause
goto menu

:tests
echo [1] Jest (JavaScript/TypeScript)
echo [2] Pytest (Python)
echo [3] Go test
echo [4] Cargo test (Rust)
set /p test="Selecciona: "
if "%test%"=="1" npm test
if "%test%"=="2" pytest
if "%test%"=="3" go test ./...
if "%test%"=="4" cargo test
pause
goto menu

:build
echo [1] npm run build
echo [2] Python setup.py build
echo [3] go build
echo [4] cargo build --release
set /p build="Selecciona: "
if "%build%"=="1" npm run build
if "%build%"=="2" python setup.py build
if "%build%"=="3" go build
if "%build%"=="4" cargo build --release
pause
goto menu

:docker
echo [1] Docker build
echo [2] Docker run
echo [3] Docker compose up
echo [4] Ver containers
set /p dock="Selecciona: "
if "%dock%"=="1" (
    set /p tag="Tag de la imagen: "
    docker build -t %tag% .
)
if "%dock%"=="2" (
    set /p img="Imagen a ejecutar: "
    docker run -p 8080:80 %img%
)
if "%dock%"=="3" docker-compose up -d
if "%dock%"=="4" docker ps -a
pause
goto menu

:salir
exit
