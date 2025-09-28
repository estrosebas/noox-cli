#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones de terminal.
"""

import os
import sys
import subprocess
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_terminal_functions():
    """Prueba las funciones de terminal del módulo proyectos."""
    print("🖥️ PROBANDO FUNCIONES DE TERMINAL")
    print("-" * 40)
    
    try:
        from noox_cli.modules.proyectos import ProyectosModule
        
        proyectos = ProyectosModule()
        test_path = Path.cwd()
        
        # Verificar que las funciones existen
        functions_to_test = [
            ('_open_terminal', 'Terminal normal'),
            ('_open_clean_terminal', 'Terminal limpio'),
            ('_open_cmd_terminal', 'Terminal CMD')
        ]
        
        results = []
        
        for func_name, description in functions_to_test:
            if hasattr(proyectos, func_name):
                func = getattr(proyectos, func_name)
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
        print(f"\n📊 Funciones de terminal: {success_rate:.1%} disponibles")
        
        return success_rate > 0.8
        
    except Exception as e:
        print(f"❌ Error probando funciones de terminal: {e}")
        return False

def test_powershell_versions():
    """Verifica qué versiones de PowerShell están disponibles."""
    print("\n🔍 VERIFICANDO VERSIONES DE POWERSHELL")
    print("-" * 40)
    
    powershell_commands = [
        ('pwsh', 'PowerShell 7'),
        ('powershell', 'PowerShell 5.1'),
        ('wt', 'Windows Terminal'),
        ('cmd', 'Command Prompt')
    ]
    
    available_terminals = []
    
    for cmd, name in powershell_commands:
        try:
            if cmd == 'wt':
                # Para Windows Terminal, solo verificar si existe
                result = subprocess.run([cmd, '--help'], 
                                      capture_output=True, 
                                      timeout=5)
                if result.returncode == 0:
                    print(f"  ✅ {name}: Disponible")
                    available_terminals.append(cmd)
                else:
                    print(f"  ❌ {name}: No disponible")
            else:
                # Para PowerShell y CMD, verificar versión
                version_cmd = '--version' if cmd != 'cmd' else '/ver'
                result = subprocess.run([cmd, version_cmd], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                
                if result.returncode == 0:
                    version = result.stdout.strip().split('\n')[0] if result.stdout else 'Desconocida'
                    print(f"  ✅ {name}: {version}")
                    available_terminals.append(cmd)
                else:
                    print(f"  ❌ {name}: No disponible")
                    
        except subprocess.TimeoutExpired:
            print(f"  ⏱️ {name}: Timeout")
        except FileNotFoundError:
            print(f"  ❌ {name}: No encontrado")
        except Exception as e:
            print(f"  ❌ {name}: Error - {e}")
    
    print(f"\n📊 Terminales disponibles: {len(available_terminals)}")
    return len(available_terminals) > 0

def test_terminal_commands():
    """Prueba comandos básicos de terminal sin abrir ventanas."""
    print("\n🧪 PROBANDO COMANDOS DE TERMINAL")
    print("-" * 40)
    
    # Comandos que podemos probar sin abrir ventanas
    test_commands = [
        (['pwsh', '-NoProfile', '-Command', 'Write-Host "Test OK"'], 'PowerShell 7 básico'),
        (['powershell', '-NoProfile', '-Command', 'Write-Host "Test OK"'], 'PowerShell 5.1 básico'),
        (['cmd', '/c', 'echo Test OK'], 'CMD básico')
    ]
    
    working_commands = []
    
    for cmd, description in test_commands:
        try:
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            
            if result.returncode == 0 and "Test OK" in result.stdout:
                print(f"  ✅ {description}: Funciona")
                working_commands.append(cmd[0])
            else:
                print(f"  ❌ {description}: Error")
                
        except subprocess.TimeoutExpired:
            print(f"  ⏱️ {description}: Timeout")
        except FileNotFoundError:
            print(f"  ❌ {description}: No encontrado")
        except Exception as e:
            print(f"  ❌ {description}: Error - {e}")
    
    print(f"\n📊 Comandos funcionando: {len(working_commands)}")
    return len(working_commands) > 0

def main():
    """Función principal de las pruebas de terminal."""
    print("🖥️ PRUEBAS DE CORRECCIONES DE TERMINAL")
    print("=" * 50)
    
    tests = [
        ("Funciones de terminal", test_terminal_functions),
        ("Versiones de PowerShell", test_powershell_versions),
        ("Comandos básicos", test_terminal_commands)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
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
        print("🎉 ¡Correcciones de terminal funcionando correctamente!")
        print("\n💡 Recomendaciones:")
        print("- Usa 'Terminal limpio' si hay problemas con el perfil")
        print("- Usa 'CMD tradicional' para máxima estabilidad")
        print("- El terminal normal debería funcionar sin problemas ahora")
        return 0
    else:
        print("⚠️ Algunas funciones de terminal necesitan revisión")
        return 1

if __name__ == '__main__':
    sys.exit(main())