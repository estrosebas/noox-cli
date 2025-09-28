#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones del módulo de proyectos.
"""

import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_vscode_detection():
    """Prueba la detección mejorada de VS Code."""
    print("🔍 Probando detección de VS Code...")
    
    try:
        from noox_cli.modules.proyectos import ProyectosModule
        
        proyectos = ProyectosModule()
        
        # Probar detección de comando
        vscode_detected = proyectos._command_exists('code')
        print(f"  Detección de comando 'code': {'✅' if vscode_detected else '❌'}")
        
        # Probar verificación específica de VS Code
        vscode_installed = proyectos._check_vscode_installation()
        print(f"  Verificación específica VS Code: {'✅' if vscode_installed else '❌'}")
        
        if vscode_installed:
            print("  💡 VS Code detectado correctamente")
        else:
            print("  ⚠️ VS Code no detectado - verificar instalación")
        
        return vscode_installed
        
    except Exception as e:
        print(f"  ❌ Error en prueba de VS Code: {e}")
        return False

def test_terminal_opening():
    """Prueba la apertura mejorada de terminal."""
    print("\n🖥️ Probando apertura de terminal...")
    
    try:
        from noox_cli.modules.proyectos import ProyectosModule
        
        proyectos = ProyectosModule()
        
        # Usar directorio actual para la prueba
        test_path = Path.cwd()
        
        print(f"  Directorio de prueba: {test_path}")
        
        # Nota: No ejecutamos realmente la apertura para evitar abrir ventanas
        # Solo verificamos que la función existe y es callable
        
        if hasattr(proyectos, '_open_terminal'):
            print("  ✅ Función _open_terminal disponible")
            
            # Verificar que es callable
            if callable(proyectos._open_terminal):
                print("  ✅ Función _open_terminal es ejecutable")
                return True
            else:
                print("  ❌ Función _open_terminal no es ejecutable")
                return False
        else:
            print("  ❌ Función _open_terminal no encontrada")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en prueba de terminal: {e}")
        return False

def test_powershell_profile():
    """Verifica que el perfil de PowerShell esté corregido."""
    print("\n🔧 Verificando perfil de PowerShell...")
    
    try:
        import subprocess
        import os
        
        username = os.environ.get('USERNAME', '')
        
        # Probar PowerShell 7 (que es el que usas principalmente)
        ps7_profile = rf"C:\Users\{username}\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
        
        if os.path.exists(ps7_profile):
            try:
                # Probar con un comando más simple
                result = subprocess.run([
                    'pwsh', '-NoProfile', '-Command',
                    f'. "{ps7_profile}"; Write-Host "PROFILE-TEST-OK"'
                ], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and "PROFILE-TEST-OK" in result.stdout:
                    print("  ✅ PowerShell 7 perfil funciona correctamente")
                    return True
                else:
                    print("  ❌ PowerShell 7 perfil tiene problemas")
                    # Mostrar solo las primeras líneas del error
                    if result.stderr:
                        error_lines = result.stderr.split('\n')[:3]
                        print(f"    Error: {' '.join(error_lines)}")
                    return False
                    
            except subprocess.TimeoutExpired:
                print("  ⏱️ Timeout verificando PowerShell 7")
                return False
            except FileNotFoundError:
                print("  ⚠️ PowerShell 7 (pwsh) no está disponible")
                return False
            except Exception as e:
                print(f"  ❌ Error ejecutando test: {e}")
                return False
        else:
            print(f"  ⚠️ No existe perfil de PowerShell 7: {ps7_profile}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error verificando perfil: {e}")
        return False

def test_project_detection():
    """Prueba la detección de proyectos."""
    print("\n📁 Probando detección de proyectos...")
    
    try:
        from noox_cli.modules.proyectos import ProyectosModule
        
        proyectos = ProyectosModule()
        
        # Verificar que el directorio de proyectos existe
        if proyectos.projects_path.exists():
            print(f"  ✅ Directorio de proyectos encontrado: {proyectos.projects_path}")
            
            # Obtener lista de proyectos
            projects = proyectos._get_projects()
            print(f"  📂 Proyectos encontrados: {len(projects)}")
            
            # Mostrar algunos proyectos si existen
            if projects:
                for i, project in enumerate(projects[:3]):  # Mostrar máximo 3
                    project_type = proyectos._detect_project_type(project)
                    print(f"    {i+1}. {project.name} ({project_type})")
                
                if len(projects) > 3:
                    print(f"    ... y {len(projects) - 3} más")
            
            return True
        else:
            print(f"  ⚠️ Directorio de proyectos no encontrado: {proyectos.projects_path}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en detección de proyectos: {e}")
        return False

def main():
    """Función principal de las pruebas."""
    print("🧪 PRUEBAS DE CORRECCIONES - MÓDULO PROYECTOS")
    print("=" * 50)
    
    tests = [
        ("Detección de VS Code", test_vscode_detection),
        ("Apertura de terminal", test_terminal_opening),
        ("Perfil de PowerShell", test_powershell_profile),
        ("Detección de proyectos", test_project_detection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error ejecutando {test_name}: {e}")
            results.append(False)
    
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
    
    if success_rate >= 0.8:
        print("🎉 ¡Correcciones aplicadas exitosamente!")
        return 0
    else:
        print("⚠️ Algunas correcciones necesitan revisión")
        return 1

if __name__ == '__main__':
    sys.exit(main())