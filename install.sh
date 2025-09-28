#!/bin/bash
# Script de instalación de NooxCLI - Linux/macOS
# chmod +x install.sh && ./install.sh

clear
echo "╔═══════════════════════════════════════════╗"
echo "║             INSTALACIÓN NOOXCLI           ║"
echo "╚═══════════════════════════════════════════╝"
echo
echo "🚀 Instalando NooxCLI - CLI Moderna"
echo

# Función para mostrar mensajes de error
error_exit() {
    echo "❌ Error: $1"
    echo "Presiona cualquier tecla para salir..."
    read -n 1
    exit 1
}

# Verificar Python
echo "[1/3] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        error_exit "Python no está instalado. Por favor instala Python 3.8+ desde https://python.org"
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION encontrado"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        error_exit "pip no está instalado. Por favor instala pip"
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

echo
echo "[2/3] Instalando dependencias..."
$PIP_CMD install -r requirements.txt || error_exit "Error instalando dependencias"
echo "✅ Dependencias instaladas"

echo
echo "[3/3] Instalando NooxCLI..."
$PIP_CMD install -e . || error_exit "Error instalando NooxCLI"
echo "✅ NooxCLI instalado correctamente"

echo
echo "╔═══════════════════════════════════════════╗"
echo "║          INSTALACIÓN COMPLETADA           ║"
echo "╚═══════════════════════════════════════════╝"
echo
echo "🎉 ¡NooxCLI se ha instalado correctamente!"
echo
echo "📌 Para usar NooxCLI:"
echo "   • Ejecuta: python3 -m noox_cli.main"
echo "   • O desde cualquier lugar: noox (si está en PATH)"
echo
echo "🔧 Para desinstalar:"
echo "   • Ejecuta: pip3 uninstall noox-cli"
echo
echo "📚 Documentación y ayuda:"
echo "   • GitHub: https://github.com/tu-usuario/noox-cli"
echo "   • Ayuda: python3 -m noox_cli.main (luego selecciona Ayuda)"
echo
echo "Presiona cualquier tecla para continuar..."
read -n 1
