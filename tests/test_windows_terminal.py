#!/usr/bin/env python3
"""
Script de prueba para verificar la integración con Windows Terminal.
"""

import os
import sys
import subprocess
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_windows_terminal_detection():
    """Verifica si Windows Terminal está disponible."""
    print("🖥️ VERIFICANDO WINDOWS TERMINAL")
    print("-" * 40)
    
    # Verificar si estamos ejecutándose dentro de Windows Terminal
    wt_session = os.environ.get('WT_SESSION')
    if wt_session:
        print(f"  ✅ Ejecutándose dentro de Windows Terminal (Session: {wt_session})")
    else:
        print("  ℹ️ No se detectó sesión de Windows Terminal")
    
    # Verificar si el comando 'wt' está disponible
    try:
        result = subprocess.run(['wt', '--help'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        
        if result.returncode == 0:
            print("  ✅ Comando 'wt' disponible")
            return True
        else:
            print("  ❌ Comando 'wt' no funciona correctamente")
            return False
            
    except subprocess.TimeoutExpired:
        print("  ⏱️ Timeout ejecutando 'wt --help'")
        return False
    except FileNotFoundError:
        print("  ❌ Comando 'wt' no encontrado")
        return False
    except Exception as e:
        print(f"  ❌ Error verificando 'wt': {e}")
        return False

def test_wt_command_syntax():
    """Prueba la sintaxis de comandos de Windows Terminal."""
    print("\n🧪 PROBANDO SINTAXIS DE COMANDOS WT")
    print("-" * 40)
    
    # Comandos que vamos a probar (sin ejecutar realmente)
    test_commands = [
        # Nueva pestaña en sesión existente
        ['wt', 'new-tab', '--startingDirectory', 'C:\\'],
        
        # Nueva ventana
        ['wt', '-d', 'C:\\'],
        
        # Nueva pestaña con PowerShell específico
        ['wt', 'new-tab', '--startingDirectory', 'C:\\', 'pwsh', '-NoProfile'],
        
        # Nueva pestaña con CMD
        ['wt', 'new-tab', '--startingDirectory', 'C:\\', 'cmd', '/k', 'echo Test']
    ]
    
    print("  📋 Comandos que se usarán:")
    for i, cmd in enumerate(test_commands, 1):
        cmd_str = ' '.join(cmd)
        print(f"    {i}. {cmd_str}")
    
    print("  ✅ Sintaxis de comandos preparada")
    return True

def test_module_wt_integration():
    """Verifica que los módulos detecten Windows Terminal correctamente."""
    print("\n🔗 VERIFICANDO INTEGRACIÓN CON MÓDULOS")
    print("-" * 40)
    
    try:
        # Probar módulo desarrollo
        from noox_cli.modules.desarrollo import DesarrolloModule
        desarrollo = DesarrolloModule()
        
        wt_detected_dev = desarrollo._command_exists('wt')
        print(f"  Módulo desarrollo detecta WT: {'✅' if wt_detected_dev else '❌'}")
        
        # Probar módulo proyectos
        from noox_cli.modules.proyectos import ProyectosModule
        proyectos = ProyectosModule()
        
        wt_detected_proj = proyectos._command_exists('wt')
        print(f"  Módulo proyectos detecta WT: {'✅' if wt_detected_proj else '❌'}")
        
        # Verificar que las funciones de terminal existen
        dev_functions = [
            '_open_terminal',
            '_open_clean_terminal', 
            '_open_cmd_terminal'
        ]
        
        proj_functions = [
            '_open_terminal',
            '_open_clean_terminal',
            '_open_cmd_terminal'
        ]
        
        dev_functions_ok = all(hasattr(desarrollo, func) for func in dev_functions)
        proj_functions_ok = all(hasattr(proyectos, func) for func in proj_functions)
        
        print(f"  Funciones desarrollo: {'✅' if dev_functions_ok else '❌'}")
        print(f"  Funciones proyectos: {'✅' if proj_functions_ok else '❌'}")
        
        return wt_detected_dev and wt_detected_proj and dev_functions_ok and proj_functions_ok
        
    except Exception as e:
        print(f"  ❌ Error verificando integración: {e}")
        return False

def test_environment_info():
    """Muestra información del entorno actual."""
    print("\n📊 INFORMACIÓN DEL ENTORNO")
    print("-" * 40)
    
    env_vars = [
        'WT_SESSION',
        'WT_PROFILE_ID', 
        'TERM',
        'TERM_PROGRAM',
        'ConEmuPID',
        'SESSIONNAME'
    ]
    
    print("  🔍 Variables de entorno relevantes:")
    for var in env_vars:
        value = os.environ.get(var, 'No definida')
        print(f"    {var}: {value}")
    
    # Información adicional
    print(f"\n  💻 Sistema: {os.name}")
    print(f"  📁 Directorio actual: {Path.cwd()}")
    
    return True

def show_usage_recommendations():
    """Muestra recomendaciones de uso."""
    print("\n💡 RECOMENDACIONES DE USO")
    print("-" * 40)
    
    wt_session = os.environ.get('WT_SESSION')
    
    if wt_session:
        print("  🎉 ¡Perfecto! Estás ejecutando NooxCLI dentro de Windows Terminal")
        print("  📋 Comportamiento esperado:")
        print("    - Terminal normal: Nueva pestaña en Windows Terminal")
        print("    - Terminal limpio: Nueva pestaña sin perfil")
        print("    - CMD tradicional: Nueva pestaña con CMD")
        print("  ✨ Mantendrás todos tus iconos, colores y configuración")
    else:
        print("  ℹ️ No estás ejecutando desde Windows Terminal")
        print("  📋 Comportamiento esperado:")
        print("    - Se abrirá nueva ventana de Windows Terminal")
        print("    - O fallback a ventana separada si WT no está disponible")
        print("  💡 Para mejor experiencia, ejecuta NooxCLI desde Windows Terminal")

def main():
    """Función principal de las pruebas de Windows Terminal."""
    print("🖥️ PRUEBAS DE INTEGRACIÓN - WINDOWS TERMINAL")
    print("=" * 50)
    
    tests = [
        ("Detección de Windows Terminal", test_windows_terminal_detection),
        ("Sintaxis de comandos WT", test_wt_command_syntax),
        ("Integración con módulos", test_module_wt_integration),
        ("Información del entorno", test_environment_info)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append(False)
    
    # Mostrar recomendaciones
    show_usage_recommendations()
    
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
    
    if success_rate >= 0.75:
        print("🎉 ¡Integración con Windows Terminal funcionando correctamente!")
        print("💡 Los terminales se abrirán como pestañas en tu Windows Terminal")
        return 0
    else:
        print("⚠️ Problemas con la integración de Windows Terminal")
        print("💡 Se usarán ventanas separadas como fallback")
        return 1

if __name__ == '__main__':
    sys.exit(main())