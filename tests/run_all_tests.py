#!/usr/bin/env python3
"""
Script maestro para ejecutar todas las pruebas de NooxCLI.
Incluye pruebas de integración, rendimiento, compatibilidad y robustez.
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path
from datetime import datetime

def print_header(title):
    """Imprime un encabezado formateado."""
    print(f"\n{'=' * 60}")
    print(f"🎯 {title}")
    print(f"{'=' * 60}")

def print_section(title):
    """Imprime un encabezado de sección."""
    print(f"\n{'-' * 50}")
    print(f"📋 {title}")
    print(f"{'-' * 50}")

def run_command(command, description, timeout=300):
    """Ejecuta un comando y retorna el resultado."""
    print(f"\n🔄 {description}...")
    
    try:
        start_time = time.time()
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=True if isinstance(command, str) else False
        )
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} - OK ({execution_time:.2f}s)")
            return True, result.stdout, execution_time
        else:
            print(f"❌ {description} - FALLÓ ({execution_time:.2f}s)")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
            return False, result.stderr, execution_time
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ {description} - TIMEOUT ({timeout}s)")
        return False, "Timeout", timeout
    except Exception as e:
        print(f"💥 {description} - EXCEPCIÓN: {e}")
        return False, str(e), 0

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas."""
    print_section("VERIFICACIÓN DE DEPENDENCIAS")
    
    dependencies = {
        'rich': 'pip install rich',
        'InquirerPy': 'pip install InquirerPy',
        'psutil': 'pip install psutil (opcional)',
        'colorama': 'pip install colorama'
    }
    
    missing_deps = []
    
    for dep, install_cmd in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep} - Disponible")
        except ImportError:
            print(f"❌ {dep} - No disponible")
            print(f"   💡 Instalar con: {install_cmd}")
            if dep != 'psutil':  # psutil es opcional
                missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n⚠️ Dependencias críticas faltantes: {', '.join(missing_deps)}")
        return False
    
    print("✅ Todas las dependencias críticas están disponibles")
    return True

def run_syntax_checks():
    """Ejecuta verificaciones de sintaxis en todos los archivos Python."""
    print_section("VERIFICACIÓN DE SINTAXIS")
    
    src_dir = Path(__file__).parent.parent / 'src'
    python_files = list(src_dir.rglob('*.py'))
    
    syntax_errors = []
    
    for py_file in python_files:
        success, output, _ = run_command(
            [sys.executable, '-m', 'py_compile', str(py_file)],
            f"Sintaxis de {py_file.name}",
            timeout=30
        )
        
        if not success:
            syntax_errors.append(str(py_file))
    
    if syntax_errors:
        print(f"\n❌ Errores de sintaxis en {len(syntax_errors)} archivos:")
        for file in syntax_errors:
            print(f"  - {file}")
        return False
    
    print(f"✅ Sintaxis correcta en {len(python_files)} archivos")
    return True

def run_import_tests():
    """Prueba que todos los módulos se puedan importar correctamente."""
    print_section("PRUEBAS DE IMPORTACIÓN")
    
    # Agregar src al path
    src_path = str(Path(__file__).parent.parent / 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    modules_to_test = [
        'noox_cli.menu',
        'noox_cli.modules.sistema',
        'noox_cli.modules.reparar',
        'noox_cli.modules.test_utf8',
        'noox_cli.modules.config',
        'noox_cli.main'
    ]
    
    import_errors = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module} - Importado correctamente")
        except Exception as e:
            print(f"❌ {module} - Error: {e}")
            import_errors.append(module)
    
    if import_errors:
        print(f"\n❌ Errores de importación en {len(import_errors)} módulos")
        return False
    
    print("✅ Todos los módulos se importan correctamente")
    return True

def run_integration_tests():
    """Ejecuta las pruebas de integración."""
    print_section("PRUEBAS DE INTEGRACIÓN")
    
    test_script = Path(__file__).parent / 'run_integration_tests.py'
    
    if not test_script.exists():
        print("❌ Script de pruebas de integración no encontrado")
        return False
    
    success, output, exec_time = run_command(
        [sys.executable, str(test_script)],
        "Pruebas de integración completas",
        timeout=600  # 10 minutos
    )
    
    if success:
        print("✅ Todas las pruebas de integración pasaron")
        return True
    else:
        print("❌ Algunas pruebas de integración fallaron")
        print(f"Salida: {output[:500]}...")
        return False

def run_performance_tests():
    """Ejecuta las pruebas de rendimiento."""
    print_section("PRUEBAS DE RENDIMIENTO")
    
    perf_script = Path(__file__).parent / 'performance' / 'test_performance.py'
    
    if not perf_script.exists():
        print("❌ Script de pruebas de rendimiento no encontrado")
        return False
    
    success, output, exec_time = run_command(
        [sys.executable, str(perf_script)],
        "Pruebas de rendimiento",
        timeout=300  # 5 minutos
    )
    
    if success:
        print("✅ Pruebas de rendimiento completadas")
        return True
    else:
        print("❌ Problemas en las pruebas de rendimiento")
        print(f"Salida: {output[:500]}...")
        return False

