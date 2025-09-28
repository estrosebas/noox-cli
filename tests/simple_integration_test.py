#!/usr/bin/env python3
"""
Pruebas de integración simplificadas para NooxCLI.
Evita problemas de codificación Unicode en consolas Windows.
"""

import os
import sys
import platform
import tempfile
import shutil
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_module_initialization():
    """Prueba la inicialización de todos los módulos."""
    print("Probando inicialización de módulos...")
    
    try:
        from noox_cli.modules import sistema, reparar, test_utf8, config
        from noox_cli.menu import NooxMenu
        
        # Probar inicialización de cada módulo
        modules = {
            'Sistema': sistema.SistemaModule,
            'Reparar': reparar.RepararModule,
            'Test UTF-8': test_utf8.TestUtf8Module,
            'Config': config.ConfigModule
        }
        
        results = []
        
        for name, module_class in modules.items():
            try:
                instance = module_class()
                print(f"  OK - {name} inicializado correctamente")
                
                # Verificar métodos requeridos
                if hasattr(instance, 'main') and hasattr(instance, '_handle_selection'):
                    print(f"  OK - {name} tiene métodos requeridos")
                    results.append(True)
                else:
                    print(f"  ERROR - {name} falta métodos requeridos")
                    results.append(False)
                    
            except Exception as e:
                print(f"  ERROR - {name}: {e}")
                results.append(False)
        
        success_rate = sum(results) / len(results)
        print(f"Inicialización: {success_rate:.1%} exitosa")
        return success_rate > 0.8
        
    except Exception as e:
        print(f"Error en prueba de inicialización: {e}")
        return False

def test_basic_functionality():
    """Prueba funcionalidad básica de cada módulo."""
    print("Probando funcionalidad básica...")
    
    try:
        from noox_cli.modules import sistema, reparar, test_utf8, config
        
        results = []
        
        # Probar módulo sistema
        try:
            sistema_module = sistema.SistemaModule()
            info = sistema_module._get_system_info_fallback()
            if info and info.hostname:
                print("  OK - Sistema: obtención de información")
                results.append(True)
            else:
                print("  ERROR - Sistema: no se pudo obtener información")
                results.append(False)
        except Exception as e:
            print(f"  ERROR - Sistema: {e}")
            results.append(False)
        
        # Probar módulo reparar
        try:
            reparar_module = reparar.RepararModule()
            content = reparar_module._get_profile_content()
            if content and len(content) > 100:
                print("  OK - Reparar: generación de perfil")
                results.append(True)
            else:
                print("  ERROR - Reparar: problema generando perfil")
                results.append(False)
        except Exception as e:
            print(f"  ERROR - Reparar: {e}")
            results.append(False)
        
        # Probar módulo test_utf8
        try:
            utf8_module = test_utf8.TestUtf8Module()
            color_support = utf8_module._check_color_support()
            print(f"  OK - Test UTF-8: verificación de colores (soporte: {color_support})")
            results.append(True)
        except Exception as e:
            print(f"  ERROR - Test UTF-8: {e}")
            results.append(False)
        
        # Probar módulo config
        try:
            config_module = config.ConfigModule()
            codepage = config_module._get_current_codepage()
            if codepage and codepage != "Desconocido":
                print(f"  OK - Config: página de códigos ({codepage})")
                results.append(True)
            else:
                print("  ERROR - Config: no se pudo obtener página de códigos")
                results.append(False)
        except Exception as e:
            print(f"  ERROR - Config: {e}")
            results.append(False)
        
        success_rate = sum(results) / len(results)
        print(f"Funcionalidad básica: {success_rate:.1%} exitosa")
        return success_rate > 0.75
        
    except Exception as e:
        print(f"Error en prueba de funcionalidad: {e}")
        return False

