#!/usr/bin/env python3
"""
Pruebas de rendimiento para los módulos de NooxCLI.
Mide tiempos de respuesta, uso de memoria y eficiencia.
"""

import os
import sys
import time
import psutil
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import tracemalloc

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class PerformanceProfiler:
    """Clase para medir rendimiento de funciones."""
    
    def __init__(self):
        self.results = {}
        
    def measure_time(self, func, *args, **kwargs):
        """Mide el tiempo de ejecución de una función."""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time
    
    def measure_memory(self, func, *args, **kwargs):
        """Mide el uso de memoria de una función."""
        tracemalloc.start()
        
        # Obtener memoria inicial
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Ejecutar función
        result = func(*args, **kwargs)
        
        # Obtener memoria final
        final_memory = process.memory_info().rss
        memory_diff = final_memory - initial_memory
        
        # Obtener estadísticas de tracemalloc
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        return result, {
            'memory_diff': memory_diff,
            'current_traced': current,
            'peak_traced': peak
        }
    
    def profile_function(self, func, name, *args, **kwargs):
        """Perfila una función midiendo tiempo y memoria."""
        print(f"📊 Perfilando: {name}")
        
        # Medir tiempo
        result, exec_time = self.measure_time(func, *args, **kwargs)
        
        # Medir memoria
        _, memory_stats = self.measure_memory(func, *args, **kwargs)
        
        self.results[name] = {
            'execution_time': exec_time,
            'memory_stats': memory_stats,
            'success': True
        }
        
        print(f"  ⏱️ Tiempo: {exec_time:.4f}s")
        print(f"  💾 Memoria pico: {memory_stats['peak_traced'] / 1024 / 1024:.2f} MB")
        
        return result

def test_sistema_module_performance():
    """Prueba el rendimiento del módulo sistema."""
    print("\n🔧 PRUEBAS DE RENDIMIENTO - MÓDULO SISTEMA")
    print("-" * 50)
    
    profiler = PerformanceProfiler()
    
    try:
        from src.noox_cli.modules import sistema
        
        # Crear instancia del módulo
        sistema_module = sistema.SistemaModule()
        
        # Probar inicialización
        profiler.profile_function(
            lambda: sistema.SistemaModule(),
            "Sistema - Inicialización"
        )
        
        # Probar obtención de información del sistema
        profiler.profile_function(
            sistema_module._get_system_info_fallback,
            "Sistema - Info del sistema (fallback)"
        )
        
        # Probar formateo de bytes
        profiler.profile_function(
            lambda: [sistema_module._format_bytes(i * 1024 * 1024) for i in range(1000)],
            "Sistema - Formateo de bytes (1000 iteraciones)"
        )
        
        # Probar parseo de memoria
        memory_strings = ["8,192 MB", "4 GB", "1024 KB"] * 100
        profiler.profile_function(
            lambda: [sistema_module._parse_memory_string(s) for s in memory_strings],
            "Sistema - Parseo de memoria (300 strings)"
        )
        
        # Probar obtención de procesos (si psutil está disponible)
        try:
            import psutil
            profiler.profile_function(
                lambda: sistema_module._get_process_list(50),
                "Sistema - Lista de procesos (50 procesos)"
            )
        except ImportError:
            print("⚠️ psutil no disponible, saltando prueba de procesos")
        
    except Exception as e:
        print(f"❌ Error en pruebas de sistema: {e}")
    
    return profiler.results