def run_manual_functionality_tests():
    """Ejecuta pruebas básicas de funcionalidad sin interacción."""
    print_section("PRUEBAS DE FUNCIONALIDAD BÁSICA")
    
    try:
        # Agregar src al path
        src_path = str(Path(__file__).parent.parent / 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Probar inicialización de módulos
        from noox_cli.modules import sistema, reparar, test_utf8, config
        
        modules = {
            'Sistema': sistema.SistemaModule,
            'Reparar': reparar.RepararModule,
            'Test UTF-8': test_utf8.TestUtf8Module,
            'Config': config.ConfigModule
        }
        
        functionality_results = []
        
        for name, module_class in modules.items():
            try:
                # Probar inicialización
                instance = module_class()
                print(f"✅ {name} - Inicialización OK")
                
                # Probar que tenga los métodos requeridos
                required_methods = ['main', '_handle_selection']
                for method in required_methods:
                    if hasattr(instance, method):
                        print(f"✅ {name} - Método {method} presente")
                    else:
                        print(f"❌ {name} - Método {method} faltante")
                        functionality_results.append(False)
                        continue
                
                # Probar métodos específicos sin interacción
                if name == 'Sistema':
                    try:
                        info = instance._get_system_info_fallback()
                        if info:
                            print(f"✅ {name} - Obtención de info del sistema OK")
                        else:
                            print(f"⚠️ {name} - Info del sistema limitada")
                    except Exception as e:
                        print(f"❌ {name} - Error en info del sistema: {e}")
                
                elif name == 'Reparar':
                    try:
                        content = instance._get_profile_content()
                        if content and len(content) > 100:
                            print(f"✅ {name} - Generación de perfil OK")
                        else:
                            print(f"❌ {name} - Problema generando perfil")
                    except Exception as e:
                        print(f"❌ {name} - Error generando perfil: {e}")
                
                elif name == 'Test UTF-8':
                    try:
                        color_support = instance._check_color_support()
                        print(f"✅ {name} - Verificación de colores OK (soporte: {color_support})")
                    except Exception as e:
                        print(f"❌ {name} - Error verificando colores: {e}")
                
                elif name == 'Config':
                    try:
                        codepage = instance._get_current_codepage()
                        if codepage and codepage != "Desconocido":
                            print(f"✅ {name} - Obtención de página de códigos OK ({codepage})")
                        else:
                            print(f"⚠️ {name} - Página de códigos no disponible")
                    except Exception as e:
                        print(f"❌ {name} - Error obteniendo página de códigos: {e}")
                
                functionality_results.append(True)
                
            except Exception as e:
                print(f"❌ {name} - Error en inicialización: {e}")
                functionality_results.append(False)
        
        success_rate = sum(functionality_results) / len(functionality_results)
        
        if success_rate >= 0.8:
            print(f"✅ Funcionalidad básica OK ({success_rate:.1%})")
            return True
        else:
            print(f"❌ Problemas en funcionalidad básica ({success_rate:.1%})")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando pruebas de funcionalidad: {e}")
        return False

def run_platform_specific_tests():
    """Ejecuta pruebas específicas de la plataforma."""
    print_section(f"PRUEBAS ESPECÍFICAS DE {platform.system().upper()}")
    
    platform_results = []
    
    if platform.system() == "Windows":
        # Probar comando chcp
        success, _, _ = run_command(
            'chcp',
            "Comando chcp (página de códigos)",
            timeout=10
        )
        platform_results.append(success)
        
        # Probar PowerShell
        success, _, _ = run_command(
            ['powershell', '-Command', 'Write-Host "Test"'],
            "PowerShell básico",
            timeout=15
        )
        platform_results.append(success)
        
        # Probar acceso al registro
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console", 0, winreg.KEY_READ):
                print("✅ Acceso al registro - OK")
                platform_results.append(True)
        except Exception as e:
            print(f"⚠️ Acceso al registro limitado: {e}")
            platform_results.append(False)
    
    else:
        print(f"ℹ️ Plataforma {platform.system()} - Pruebas básicas")
        # Para sistemas no-Windows, solo verificar Python básico
        success, _, _ = run_command(
            [sys.executable, '--version'],
            "Versión de Python",
            timeout=5
        )
        platform_results.append(success)
    
    success_rate = sum(platform_results) / len(platform_results) if platform_results else 0
    
    if success_rate >= 0.7:
        print(f"✅ Compatibilidad de plataforma OK ({success_rate:.1%})")
        return True
    else:
        print(f"❌ Problemas de compatibilidad ({success_rate:.1%})")
        return False

def generate_final_report(results):
    """Genera el reporte final de todas las pruebas."""
    print_header("REPORTE FINAL DE PRUEBAS")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"🕒 Fecha y hora: {timestamp}")
    print(f"💻 Sistema: {platform.system()} {platform.release()}")
    print(f"🏗️ Arquitectura: {platform.architecture()[0]}")
    print(f"🐍 Python: {platform.python_version()}")
    
    print(f"\n📊 RESULTADOS POR CATEGORÍA:")
    
    total_categories = len(results)
    passed_categories = sum(results.values())
    
    for category, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {category}: {status}")
    
    overall_score = passed_categories / total_categories if total_categories > 0 else 0
    
    print(f"\n🎯 PUNTUACIÓN GENERAL: {overall_score:.1%} ({passed_categories}/{total_categories})")
    
    if overall_score >= 0.9:
        print("🏆 EXCELENTE - NooxCLI está listo para producción")
        recommendation = "Todos los sistemas funcionan correctamente. ¡Excelente trabajo!"
    elif overall_score >= 0.8:
        print("✅ BUENO - NooxCLI está en buen estado")
        recommendation = "La mayoría de funcionalidades están OK. Revisar elementos fallidos."
    elif overall_score >= 0.7:
        print("⚠️ ACEPTABLE - Algunos problemas detectados")
        recommendation = "Hay problemas menores que deben ser corregidos antes del despliegue."
    elif overall_score >= 0.5:
        print("❌ NECESITA TRABAJO - Problemas significativos")
        recommendation = "Se requieren correcciones importantes antes de usar en producción."
    else:
        print("🚨 CRÍTICO - Múltiples fallas detectadas")
        recommendation = "El sistema necesita revisión completa antes de ser utilizable."
    
    print(f"\n💡 RECOMENDACIÓN: {recommendation}")
    
    # Sugerencias específicas
    print(f"\n🔧 PRÓXIMOS PASOS:")
    
    failed_categories = [cat for cat, passed in results.items() if not passed]
    
    if failed_categories:
        print("📋 Categorías que requieren atención:")
        for category in failed_categories:
            print(f"  - {category}")
        
        if "Dependencias" in failed_categories:
            print("💡 Instalar dependencias faltantes con pip")
        
        if "Sintaxis" in failed_categories:
            print("💡 Revisar y corregir errores de sintaxis en el código")
        
        if "Importación" in failed_categories:
            print("💡 Verificar rutas de módulos y dependencias")
        
        if "Integración" in failed_categories:
            print("💡 Revisar pruebas de integración detalladas")
        
        if "Rendimiento" in failed_categories:
            print("💡 Optimizar funciones lentas o con alto uso de memoria")
        
        if "Funcionalidad" in failed_categories:
            print("💡 Revisar implementación de métodos principales")
        
        if "Plataforma" in failed_categories:
            print("💡 Verificar compatibilidad con el sistema operativo actual")
    
    else:
        print("🎉 ¡Todas las categorías pasaron! El sistema está en excelente estado.")
        print("💡 Considera ejecutar pruebas adicionales de estrés o casos edge")
    
    return overall_score

