"""
Sistema de menús interactivos para NooxCLI.
Utiliza InquirerPy para crear interfaces de usuario navegables con flechas.
"""

import os
import sys
from typing import List, Dict, Any, Optional, Callable
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
import colorama

# Inicializar colorama para Windows
colorama.init()

class NooxMenu:
    """Clase base para crear menús interactivos con InquirerPy."""
    
    def __init__(self, title: str = "NooxCLI"):
        self.console = Console()
        self.title = title
        
    def clear_screen(self):
        """Limpia la pantalla de forma multiplataforma."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_banner(self):
        """Muestra el banner principal de NooxCLI."""
        self.clear_screen()
        
        banner_text = Text()
        banner_text.append("🚀 ", style="bold blue")
        banner_text.append("NooxCLI", style="bold cyan")
        banner_text.append(" - CLI Interactiva Moderna", style="bold white")
        
        info_text = Text()
        info_text.append("✨ Navega con ", style="white")
        info_text.append("↑↓", style="bold yellow")
        info_text.append(" - Selecciona con ", style="white")
        info_text.append("ENTER", style="bold green")
        info_text.append(" - Salir con ", style="white")
        info_text.append("CTRL+C", style="bold red")
        
        panel = Panel(
            f"{banner_text}\\n{info_text}",
            box=box.DOUBLE,
            border_style="cyan",
            title="🎯 Bienvenido",
            title_align="center"
        )
        
        self.console.print(panel)
        self.console.print()
    
    def show_menu(self, choices: List[Dict[str, Any]], message: str = "Selecciona una opción:") -> Optional[str]:
        """
        Muestra un menú interactivo con las opciones proporcionadas.
        
        Args:
            choices: Lista de diccionarios con 'name', 'value' y opcionalmente 'description'
            message: Mensaje a mostrar en el prompt
            
        Returns:
            El valor de la opción seleccionada o None si se cancela
        """
        try:
            # Convertir choices al formato de InquirerPy
            inquirer_choices = []
            for choice in choices:
                if isinstance(choice, dict):
                    name = choice.get('name', choice.get('value', str(choice)))
                    value = choice.get('value', choice.get('name', str(choice)))
                    
                    if 'description' in choice:
                        name = f"{name} - {choice['description']}"
                    
                    inquirer_choices.append(Choice(name=name, value=value))
                else:
                    inquirer_choices.append(Choice(name=str(choice), value=str(choice)))
            
            # Agregar opción de salir si no existe
            if not any(choice.value in ['exit', 'salir', 'volver'] for choice in inquirer_choices):
                inquirer_choices.append(Choice(name="← Volver/Salir", value="exit"))
            
            questions = [
                {
                    'type': 'list',
                    'name': 'selection',
                    'message': message,
                    'choices': inquirer_choices,
                    'default': inquirer_choices[0] if inquirer_choices else None
                }
            ]
            
            result = prompt(questions)
            return result.get('selection') if result else None
            
        except KeyboardInterrupt:
            self.console.print("\\n[red]Operación cancelada por el usuario[/red]")
            return None
        except Exception as e:
            self.console.print(f"[red]Error en el menú: {e}[/red]")
            return None
    
    def show_confirmation(self, message: str = "¿Continuar?") -> bool:
        """Muestra un prompt de confirmación."""
        try:
            questions = [
                {
                    'type': 'confirm',
                    'name': 'confirm',
                    'message': message,
                    'default': True
                }
            ]
            
            result = prompt(questions)
            return result.get('confirm', False) if result else False
            
        except KeyboardInterrupt:
            return False
    
    def show_input(self, message: str, default: str = "") -> Optional[str]:
        """Muestra un prompt de entrada de texto."""
        try:
            questions = [
                {
                    'type': 'input',
                    'name': 'input',
                    'message': message,
                    'default': default
                }
            ]
            
            result = prompt(questions)
            return result.get('input') if result else None
            
        except KeyboardInterrupt:
            return None
    
    def show_success(self, message: str):
        """Muestra un mensaje de éxito."""
        self.console.print(f"[green]✅ {message}[/green]")
    
    def show_error(self, message: str):
        """Muestra un mensaje de error."""
        self.console.print(f"[red]❌ {message}[/red]")
    
    def show_warning(self, message: str):
        """Muestra un mensaje de advertencia."""
        self.console.print(f"[yellow]⚠️ {message}[/yellow]")
    
    def show_info(self, message: str):
        """Muestra un mensaje informativo."""
        self.console.print(f"[blue]ℹ️ {message}[/blue]")
    
    def pause(self, message: str = "Presiona ENTER para continuar..."):
        """Pausa la ejecución hasta que el usuario presione ENTER."""
        try:
            input(f"\\n{message}")
        except KeyboardInterrupt:
            pass


def create_main_menu() -> List[Dict[str, Any]]:
    """Crea las opciones del menú principal."""
    return [
        {
            'name': '🛠️  Desarrollo',
            'value': 'desarrollo',
            'description': 'Herramientas de desarrollo'
        },
        {
            'name': '⚙️  Sistema', 
            'value': 'sistema',
            'description': 'Scripts y utilidades del sistema'
        },
        {
            'name': '📁 Proyectos',
            'value': 'proyectos', 
            'description': 'Gestión de proyectos Laragon'
        },
        {
            'name': '🔧 Configuración',
            'value': 'config',
            'description': 'Configuración de consola y UTF-8'
        },
        {
            'name': '❓ Ayuda',
            'value': 'ayuda',
            'description': 'Sistema de ayuda y documentación'
        },
        {
            'name': '🔨 Reparar',
            'value': 'reparar',
            'description': 'Utilidades de reparación'
        },
        {
            'name': '🧪 Test UTF-8',
            'value': 'test_utf8',
            'description': 'Pruebas de codificación'
        }
    ]