def test_reparar_module_performance():
    """Prueba el rendimiento del módulo reparar."""
    print("\n🔨 PRUEBAS DE RENDIMIENTO - MÓDULO REPARAR")
    print("-" * 50)
    
    profiler = PerformanceProfiler()
    
    try:
        from src.noox_cli.modules import reparar
        
        # Crear instancia del módulo
        reparar_module = reparar.RepararModule()
        
        # Probar inicialización
        profiler.profile_function(
            lambda: reparar.RepararModule(),
            "Reparar - Inicialización"
        )
        
        # Probar generación de contenido del perfil
        profiler.profile_function(
            reparar_module._get_profile_content,
            "Reparar - Generación de contenido del perfil"
        )
        
        # Probar verificación de oh-my-posh
        profiler.profile_function(
            reparar_module._check_omp_installation,
            "Reparar - Verificación oh-my-posh"
        )
        
        # Probar generación múltiple de contenido (stress test)
        profiler.profile_function(
            lambda: [reparar_module._get_profile_content() for _ in range(100)],
            "Reparar - Generación múltiple (100 iteraciones)"
        )
        
    except Exception as e:
        print(f"❌ Error en pruebas de reparar: {e}")
    
    return profiler.results

def test_test_utf8_module_performance():
    """Prueba el rendimiento del módulo test_utf8."""
    print("\n🧪 PRUEBAS DE RENDIMIENTO - MÓDULO TEST UTF-8")
    print("-" * 50)
    
    profiler = PerformanceProfiler()
    
    try:
        from src.noox_cli.modules import test_utf8
        
        # Crear instancia del módulo
        utf8_module = test_utf8.TestUtf8Module()
        
        # Probar inicialización
        profiler.profile_function(
            lambda: test_utf8.TestUtf8Module(),
            "UTF-8 - Inicialización"
        )
        
        # Probar verificación de soporte de colores
        profiler.profile_function(
            utf8_module._check_color_support,
            "UTF-8 - Verificación soporte de colores"
        )
        
        # Probar obtención de codificación de Python
        profiler.profile_function(
            utf8_module._get_python_encoding,
            "UTF-8 - Obtención codificación Python"
        )
        
        # Probar verificación múltiple de colores (stress test)
        profiler.profile_function(
            lambda: [utf8_module._check_color_support() for _ in range(1000)],
            "UTF-8 - Verificación colores (1000 iteraciones)"
        )
        
        # Probar información de codificación en Windows
        if platform.system() == "Windows":
            profiler.profile_function(
                utf8_module._get_powershell_encoding,
                "UTF-8 - Codificación PowerShell"
            )
        
    except Exception as e:
        print(f"❌ Error en pruebas de test_utf8: {e}")
    
    return profiler.results

def test_config_module_performance():
    """Prueba el rendimiento del módulo config."""
    print("\n⚙️ PRUEBAS DE RENDIMIENTO - MÓDULO CONFIG")
    print("-" * 50)
    
    profiler = PerformanceProfiler()
    
    try:
        from src.noox_cli.modules import config
        
        # Crear instancia del módulo
        config_module = config.ConfigModule()
        
        # Probar inicialización
        profiler.profile_function(
            lambda: config.ConfigModule(),
            "Config - Inicialización"
        )
        
        # Probar obtención de página de códigos
        profiler.profile_function(
            config_module._get_current_codepage,
            "Config - Página de códigos actual"
        )
        
        # Probar obtención de codificación de Python
        profiler.profile_function(
            config_module._get_python_encoding,
            "Config - Codificación Python"
        )
        
        # Probar obtención de codificación de PowerShell
        profiler.profile_function(
            config_module._get_powershell_encoding,
            "Config - Codificación PowerShell"
        )
        
        # Probar obtención múltiple de página de códigos (stress test)
        profiler.profile_function(
            lambda: [config_module._get_current_codepage() for _ in range(100)],
            "Config - Página códigos (100 iteraciones)"
        )
        
        # Probar configuración del registro en Windows
        if platform.system() == "Windows":
            profiler.profile_function(
                config_module._get_registry_config,
                "Config - Configuración del registro"
            )
        
    except Exception as e:
        print(f"❌ Error en pruebas de config: {e}")
    
    return profiler.results

