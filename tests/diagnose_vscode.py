#!/usr/bin/env python3
"""
Script de diagnóstico para encontrar VS Code en el sistema.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_path_variables():
    """Verifica las variables PATH del usuario y del sistema."""
    print("🔍 VERIFICANDO VARIABLES PATH")
    print("-" * 40)
    
    # PATH del usuario actual
    user_path = os.environ.get('PATH', '')
    print(f"📁 PATH del usuario:")
    for path_entry in user_path.split(';'):
        if 'VS Code' in path_entry or 'code' in path_entry.lower():
            print(f"  ✅ {path_entry}")
    
    # Verificar PATH del sistema (Windows)
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
            system_path = winreg.QueryValueEx(key, "Path")[0]
            print(f"\n🖥️ PATH del sistema:")
            for path_entry in system_path.split(';'):
                if 'VS Code' in path_entry or 'code' in path_entry.lower():
                    print(f"  ✅ {path_entry}")
    except Exception as e:
        print(f"  ❌ No se pudo acceder al PATH del sistema: {e}")

def check_common_locations():
    """Verifica ubicaciones comunes de VS Code."""
    print("\n📂 VERIFICANDO UBICACIONES COMUNES")
    print("-" * 40)
    
    username = os.environ.get('USERNAME', '')
    
    locations = [
        # Tu ubicación específica
        rf"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code",
        rf"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\bin",
        rf"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
        rf"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        
        # Ubicaciones del sistema
        r"C:\Program Files\Microsoft VS Code",
        r"C:\Program Files\Microsoft VS Code\bin",
        r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        
        # Ubicaciones x86
        r"C:\Program Files (x86)\Microsoft VS Code",
        r"C:\Program Files (x86)\Microsoft VS Code\bin",
        r"C:\Program Files (x86)\Microsoft VS Code\bin\code.cmd",
        r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
    ]
    
    found_locations = []
    
    for location in locations:
        if os.path.exists(location):
            print(f"  ✅ {location}")
            found_locations.append(location)
        else:
            print(f"  ❌ {location}")
    
    return found_locations

def test_vscode_commands():
    """Prueba diferentes comandos para abrir VS Code."""
    print("\n🧪 PROBANDO COMANDOS DE VS CODE")
    print("-" * 40)
    
    username = os.environ.get('USERNAME', '')
    
    commands = [
        'code',
        'code.cmd',
        rf"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
        rf"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
        r"C:\Program Files\Microsoft VS Code\Code.exe"
    ]
    
    working_commands = []
    
    for cmd in commands:
        try:
            # Probar solo --version para no abrir VS Code
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0] if result.stdout else 'Desconocida'
                print(f"  ✅ {cmd} - Versión: {version}")
                working_commands.append(cmd)
            else:
                print(f"  ❌ {cmd} - Error: {result.stderr[:50]}...")
                
        except subprocess.TimeoutExpired:
            print(f"  ⏱️ {cmd} - Timeout")
        except FileNotFoundError:
            print(f"  ❌ {cmd} - No encontrado")
        except Exception as e:
            print(f"  ❌ {cmd} - Error: {e}")
    
    return working_commands

def check_registry():
    """Verifica entradas del registro relacionadas con VS Code."""
    print("\n📋 VERIFICANDO REGISTRO DE WINDOWS")
    print("-" * 40)
    
    try:
        import winreg
        
        # Verificar aplicaciones instaladas
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        
        for hkey, path in registry_paths:
            try:
                with winreg.OpenKey(hkey, path) as key:
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            if 'code' in subkey_name.lower() or 'visual' in subkey_name.lower():
                                try:
                                    with winreg.OpenKey(key, subkey_name) as subkey:
                                        try:
                                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                            if 'Visual Studio Code' in display_name:
                                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                                print(f"  ✅ {display_name}")
                                                print(f"     📁 Ubicación: {install_location}")
                                        except FileNotFoundError:
                                            pass
                                except Exception:
                                    pass
                            i += 1
                        except OSError:
                            break
            except Exception as e:
                print(f"  ❌ Error accediendo a {path}: {e}")
                
    except ImportError:
        print("  ❌ winreg no disponible")

def main():
    """Función principal del diagnóstico."""
    print("🔍 DIAGNÓSTICO DE VS CODE")
    print("=" * 50)
    
    # Información del sistema
    print(f"👤 Usuario: {os.environ.get('USERNAME', 'Desconocido')}")
    print(f"💻 Sistema: {os.name}")
    
    # Ejecutar diagnósticos
    check_path_variables()
    found_locations = check_common_locations()
    working_commands = test_vscode_commands()
    check_registry()
    
    # Resumen y recomendaciones
    print("\n📊 RESUMEN Y RECOMENDACIONES")
    print("=" * 50)
    
    if working_commands:
        print("✅ VS Code encontrado y funcional!")
        print("🎯 Comandos que funcionan:")
        for cmd in working_commands:
            print(f"  - {cmd}")
        
        print("\n💡 Recomendación:")
        print(f"   Usar: {working_commands[0]}")
        
    elif found_locations:
        print("⚠️ VS Code encontrado pero comandos no funcionan")
        print("🔧 Ubicaciones encontradas:")
        for loc in found_locations:
            print(f"  - {loc}")
        
        print("\n💡 Recomendaciones:")
        print("1. Agregar la carpeta 'bin' de VS Code al PATH")
        print("2. O usar la ruta completa al ejecutable")
        
    else:
        print("❌ VS Code no encontrado")
        print("\n💡 Recomendaciones:")
        print("1. Instalar VS Code desde: https://code.visualstudio.com/")
        print("2. Durante la instalación, marcar 'Add to PATH'")

if __name__ == '__main__':
    main()