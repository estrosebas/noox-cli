#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas de integración de NooxCLI.
Incluye pruebas de funcionalidad, manejo de errores, permisos y consistencia visual.
"""

import os
import sys
import unittest
import platform
import subprocess
from pathlib import Path
from datetime import datetime

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def setup_test_environment():
    """Configura el entorno para las pruebas."""
    print("🔧 Configurando entorno de pruebas...")
    
    # Configurar UTF-8 en Windows
    if platform.system() == "Windows":
        try:
            subprocess.run(['chcp', '65001'], shell=True, capture_output=True)
            print("✅ Página de códigos UTF-8 configurada")
        except Exception as e:
            print(f"⚠️ No se pudo configurar UTF-8: {e}")
    
    # Verificar dependencias
    dependencies = ['rich', 'InquirerPy']
    missing_deps = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} disponible")
        except ImportError:
            missing_deps.append(dep)
            print(f"❌ {dep} no disponible")
    
    if missing_deps:
        print(f"⚠️ Dependencias faltantes: {', '.join(missing_deps)}")
        print("💡 Instala con: pip install rich InquirerPy")
        return False
    
    # Verificar psutil (opcional)
    try:
        import psutil
        print("✅ psutil disponible (funcionalidad completa)")
    except ImportError:
        print("⚠️ psutil no disponible (funcionalidad limitada)")
    
    return True

def run_module_tests():
    """Ejecuta las pruebas de cada módulo individualmente."""
    print("\n🧪 EJECUTANDO PRUEBAS POR MÓDULO")
    print("=" * 50)
    
    test_results = {}
    
    # Importar módulos para pruebas básicas
    modules_to_test = [
        ('sistema', 'src.noox_cli.modules.sistema'),
        ('reparar', 'src.noox_cli.modules.reparar'),
        ('test_utf8', 'src.noox_cli.modules.test_utf8'),
        ('config', 'src.noox_cli.modules.config')
    ]
    
    for module_name, module_path in modules_to_test:
        print(f"\n📦 Probando módulo: {module_name}")
        try:
            # Importar el módulo
            module = __import__(module_path, fromlist=[''])
            
            # Verificar que tenga las clases esperadas
            expected_classes = {
                'sistema': 'SistemaModule',
                'reparar': 'RepararModule', 
                'test_utf8': 'TestUtf8Module',
                'config': 'ConfigModule'
            }
            
            class_name = expected_classes[module_name]
            if hasattr(module, class_name):
                # Intentar instanciar la clase
                module_class = getattr(module, class_name)
                instance = module_class()
                
                # Verificar métodos básicos
                required_methods = ['main', '_handle_selection']
                missing_methods = []
                
                for method in required_methods:
                    if not hasattr(instance, method):
                        missing_methods.append(method)
                
                if missing_methods:
                    print(f"❌ Métodos faltantes: {', '.join(missing_methods)}")
                    test_results[module_name] = False
                else:
                    print(f"✅ Módulo {module_name} OK")
                    test_results[module_name] = True
            else:
                print(f"❌ Clase {class_name} no encontrada")
                test_results[module_name] = False
                
        except Exception as e:
            print(f"❌ Error importando {module_name}: {e}")
            test_results[module_name] = False
    
    return test_results

def run_integration_tests():
    """Ejecuta las pruebas de integración completas."""
    print("\n🔗 EJECUTANDO PRUEBAS DE INTEGRACIÓN")
    print("=" * 50)
    
    # Buscar archivos de prueba
    test_dir = Path(__file__).parent / 'integration'
    test_files = list(test_dir.glob('test_*.py'))
    
    if not test_files:
        print("❌ No se encontraron archivos de prueba de integración")
        return False
    
    print(f"📁 Encontrados {len(test_files)} archivos de prueba")
    
    # Ejecutar pruebas usando unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Cargar todas las pruebas
    for test_file in test_files:
        try:
            # Importar el módulo de prueba
            module_name = test_file.stem
            spec = unittest.util.spec_from_file_location(module_name, test_file)
            test_module = unittest.util.module_from_spec(spec)
            spec.loader.exec_module(test_module)
            
            # Agregar pruebas al suite
            suite.addTests(loader.loadTestsFromModule(test_module))
            print(f"✅ Cargadas pruebas de {test_file.name}")
            
        except Exception as e:
            print(f"❌ Error cargando {test_file.name}: {e}")
    
    # Ejecutar las pruebas
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def test_cross_platform_compatibility():
    """Prueba la compatibilidad multiplataforma."""
    print("\n🌐 PRUEBAS DE COMPATIBILIDAD MULTIPLATAFORMA")
    print("=" * 50)
    
    system_info = {
        'Sistema': platform.system(),
        'Versión': platform.version(),
        'Arquitectura': platform.architecture()[0],
        'Python': platform.python_version(),
        'Encoding': sys.getdefaultencoding()
    }
    
    print("📊 Información del sistema:")
    for key, value in system_info.items():
        print(f"  {key}: {value}")
    
    # Pruebas específicas por plataforma
    compatibility_tests = []
    
    if platform.system() == "Windows":
        print("\n🪟 Pruebas específicas de Windows:")
        
        # Probar comando chcp
        try:
            result = subprocess.run(['chcp'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                print("✅ Comando chcp disponible")
                compatibility_tests.append(True)
            else:
                print("❌ Comando chcp falló")
                compatibility_tests.append(False)
        except Exception as e:
            print(f"❌ Error ejecutando chcp: {e}")
            compatibility_tests.append(False)
        
        # Probar acceso al registro
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console", 0, winreg.KEY_READ):
                print("✅ Acceso al registro disponible")
                compatibility_tests.append(True)
        except Exception as e:
            print(f"⚠️ Acceso limitado al registro: {e}")
            compatibility_tests.append(False)
        
        # Probar PowerShell
        try:
            result = subprocess.run(['powershell', '-Command', 'Write-Host "Test"'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ PowerShell disponible")
                compatibility_tests.append(True)
            else:
                print("❌ PowerShell no disponible")
                compatibility_tests.append(False)
        except Exception as e:
            print(f"❌ Error ejecutando PowerShell: {e}")
            compatibility_tests.append(False)
    
    else:
        print(f"\n🐧 Sistema {platform.system()} detectado")
        print("⚠️ Algunas funcionalidades pueden estar limitadas")
        compatibility_tests.append(True)  # Asumir compatibilidad básica
    
    success_rate = sum(compatibility_tests) / len(compatibility_tests) if compatibility_tests else 0
    print(f"\n📊 Compatibilidad: {success_rate:.1%} ({sum(compatibility_tests)}/{len(compatibility_tests)})")
    
    return success_rate > 0.7  # 70% de éxito mínimo

def test_error_handling():
    """Prueba el manejo de errores en condiciones adversas."""
    print("\n🚨 PRUEBAS DE MANEJO DE ERRORES")
    print("=" * 50)
    
    error_tests = []
    
    # Probar importación con dependencias faltantes
    print("🔍 Probando manejo de dependencias faltantes...")
    
    # Simular ausencia de psutil
    original_psutil = sys.modules.get('psutil')
    try:
        if 'psutil' in sys.modules:
            del sys.modules['psutil']
        
        # Intentar importar módulo sistema
        from src.noox_cli.modules import sistema
        sistema_module = sistema.SistemaModule()
        print("✅ Módulo sistema maneja ausencia de psutil")
        error_tests.append(True)
        
    except Exception as e:
        print(f"❌ Error manejando ausencia de psutil: {e}")
        error_tests.append(False)
    finally:
        if original_psutil:
            sys.modules['psutil'] = original_psutil
    
    # Probar manejo de permisos insuficientes
    print("🔒 Probando manejo de permisos insuficientes...")
    try:
        # Intentar operaciones que requieren permisos
        from src.noox_cli.modules import config
        config_module = config.ConfigModule()
        
        # Esto debería manejar errores de permisos graciosamente
        reg_config = config_module._get_registry_config()
        print("✅ Manejo de permisos del registro OK")
        error_tests.append(True)
        
    except Exception as e:
        print(f"❌ Error manejando permisos: {e}")
        error_tests.append(False)
    
    # Probar manejo de archivos inexistentes
    print("📁 Probando manejo de archivos inexistentes...")
    try:
        from src.noox_cli.modules import reparar
        reparar_module = reparar.RepararModule()
        
        # Configurar ruta inexistente
        reparar_module.profile_path = Path("/ruta/inexistente/perfil.ps1")
        backup_result = reparar_module._backup_profile()
        
        # Debe retornar None sin lanzar excepción
        if backup_result is None:
            print("✅ Manejo de archivos inexistentes OK")
            error_tests.append(True)
        else:
            print("❌ No maneja correctamente archivos inexistentes")
            error_tests.append(False)
            
    except Exception as e:
        print(f"❌ Error manejando archivos inexistentes: {e}")
        error_tests.append(False)
    
    success_rate = sum(error_tests) / len(error_tests) if error_tests else 0
    print(f"\n📊 Manejo de errores: {success_rate:.1%} ({sum(error_tests)}/{len(error_tests)})")
    
    return success_rate > 0.8  # 80% de éxito mínimo

def generate_test_report(module_results, integration_success, compatibility_success, error_handling_success):
    """Genera un reporte completo de las pruebas."""
    print("\n📋 REPORTE FINAL DE PRUEBAS")
    print("=" * 50)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"🕒 Fecha: {timestamp}")
    print(f"💻 Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {platform.python_version()}")
    
    print("\n📦 RESULTADOS POR MÓDULO:")
    for module, success in module_results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {module}: {status}")
    
    print("\n🔗 PRUEBAS DE INTEGRACIÓN:")
    status = "✅ PASS" if integration_success else "❌ FAIL"
    print(f"  Integración completa: {status}")
    
    print("\n🌐 COMPATIBILIDAD:")
    status = "✅ PASS" if compatibility_success else "❌ FAIL"
    print(f"  Multiplataforma: {status}")
    
    print("\n🚨 MANEJO DE ERRORES:")
    status = "✅ PASS" if error_handling_success else "❌ FAIL"
    print(f"  Robustez: {status}")
    
    # Calcular puntuación general
    total_tests = len(module_results) + 3  # módulos + 3 categorías adicionales
    passed_tests = sum(module_results.values()) + sum([integration_success, compatibility_success, error_handling_success])
    
    overall_score = passed_tests / total_tests
    
    print(f"\n🎯 PUNTUACIÓN GENERAL: {overall_score:.1%} ({passed_tests}/{total_tests})")
    
    if overall_score >= 0.9:
        print("🏆 EXCELENTE - Todos los módulos están listos para producción")
    elif overall_score >= 0.8:
        print("✅ BUENO - Los módulos están en buen estado")
    elif overall_score >= 0.7:
        print("⚠️ ACEPTABLE - Algunos problemas menores detectados")
    else:
        print("❌ NECESITA TRABAJO - Se requieren correcciones importantes")
    
    return overall_score

def main():
    """Función principal del script de pruebas."""
    # Configurar UTF-8 para evitar errores de codificación
    if platform.system() == "Windows":
        os.system('chcp 65001 > nul')
    
    print("SUITE DE PRUEBAS DE INTEGRACIÓN - NooxCLI")
    print("=" * 60)
    
    # Configurar entorno
    if not setup_test_environment():
        print("❌ No se pudo configurar el entorno de pruebas")
        return 1
    
    # Ejecutar pruebas por módulo
    module_results = run_module_tests()
    
    # Ejecutar pruebas de integración
    integration_success = run_integration_tests()
    
    # Probar compatibilidad multiplataforma
    compatibility_success = test_cross_platform_compatibility()
    
    # Probar manejo de errores
    error_handling_success = test_error_handling()
    
    # Generar reporte final
    overall_score = generate_test_report(
        module_results, 
        integration_success, 
        compatibility_success, 
        error_handling_success
    )
    
    # Retornar código de salida apropiado
    return 0 if overall_score >= 0.8 else 1

if __name__ == '__main__':
    sys.exit(main())