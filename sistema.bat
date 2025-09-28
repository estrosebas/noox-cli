@echo off
REM Script de gestion del sistema - by Sebas
title Administracion del Sistema

:menu
cls
echo.
echo ╔═════════════════════════════════════════╗
echo ║      ADMINISTRACION DEL SISTEMA         ║
echo ╚═════════════════════════════════════════╝
echo.
echo [1] Informacion del sistema
echo [2] Procesos en ejecucion
echo [3] Uso de red
echo [4] Espacio en disco
echo [5] Servicios de Windows
echo [6] Variables de entorno
echo [7] Limpiar archivos temporales
echo [8] Administrador de tareas
echo [9] Editor del registro
echo [A] Información de IP/Red
echo [B] Ping a servidor
echo [C] Flush DNS
echo [0] Salir
echo.
set /p opcion="Selecciona una opcion: "

if /i "%opcion%"=="1" goto sysinfo
if /i "%opcion%"=="2" goto procesos
if /i "%opcion%"=="3" goto network
if /i "%opcion%"=="4" goto disk
if /i "%opcion%"=="5" goto services
if /i "%opcion%"=="6" goto env
if /i "%opcion%"=="7" goto cleanup
if /i "%opcion%"=="8" goto taskmgr
if /i "%opcion%"=="9" goto registry
if /i "%opcion%"=="A" goto ipinfo
if /i "%opcion%"=="B" goto ping
if /i "%opcion%"=="C" goto dns
if "%opcion%"=="0" goto salir

goto menu

:sysinfo
systeminfo | findstr /C:"Nombre del host" /C:"Nombre del sistema" /C:"Tipo de sistema" /C:"Memoria física total"
pause
goto menu

:procesos
tasklist | more
pause
goto menu

:network
netstat -an | more
pause
goto menu

:disk
echo.
echo === ESPACIO EN DISCO ===
wmic logicaldisk get size,freespace,caption
echo.
dir /s /-c %TEMP% 2>nul | find "bytes"
echo Archivos temporales ^
pause
goto menu

:services
echo [1] Ver todos los servicios
echo [2] Ver servicios en ejecucion
set /p svc="Selecciona: "
if "%svc%"=="1" net start
if "%svc%"=="2" sc query type= service
pause
goto menu

:env
set | more
pause
goto menu

:cleanup
echo Limpiando archivos temporales...
del /q /f /s %TEMP%\* 2>nul
for /d %%i in ("%TEMP%\*") do rmdir /s /q "%%i" 2>nul
echo Limpieza completada!
pause
goto menu

:taskmgr
start taskmgr
goto menu

:registry
start regedit
goto menu

:ipinfo
echo === INFORMACION DE RED ===
ipconfig /all | findstr /C:"Adaptador" /C:"IPv4" /C:"IPv6" /C:"Puerta de enlace"
echo.
echo === DIRECCION IP PUBLICA ===
powershell -Command "try { (Invoke-WebRequest -Uri 'https://api.ipify.org' -UseBasicParsing).Content } catch { 'No se pudo obtener IP publica' }"
pause
goto menu

:ping
set /p servidor="Introduce servidor/IP para ping: "
ping -t %servidor%
pause
goto menu

:dns
echo Limpiando cache DNS...
ipconfig /flushdns
echo Cache DNS limpiado!
pause
goto menu

:salir
exit