def test_menu_system_performance():
    """Prueba el rendimiento del sistema de menús."""
    print("\n📋 PRUEBAS DE RENDIMIENTO - SISTEMA DE MENÚS")
    print("-" * 50)
    
    profiler = PerformanceProfiler()
    
    try:
        from src.noox_cli.menu import NooxMenu
        
        # Probar inicialización del menú
        profiler.profile_function(
            lambda: NooxMenu("Test Menu"),
            "Menu - Inicialización"
        )
        
        menu = NooxMenu("Test Menu")
        
        # Probar creación de múltiples menús
        profiler.profile_function(
            lambda: [NooxMenu(f"Menu {i}") for i in range(100)],
            "Menu - Creación múltiple (100 menús)"
        )
        
        # Probar métodos de mensaje
        profiler.profile_function(
            lambda: [menu.show_info(f"Mensaje {i}") for i in range(100)],
            "Menu - Mensajes info (100 mensajes)"
        )
        
    except Exception as e:
        print(f"❌ Error en pruebas de menú: {e}")
    
    return profiler.results

def test_startup_performance():
    """Prueba el rendimiento de inicio de la aplicación."""
    print("\n🚀 PRUEBAS DE RENDIMIENTO - INICIO DE APLICACIÓN")
    print("-" * 50)
    
    profiler = PerformanceProfiler()
    
    try:
        # Probar importación de módulos
        profiler.profile_function(
            lambda: __import__('src.noox_cli.modules.sistema', fromlist=['']),
            "Startup - Importación módulo sistema"
        )
        
        profiler.profile_function(
            lambda: __import__('src.noox_cli.modules.reparar', fromlist=['']),
            "Startup - Importación módulo reparar"
        )
        
        profiler.profile_function(
            lambda: __import__('src.noox_cli.modules.test_utf8', fromlist=['']),
            "Startup - Importación módulo test_utf8"
        )
        
        profiler.profile_function(
            lambda: __import__('src.noox_cli.modules.config', fromlist=['']),
            "Startup - Importación módulo config"
        )
        
        # Probar importación completa
        def import_all_modules():
            from src.noox_cli.modules import sistema, reparar, test_utf8, config
            from src.noox_cli.menu import NooxMenu
            return sistema, reparar, test_utf8, config, NooxMenu
        
        profiler.profile_function(
            import_all_modules,
            "Startup - Importación completa"
        )
        
    except Exception as e:
        print(f"❌ Error en pruebas de startup: {e}")
    
    return profiler.results

