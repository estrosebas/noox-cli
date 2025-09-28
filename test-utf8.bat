@echo off
REM Script de prueba UTF-8 - by Sebas
title Prueba de Caracteres Especiales UTF-8

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║           PRUEBA DE UTF-8 Y CARACTERES       ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM Mostrar página de códigos actual
echo 📊 Información actual:
echo =====================
echo Página de códigos: 
chcp
echo.

REM Prueba de caracteres especiales básicos
echo 🎯 CARACTERES ESPECIALES BÁSICOS:
echo ==================================
echo ñ Ñ á é í ó ú Á É Í Ó Ú ü Ü ¿ ¡
echo àèìòù ÀÈÌÒÙ âêîôû ÂÊÎÔÛ
echo ç Ç œ Œ æ Æ ß
echo.

REM Prueba de símbolos de caja (box drawing)
echo 📦 SÍMBOLOS DE CAJA:
echo ===================
echo ┌─┬─┐  ╔═╦═╗  ╭───╮
echo │ │ │  ║ ║ ║  │   │
echo ├─┼─┤  ╠═╬═╣  ├───┤
echo │ │ │  ║ ║ ║  │   │
echo └─┴─┘  ╚═╩═╝  ╰───╯
echo.

REM Prueba de emojis y símbolos unicode
echo 🎨 EMOJIS Y SÍMBOLOS:
echo ====================
echo 💻 🚀 ⚡ 🔥 ✨ 🎯 📁 📝 🌐 ⚙️
echo ✅ ❌ ⚠️ 📊 🎉 💡 🔧 🎪 🌟 🏆
echo.

REM Prueba de caracteres matemáticos y técnicos
echo 📐 SÍMBOLOS MATEMÁTICOS:
echo =======================
echo π ∑ ∆ ∞ ± × ÷ √ ∫ ∂
echo α β γ δ λ μ σ Ω θ φ
echo ← ↑ → ↓ ↔ ↕ ⇐ ⇑ ⇒ ⇓
echo.

REM Prueba de caracteres de moneda
echo 💰 SÍMBOLOS DE MONEDA:
echo =====================
echo $ € £ ¥ ¢ ₹ ₽ ₩ ₪ ₫
echo.

REM Prueba de caracteres especiales de programación
echo 💻 CARACTERES DE PROGRAMACIÓN:
echo =============================
echo { } [ ] < > ( ) " ' `
echo | \ / ~ # @ & * % ^
echo.

REM Mostrar tabla de colores si es posible
echo 🌈 PRUEBA DE COLORES:
echo ====================
echo [91mRojo[0m [92mVerde[0m [93mAmarillo[0m [94mAzul[0m [95mMagenta[0m [96mCian[0m
echo.

echo 🔍 DIAGNÓSTICO:
echo ===============
if "%1"=="auto" (
    echo Ejecutando en modo automático...
    goto diagnostico
) else (
    set /p diagnostico="¿Quieres ver diagnóstico completo? (S/N): "
    if /i "%diagnostico%"=="S" goto diagnostico
    goto fin
)

:diagnostico
echo.
echo 📋 Información del sistema:
echo Codepage actual: 
chcp
echo.
powershell -Command "Write-Host 'PowerShell OutputEncoding:' $OutputEncoding.EncodingName"
powershell -Command "Write-Host 'Console OutputEncoding:' [Console]::OutputEncoding.EncodingName"
echo.
echo 📝 Configuración del registro:
powershell -Command "Get-ItemProperty -Path 'HKCU:\Console' -Name 'CodePage' -ErrorAction SilentlyContinue | Select-Object CodePage"
echo.

:fin
echo.
echo 🎯 RESULTADO:
echo =============
echo Si puedes ver correctamente todos los caracteres especiales,
echo emojis y símbolos mostrados arriba, entonces la configuración
echo UTF-8 está funcionando perfectamente.
echo.
echo Si algunos caracteres se ven como cuadros, signos de interrogación
echo o caracteres extraños, entonces necesitas ejecutar el script de
echo configuración: config-consola.bat
echo.
pause