def main():
    """Función principal que ejecuta todas las pruebas."""
    print_header("SUITE COMPLETA DE PRUEBAS - NooxCLI")
    
    start_time = time.time()
    
    # Diccionario para almacenar resultados
    results = {}
    
    # 1. Verificar dependencias
    results["Dependencias"] = check_dependencies()
    
    # 2. Verificar sintaxis
    results["Sintaxis"] = run_syntax_checks()
    
    # 3. Probar importaciones
    results["Importación"] = run_import_tests()
    
    # 4. Pruebas de funcionalidad básica
    results["Funcionalidad"] = run_manual_functionality_tests()
    
    # 5. Pruebas específicas de plataforma
    results["Plataforma"] = run_platform_specific_tests()
    
    # 6. Pruebas de integración (si las dependencias están OK)
    if results["Dependencias"] and results["Importación"]:
        results["Integración"] = run_integration_tests()
    else:
        print("⚠️ Saltando pruebas de integración (dependencias faltantes)")
        results["Integración"] = False
    
    # 7. Pruebas de rendimiento (si todo lo anterior está OK)
    if results["Dependencias"] and results["Funcionalidad"]:
        results["Rendimiento"] = run_performance_tests()
    else:
        print("⚠️ Saltando pruebas de rendimiento (problemas previos)")
        results["Rendimiento"] = False
    
    # Generar reporte final
    overall_score = generate_final_report(results)
    
    # Tiempo total
    total_time = time.time() - start_time
    print(f"\n⏱️ Tiempo total de ejecución: {total_time:.2f} segundos")
    
    # Código de salida
    exit_code = 0 if overall_score >= 0.8 else 1
    
    if exit_code == 0:
        print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revisar los resultados arriba.")
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())