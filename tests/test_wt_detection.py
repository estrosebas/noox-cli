#!/usr/bin/env python3
"""
Script de prueba para verificar la detección mejorada de Windows Terminal.
"""

import os
import sys
import glob
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_wt_command():
    """Verifica si el comando 'wt' está disponible."""
    print("🔍 VERIFICANDO COMANDO 'wt'")
    print("-" * 40)
    
    try:
        import subprocess
        result = subprocess.run(['wt', '--help'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        
        if result.returncode == 0:
            print("  ✅ Comando 'wt' disponible en PATH")
            return True
        else:
            print("  ❌ Comando 'wt' no funciona")
            return False
            
    except subprocess.TimeoutExpired:
        print("  ⏱️ Timeout ejecutando 'wt --help'")
        return False
    except FileNotFoundError:
        print("  ❌ Comando 'wt' no encontrado en PATH")
        return False
    except Exception as e:
        print(f"  ❌ Error verificando 'wt': {e}")
        return False

def test_wt_executable_search():
    """Busca el ejecutable de Windows Terminal en ubicaciones comunes."""
    print("\n📂 BUSCANDO EJECUTABLE DE WINDOWS TERMINAL")
    print("-" * 40)
    
    # Ubicaciones a verificar
    wt_paths = [
        # Microsoft Store - usuario actual
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe'),
        # Microsoft Store - sistema (con wildcard)
        r'C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_*\wt.exe',
        # Instalación manual
        r'C:\Program Files\Windows Terminal\wt.exe',
        r'C:\Program Files (x86)\Windows Terminal\wt.exe',
        # Otras ubicaciones posibles
        os.path.expandvars(r'%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\Microsoft.WindowsTerminal_*\wt.exe'),
        os.path.expandvars(r'%PROGRAMFILES%\WindowsApps\Microsoft.WindowsTerminal_*\wt.exe')
    ]
    
    found_paths = []
    
    for wt_path in wt_paths:
        try:
            print(f"  🔍 Buscando: {wt_path}")
            
            # Para rutas con wildcards, usar glob
            if '*' in wt_path:
                matching_paths = glob.glob(wt_path)
                if matching_paths:
                    # Ordenar para obtener la versión más reciente
                    matching_paths.sort(reverse=True)
                    for match in matching_paths:
                        if os.path.exists(match):
                            print(f"    ✅ Encontrado: {match}")
                            found_paths.append(match)
                        else:
                            print(f"    ❌ No existe: {match}")
                else:
                    print(f"    ❌ No hay coincidencias para el patrón")
            else:
                if os.path.exists(wt_path):
                    print(f"    ✅ Encontrado: {wt_path}")
                    found_paths.append(wt_path)
                else:
                    print(f"    ❌ No existe: {wt_path}")
                    
        except Exception as e:
            print(f"    ❌ Error buscando: {e}")
    
    print(f"\n📊 Ejecutables encontrados: {len(found_paths)}")
    return found_paths

def test_module_detection():
    """Prueba la detección de Windows Terminal en los módulos."""
    print("\n🔗 PROBANDO DETECCIÓN EN MÓDULOS")
    print("-" * 40)
    
    try:
        # Probar módulo desarrollo
        from noox_cli.modules.desarrollo import DesarrolloModule
        desarrollo = DesarrolloModule()
        
        wt_found_dev = desarrollo._find_windows_terminal()
        print(f"  Módulo desarrollo encontró WT: {'✅' if wt_found_dev else '❌'}")
        if wt_found_dev:
            print(f"    Ruta: {wt_found_dev}")
        
        # Probar módulo proyectos
        from noox_cli.modules.proyectos import ProyectosModule
        proyectos = ProyectosModule()
        
        wt_found_proj = proyectos._find_windows_terminal()
        print(f"  Módulo proyectos encontró WT: {'✅' if wt_found_proj else '❌'}")
        if wt_found_proj:
            print(f"    Ruta: {wt_found_proj}")
        
        return wt_found_dev is not None or wt_found_proj is not None
        
    except Exception as e:
        print(f"  ❌ Error probando módulos: {e}")
        return False

def test_wt_execution():
    """Prueba ejecutar Windows Terminal (sin abrir realmente)."""
    print("\n🧪 PROBANDO EJECUCIÓN DE WINDOWS TERMINAL")
    print("-" * 40)
    
    try:
        from noox_cli.modules.desarrollo import DesarrolloModule
        desarrollo = DesarrolloModule()
        
        wt_executable = desarrollo._find_windows_terminal()
        
        if wt_executable:
            print(f"  📍 Ejecutable encontrado: {wt_executable}")
            
            # Probar comando de ayuda (no abre ventana)
            try:
                import subprocess
                result = subprocess.run([wt_executable, '--help'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                
                if result.returncode == 0:
                    print("  ✅ Ejecutable funciona correctamente")
                    return True
                else:
                    print("  ❌ Ejecutable no funciona")
                    return False
                    
            except subprocess.TimeoutExpired:
                print("  ⏱️ Timeout ejecutando Windows Terminal")
                return False
            except Exception as e:
                print(f"  ❌ Error ejecutando: {e}")
                return False
        else:
            print("  ❌ No se encontró ejecutable de Windows Terminal")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en prueba de ejecución: {e}")
        return False

def show_installation_info():
    """Muestra información sobre cómo instalar Windows Terminal."""
    print("\n💡 INFORMACIÓN DE INSTALACIÓN")
    print("-" * 40)
    
    print("  🏪 Microsoft Store:")
    print("    - Busca 'Windows Terminal'")
    print("    - Instalación automática de actualizaciones")
    print("    - Configuración integrada con Windows")
    
    print("\n  📦 winget (línea de comandos):")
    print("    winget install --id=Microsoft.WindowsTerminal -e")
    
    print("\n  🌐 Descarga manual:")
    print("    - GitHub: https://github.com/microsoft/terminal/releases")
    print("    - Descargar archivo .msixbundle")
    
    print("\n  ✨ Beneficios:")
    print("    - Pestañas múltiples")
    print("    - Iconos y colores personalizables")
    print("    - Mejor rendimiento")
    print("    - Soporte completo UTF-8")

def main():
    """Función principal de las pruebas de detección de Windows Terminal."""
    print("🖥️ PRUEBAS DE DETECCIÓN MEJORADA - WINDOWS TERMINAL")
    print("=" * 60)
    
    tests = [
        ("Comando 'wt'", test_wt_command),
        ("Búsqueda de ejecutable", lambda: len(test_wt_executable_search()) > 0),
        ("Detección en módulos", test_module_detection),
        ("Ejecución de WT", test_wt_execution)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append(False)
    
    # Mostrar información de instalación si no está disponible
    if not any(results):
        show_installation_info()
    
    # Resumen
    print("\n📊 RESUMEN DE PRUEBAS")
    print("-" * 30)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    success_rate = passed / total if total > 0 else 0
    print(f"\nPuntuación: {success_rate:.1%} ({passed}/{total})")
    
    if success_rate >= 0.5:
        print("🎉 ¡Windows Terminal detectado o parcialmente disponible!")
        print("💡 Los terminales se abrirán en Windows Terminal cuando sea posible")
        return 0
    else:
        print("⚠️ Windows Terminal no detectado")
        print("💡 Se usarán terminales tradicionales como fallback")
        print("🔧 Considera instalar Windows Terminal para mejor experiencia")
        return 1

if __name__ == '__main__':
    sys.exit(main())