def test_error_handling():
    """Prueba el manejo de errores."""
    print("Probando manejo de errores...")
    
    try:
        from noox_cli.modules import sistema, reparar, config
        
        results = []
        
        # Probar manejo de errores en sistema
        try:
            sistema_module = sistema.SistemaModule()
            # Probar con datos inválidos
            result = sistema_module._parse_memory_string("invalid_data")
            if result == 0:  # Debe retornar 0 para datos inválidos
                print("  OK - Sistema: manejo de datos inválidos")
                results.append(True)
            else:
                print("  ERROR - Sistema: no maneja datos inválidos correctamente")
                results.append(False)
        except Exception as e:
            print(f"  ERROR - Sistema manejo de errores: {e}")
            results.append(False)
        
        # Probar manejo de errores en reparar
        try:
            reparar_module = reparar.RepararModule()
            # Configurar ruta inexistente
            reparar_module.profile_path = Path("/ruta/inexistente/perfil.ps1")
            backup_result = reparar_module._backup_profile()
            if backup_result is None:  # Debe retornar None para archivos inexistentes
                print("  OK - Reparar: manejo de archivos inexistentes")
                results.append(True)
            else:
                print("  ERROR - Reparar: no maneja archivos inexistentes")
                results.append(False)
        except Exception as e:
            print(f"  ERROR - Reparar manejo de errores: {e}")
            results.append(False)
        
        # Probar manejo de errores en config
        try:
            config_module = config.ConfigModule()
            # Esto debe funcionar sin errores incluso sin permisos especiales
            reg_config = config_module._get_registry_config()
            if isinstance(reg_config, dict):
                print("  OK - Config: manejo de acceso al registro")
                results.append(True)
            else:
                print("  ERROR - Config: problema con acceso al registro")
                results.append(False)
        except Exception as e:
            print(f"  ERROR - Config manejo de errores: {e}")
            results.append(False)
        
        success_rate = sum(results) / len(results)
        print(f"Manejo de errores: {success_rate:.1%} exitoso")
        return success_rate > 0.7
        
    except Exception as e:
        print(f"Error en prueba de manejo de errores: {e}")
        return False

def test_cross_module_consistency():
    """Prueba la consistencia entre módulos."""
    print("Probando consistencia entre módulos...")
    
    try:
        from noox_cli.modules import sistema, reparar, test_utf8, config
        from noox_cli.menu import NooxMenu
        
        modules = {
            'sistema': sistema.SistemaModule(),
            'reparar': reparar.RepararModule(),
            'test_utf8': test_utf8.TestUtf8Module(),
            'config': config.ConfigModule()
        }
        
        results = []
        
        # Verificar que todos tengan menu
        for name, module in modules.items():
            if hasattr(module, 'menu') and isinstance(module.menu, NooxMenu):
                print(f"  OK - {name}: tiene objeto menu correcto")
                results.append(True)
            else:
                print(f"  ERROR - {name}: menu incorrecto o faltante")
                results.append(False)
        
        # Verificar títulos de menu consistentes
        expected_titles = {
            'sistema': "Sistema - NooxCLI",
            'reparar': "Reparación - NooxCLI",
            'test_utf8': "Test UTF-8 - NooxCLI",
            'config': "Configuración - NooxCLI"
        }
        
        for name, expected_title in expected_titles.items():
            if modules[name].menu.title == expected_title:
                print(f"  OK - {name}: título correcto")
                results.append(True)
            else:
                print(f"  ERROR - {name}: título incorrecto")
                results.append(False)
        
        success_rate = sum(results) / len(results)
        print(f"Consistencia: {success_rate:.1%} exitosa")
        return success_rate > 0.9
        
    except Exception as e:
        print(f"Error en prueba de consistencia: {e}")
        return False

def main():
    """Función principal de las pruebas simplificadas."""
    print("PRUEBAS DE INTEGRACIÓN SIMPLIFICADAS - NooxCLI")
    print("=" * 50)
    
    # Configurar UTF-8 en Windows
    if platform.system() == "Windows":
        os.system('chcp 65001 > nul')
    
    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print()
    
    # Ejecutar pruebas
    tests = [
        ("Inicialización de módulos", test_module_initialization),
        ("Funcionalidad básica", test_basic_functionality),
        ("Manejo de errores", test_error_handling),
        ("Consistencia entre módulos", test_cross_module_consistency)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"--- {test_name} ---")
        try:
            result = test_func()
            results.append(result)
            status = "PASS" if result else "FAIL"
            print(f"Resultado: {status}")
        except Exception as e:
            print(f"ERROR: {e}")
            results.append(False)
        print()
    
    # Resumen final
    print("RESUMEN FINAL")
    print("-" * 30)
    
    passed = sum(results)
    total = len(results)
    success_rate = passed / total if total > 0 else 0
    
    for i, (test_name, _) in enumerate(tests):
        status = "PASS" if results[i] else "FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nPuntuación general: {success_rate:.1%} ({passed}/{total})")
    
    if success_rate >= 0.9:
        print("EXCELENTE - Todos los módulos funcionan correctamente")
        return 0
    elif success_rate >= 0.8:
        print("BUENO - La mayoría de funcionalidades están OK")
        return 0
    elif success_rate >= 0.7:
        print("ACEPTABLE - Algunos problemas menores")
        return 1
    else:
        print("NECESITA TRABAJO - Problemas significativos detectados")
        return 1

if __name__ == '__main__':
    sys.exit(main())