def analyze_performance_results(all_results: Dict[str, Dict]):
    """Analiza los resultados de rendimiento y genera recomendaciones."""
    print("\n📊 ANÁLISIS DE RENDIMIENTO")
    print("=" * 50)
    
    # Recopilar todas las métricas
    all_times = []
    all_memory = []
    slow_functions = []
    memory_heavy_functions = []
    
    for module_name, results in all_results.items():
        print(f"\n📦 {module_name.upper()}:")
        
        for func_name, metrics in results.items():
            if metrics.get('success', False):
                exec_time = metrics['execution_time']
                memory_peak = metrics['memory_stats']['peak_traced']
                
                all_times.append(exec_time)
                all_memory.append(memory_peak)
                
                print(f"  {func_name}:")
                print(f"    ⏱️ Tiempo: {exec_time:.4f}s")
                print(f"    💾 Memoria: {memory_peak / 1024 / 1024:.2f} MB")
                
                # Identificar funciones lentas (>1 segundo)
                if exec_time > 1.0:
                    slow_functions.append((func_name, exec_time))
                
                # Identificar funciones que usan mucha memoria (>50 MB)
                if memory_peak > 50 * 1024 * 1024:
                    memory_heavy_functions.append((func_name, memory_peak))
    
    # Estadísticas generales
    if all_times:
        avg_time = sum(all_times) / len(all_times)
        max_time = max(all_times)
        min_time = min(all_times)
        
        print(f"\n📈 ESTADÍSTICAS DE TIEMPO:")
        print(f"  Promedio: {avg_time:.4f}s")
        print(f"  Máximo: {max_time:.4f}s")
        print(f"  Mínimo: {min_time:.4f}s")
    
    if all_memory:
        avg_memory = sum(all_memory) / len(all_memory)
        max_memory = max(all_memory)
        min_memory = min(all_memory)
        
        print(f"\n💾 ESTADÍSTICAS DE MEMORIA:")
        print(f"  Promedio: {avg_memory / 1024 / 1024:.2f} MB")
        print(f"  Máximo: {max_memory / 1024 / 1024:.2f} MB")
        print(f"  Mínimo: {min_memory / 1024 / 1024:.2f} MB")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    
    if slow_functions:
        print(f"⚠️ Funciones lentas detectadas:")
        for func_name, exec_time in sorted(slow_functions, key=lambda x: x[1], reverse=True):
            print(f"  - {func_name}: {exec_time:.4f}s")
        print("  💡 Considera optimizar estas funciones o agregar indicadores de progreso")
    
    if memory_heavy_functions:
        print(f"⚠️ Funciones con alto uso de memoria:")
        for func_name, memory in sorted(memory_heavy_functions, key=lambda x: x[1], reverse=True):
            print(f"  - {func_name}: {memory / 1024 / 1024:.2f} MB")
        print("  💡 Considera optimizar el uso de memoria o implementar liberación explícita")
    
    if not slow_functions and not memory_heavy_functions:
        print("✅ Todas las funciones tienen buen rendimiento")
    
    # Puntuación general
    performance_score = 100
    
    # Penalizar funciones lentas
    performance_score -= len(slow_functions) * 10
    
    # Penalizar uso excesivo de memoria
    performance_score -= len(memory_heavy_functions) * 5
    
    # Asegurar que la puntuación no sea negativa
    performance_score = max(0, performance_score)
    
    print(f"\n🎯 PUNTUACIÓN DE RENDIMIENTO: {performance_score}/100")
    
    if performance_score >= 90:
        print("🏆 EXCELENTE - Rendimiento óptimo")
    elif performance_score >= 80:
        print("✅ BUENO - Rendimiento aceptable")
    elif performance_score >= 70:
        print("⚠️ REGULAR - Necesita algunas optimizaciones")
    else:
        print("❌ POBRE - Requiere optimizaciones importantes")
    
    return performance_score

def main():
    """Función principal de las pruebas de rendimiento."""
    # Configurar UTF-8 para evitar errores de codificación
    if platform.system() == "Windows":
        os.system('chcp 65001 > nul')
    
    print("SUITE DE PRUEBAS DE RENDIMIENTO - NooxCLI")
    print("=" * 60)
    
    start_time = time.time()
    
    # Información del sistema
    print(f"💻 Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {platform.python_version()}")
    print(f"⚙️ Procesador: {platform.processor()}")
    
    if hasattr(psutil, 'cpu_count'):
        print(f"🔢 CPUs: {psutil.cpu_count()}")
    
    if hasattr(psutil, 'virtual_memory'):
        memory = psutil.virtual_memory()
        print(f"💾 Memoria: {memory.total / 1024 / 1024 / 1024:.1f} GB")
    
    # Ejecutar todas las pruebas de rendimiento
    all_results = {}
    
    # Pruebas de startup
    startup_results = test_startup_performance()
    if startup_results:
        all_results['startup'] = startup_results
    
    # Pruebas del sistema de menús
    menu_results = test_menu_system_performance()
    if menu_results:
        all_results['menu'] = menu_results
    
    # Pruebas de módulos individuales
    sistema_results = test_sistema_module_performance()
    if sistema_results:
        all_results['sistema'] = sistema_results
    
    reparar_results = test_reparar_module_performance()
    if reparar_results:
        all_results['reparar'] = reparar_results
    
    utf8_results = test_test_utf8_module_performance()
    if utf8_results:
        all_results['test_utf8'] = utf8_results
    
    config_results = test_config_module_performance()
    if config_results:
        all_results['config'] = config_results
    
    # Analizar resultados
    performance_score = analyze_performance_results(all_results)
    
    # Tiempo total de ejecución
    total_time = time.time() - start_time
    print(f"\n⏱️ Tiempo total de pruebas: {total_time:.2f}s")
    
    # Retornar código de salida basado en la puntuación
    return 0 if performance_score >= 70 else 1

if __name__ == '__main__':
    sys.exit(main())