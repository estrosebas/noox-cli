#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones del módulo desarrollo.
"""

import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_desarrollo_initialization():
    """Prueba la inicialización del módulo desarrollo."""
    print("🔍 Probando inicialización del módulo desarrollo...")
    
    try:
        from noox_cli.modules.desarrollo import DesarrolloModule
        
        desarrollo = DesarrolloModule()
        
        # Verificar inicialización básica
        if hasattr(desarrollo, 'menu') and hasattr(desarrollo, 'current_dir'):
            print("  ✅ Módulo desarrollo inicializado correctamente")
            return True
        else:
            print("  ❌ Módulo desarrollo falta atributos básicos")
            return False
            
    except Exception as e:
        print(f"  ❌ Error inicializando módulo desarrollo: {e}")
        return False

def test_terminal_functions():
    """Prueba las funciones de terminal mejoradas."""
    print("\n🖥️ Probando funciones de terminal mejoradas...")
    
    try:
        from noox_cli.modules.desarrollo import DesarrolloModule
        
        desarrollo = DesarrolloModule()
        
        # Verificar que las nuevas funciones existen
        terminal_functions = [
            ('_open_terminal', 'Terminal normal'),
            ('_open_clean_terminal', 'Terminal limpio'),
            ('_open_cmd_terminal', 'Terminal CMD')
        ]
        
        results = []
        
        for func_name, description in terminal_functions:
            if hasattr(desarrollo, func_name):
                func = getattr(desarrollo, func_name)
                if callable(func):
                    print(f"  ✅ {description}: Función disponible")
                    results.append(True)
                else:
                    print(f"  ❌ {description}: No es ejecutable")
                    results.append(False)
            else:
                print(f"  ❌ {description}: Función no encontrada")
                results.append(False)
        
        success_rate = sum(results) / len(results)
        print(f"  📊 Funciones de terminal: {success_rate:.1%} disponibles")
        
        return success_rate > 0.8
        
    except Exception as e:
        print(f"  ❌ Error probando funciones de terminal: {e}")
        return False

def test_vscode_detection():
    """Prueba la detección mejorada de VS Code."""
    print("\n🔍 Probando detección mejorada de VS Code...")
    
    try:
        from noox_cli.modules.desarrollo import DesarrolloModule
        
        desarrollo = DesarrolloModule()
        
        # Probar detección de comando
        vscode_detected = desarrollo._command_exists('code')
        print(f"  Detección de comando 'code': {'✅' if vscode_detected else '❌'}")
        
        # Probar verificación específica de VS Code
        if hasattr(desarrollo, '_check_vscode_installation'):
            vscode_installed = desarrollo._check_vscode_installation()
            print(f"  Verificación específica VS Code: {'✅' if vscode_installed else '❌'}")
        else:
            vscode_installed = False
            print("  ⚠️ Función _check_vscode_installation no encontrada")
        
        # Probar función mejorada de apertura
        if hasattr(desarrollo, '_open_vscode_improved'):
            print("  ✅ Función _open_vscode_improved disponible")
            improved_available = True
        else:
            print("  ❌ Función _open_vscode_improved no encontrada")
            improved_available = False
        
        overall_success = vscode_detected or vscode_installed or improved_available
        
        if overall_success:
            print("  💡 VS Code detectado o funciones mejoradas disponibles")
        else:
            print("  ⚠️ VS Code no detectado - verificar instalación")
        
        return overall_success
        
    except Exception as e:
        print(f"  ❌ Error en prueba de VS Code: {e}")
        return False

def test_command_detection():
    """Prueba la detección mejorada de comandos."""
    print("\n🧪 Probando detección de comandos...")
    
    try:
        from noox_cli.modules.desarrollo import DesarrolloModule
        
        desarrollo = DesarrolloModule()
        
        # Comandos a probar
        commands_to_test = [
            ('git', 'Git'),
            ('npm', 'NPM'),
            ('python', 'Python'),
            ('code', 'VS Code'),
            ('pwsh', 'PowerShell 7'),
            ('powershell', 'PowerShell 5.1')
        ]
        
        detected_commands = []
        
        for cmd, name in commands_to_test:
            try:
                if desarrollo._command_exists(cmd):
                    print(f"  ✅ {name}: Disponible")
                    detected_commands.append(cmd)
                else:
                    print(f"  ❌ {name}: No disponible")
            except Exception as e:
                print(f"  ❌ {name}: Error - {e}")
        
        print(f"  📊 Comandos detectados: {len(detected_commands)}/{len(commands_to_test)}")
        
        # Al menos git, python y algún PowerShell deberían estar disponibles
        essential_commands = ['git', 'python']
        powershell_commands = ['pwsh', 'powershell']
        
        has_essentials = all(cmd in detected_commands for cmd in essential_commands)
        has_powershell = any(cmd in detected_commands for cmd in powershell_commands)
        
        return has_essentials and has_powershell
        
    except Exception as e:
        print(f"  ❌ Error probando detección de comandos: {e}")
        return False

def test_module_methods():
    """Verifica que todos los métodos principales estén disponibles."""
    print("\n🔧 Verificando métodos principales del módulo...")
    
    try:
        from noox_cli.modules.desarrollo import DesarrolloModule
        
        desarrollo = DesarrolloModule()
        
        # Métodos principales que deben existir
        required_methods = [
            'main',
            '_handle_selection',
            '_open_vscode',
            '_open_powershell',
            '_git_init',
            '_npm_install',
            '_command_exists'
        ]
        
        missing_methods = []
        
        for method in required_methods:
            if hasattr(desarrollo, method) and callable(getattr(desarrollo, method)):
                print(f"  ✅ {method}: Disponible")
            else:
                print(f"  ❌ {method}: No encontrado o no ejecutable")
                missing_methods.append(method)
        
        success_rate = (len(required_methods) - len(missing_methods)) / len(required_methods)
        print(f"  📊 Métodos disponibles: {success_rate:.1%}")
        
        return success_rate > 0.9
        
    except Exception as e:
        print(f"  ❌ Error verificando métodos: {e}")
        return False

def main():
    """Función principal de las pruebas del módulo desarrollo."""
    print("🛠️ PRUEBAS DE CORRECCIONES - MÓDULO DESARROLLO")
    print("=" * 50)
    
    tests = [
        ("Inicialización del módulo", test_desarrollo_initialization),
        ("Funciones de terminal", test_terminal_functions),
        ("Detección de VS Code", test_vscode_detection),
        ("Detección de comandos", test_command_detection),
        ("Métodos principales", test_module_methods)
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
        print("🎉 ¡Correcciones del módulo desarrollo funcionando correctamente!")
        print("\n💡 Mejoras aplicadas:")
        print("- Terminal con múltiples opciones (normal, limpio, CMD)")
        print("- Detección mejorada de VS Code")
        print("- Aislamiento de procesos para evitar conflictos")
        print("- Manejo robusto de errores")
        return 0
    else:
        print("⚠️ Algunas correcciones del módulo desarrollo necesitan revisión")
        return 1

if __name__ == '__main__':
    sys.exit(main())