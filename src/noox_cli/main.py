#!/usr/bin/env python3
"""
NooxCLI - Punto de entrada principal
CLI moderna con menús interactivos para desarrollo y administración de sistema
"""

import sys
import os
from typing import Dict, Any
import colorama

# Asegurar que el directorio src esté en el path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from noox_cli.menu import NooxMenu, create_main_menu
from noox_cli.modules import ayuda, desarrollo, sistema, proyectos, config, reparar, test_utf8

# Inicializar colorama para Windows
colorama.init()

class NooxCLI:
    """Clase principal de la aplicación NooxCLI."""
    
    def __init__(self):
        self.menu = NooxMenu("NooxCLI - Terminal Moderna")
        self.modules = {
            'desarrollo': desarrollo,
            'sistema': sistema, 
            'proyectos': proyectos,
            'config': config,
            'ayuda': ayuda,
            'reparar': reparar,
            'test_utf8': test_utf8
        }
    
    def run(self):
        """Ejecuta el bucle principal de la aplicación."""
        try:
            while True:
                self.menu.show_banner()
                
                # Mostrar menú principal
                main_choices = create_main_menu()
                selection = self.menu.show_menu(
                    main_choices, 
                    "🎯 Selecciona un módulo:"
                )
                
                if not selection or selection == 'exit':
                    self.exit_application()
                    break
                    
                # Ejecutar el módulo seleccionado
                self.execute_module(selection)
                
        except KeyboardInterrupt:
            self.exit_application()
        except Exception as e:
            self.menu.show_error(f"Error inesperado: {e}")
            self.menu.pause()
    
    def execute_module(self, module_name: str):
        """Ejecuta un módulo específico."""
        try:
            if module_name in self.modules:
                module = self.modules[module_name]
                if hasattr(module, 'main'):
                    module.main()
                else:
                    self.menu.show_warning(f"El módulo '{module_name}' no tiene función main()")
            else:
                self.menu.show_error(f"Módulo '{module_name}' no encontrado")
                
        except KeyboardInterrupt:
            self.menu.show_info("Módulo cancelado por el usuario")
        except Exception as e:
            self.menu.show_error(f"Error ejecutando módulo '{module_name}': {e}")
        
        # Pausa antes de volver al menú principal
        self.menu.pause()
    
    def exit_application(self):
        """Salir de la aplicación con mensaje de despedida."""
        self.menu.clear_screen()
        self.menu.show_success("¡Gracias por usar NooxCLI! 👋")
        self.menu.show_info("Desarrollado con ❤️ por Sebastian")
        sys.exit(0)


def main():
    """Función principal - punto de entrada del comando 'noox'."""
    try:
        # Configurar UTF-8 en Windows
        if os.name == 'nt':
            os.system('chcp 65001 > nul')
        
        app = NooxCLI()
        app.run()
        
    except KeyboardInterrupt:
        print("\\n¡Hasta luego! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
