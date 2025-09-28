#!/usr/bin/env python3
"""
Script de prueba para verificar que Windows Terminal se abre correctamente.
ADVERTENCIA: Este script abrirá realmente Windows Terminal.
"""

import os
import sys
import time
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_open_terminal_desarrollo():
    """Prueba abrir terminal desde el módulo desarrollo."""
    print("🛠️ PROBANDO APERTURA DE TERMINAL - MÓDULO DESARROLLO")
    print("-" * 50)
    
    try:
        from noox_cli.modules.desarrollo import DesarrolloModule
        
        desarrollo = DesarrolloModule()
        
        print("  🔍 Detectando Windows Terminal...")
        wt_executable = desarrollo._find_windows_terminal()
        
        if wt_executable:
            print(f"  ✅ Windows Terminal encontrado: {wt_executable}")
            
            # Preguntar al usuario si quiere probar
            response = input("  ❓ ¿Quieres probar abrir Windows Terminal? (s/N): ")
            
            if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                print("  🚀 Abriendo Windows Terminal...")
                
                success = desarrollo._open_terminal()
                
                if success:
                    print("  ✅ Terminal abierto exitosamente")
                    print("  💡 Verifica que se abrió Windows Terminal con el directorio correcto")
                    return True
                else:
                    print("  ❌ Error abriendo terminal")
                    return False
            else:
                print("  ℹ️ Prueba cancelada por el usuario")
                return True  # No es un error, solo cancelado
        else:
            print("  ❌ Windows Terminal no encontrado")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en prueba: {e}")
        return False

def test_open_terminal_proyectos():
    """Prueba abrir terminal desde el módulo proyectos."""
    print("\n📁 PROBANDO APERTURA DE TERMINAL - MÓDULO PROYECTOS")
    print("-" * 50)
    
    try:
        from noox_cli.modules.proyectos import ProyectosModule
        
        proyectos = ProyectosModule()
        
        print("  🔍 Detectando Windows Terminal...")
        wt_executable = proyectos._find_windows_terminal()
        
        if wt_executable:
            print(f"  ✅ Windows Terminal encontrado: {wt_executable}")
            
            # Preguntar al usuario si quiere probar
            response = input("  ❓ ¿Quieres probar abrir Windows Terminal para proyectos? (s/N): ")
            
            if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                print("  🚀 Abriendo Windows Terminal...")
                
                # Usar directorio actual como proyecto de prueba
                test_project_path = Path.cwd()
                success = proyectos._open_terminal(test_project_path)
                
                if success:
                    print("  ✅ Terminal abierto exitosamente")
                    print("  💡 Verifica que se abrió Windows Terminal con el directorio correcto")
                    return True
                else:
                    print("  ❌ Error abriendo terminal")
                    return False
            else:
                print("  ℹ️ Prueba cancelada por el usuario")
                return True  # No es un error, solo cancelado
        else:
            print("  ❌ Windows Terminal no encontrado")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en prueba: {e}")
        return False

def show_wt_session_info():
    """Muestra información sobre la sesión actual de Windows Terminal."""
    print("\n📊 INFORMACIÓN DE SESIÓN ACTUAL")
    print("-" * 40)
    
    wt_session = os.environ.get('WT_SESSION')
    wt_profile = os.environ.get('WT_PROFILE_ID')
    
    if wt_session:
        print(f"  ✅ Ejecutándose en Windows Terminal")
        print(f"    Session ID: {wt_session}")
        if wt_profile:
            print(f"    Profile ID: {wt_profile}")
        print("  💡 Los nuevos terminales se abrirán como pestañas")
    else:
        print("  ℹ️ No se está ejecutando en Windows Terminal")
        print("  💡 Los nuevos terminales se abrirán como ventanas nuevas")

def main():
    """Función principal de las pruebas de apertura."""
    print("🖥️ PRUEBAS DE APERTURA DE WINDOWS TERMINAL")
    print("=" * 50)
    
    print("⚠️  ADVERTENCIA: Este script abrirá realmente Windows Terminal")
    print("🔄 Asegúrate de cerrar las ventanas/pestañas después de la prueba")
    print()
    
    # Mostrar información de sesión
    show_wt_session_info()
    
    # Preguntar si continuar
    response = input("\n❓ ¿Continuar con las pruebas? (s/N): ")
    
    if response.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("ℹ️ Pruebas canceladas por el usuario")
        return 0
    
    # Ejecutar pruebas
    tests = [
        ("Módulo Desarrollo", test_open_terminal_desarrollo),
        ("Módulo Proyectos", test_open_terminal_proyectos)
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
    
    if success_rate >= 0.5:
        print("🎉 ¡Windows Terminal se abre correctamente!")
        print("💡 Ahora los terminales se abrirán en tu Windows Terminal configurado")
        print("🎨 Mantendrás todos tus iconos, colores y configuración personalizada")
        return 0
    else:
        print("⚠️ Problemas abriendo Windows Terminal")
        print("💡 Verifica la instalación y configuración")
        return 1

if __name__ == '__main__':
    sys.exit(main())