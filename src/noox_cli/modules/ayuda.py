"""
Módulo de Ayuda - NooxCLI
Migrado desde ayuda.bat con interfaz interactiva mejorada
"""

from typing import List, Dict, Any
from ..menu import NooxMenu
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich import box


class AyudaModule:
    """Módulo de ayuda interactivo."""
    
    def __init__(self):
        self.menu = NooxMenu("Ayuda - NooxCLI")
    
    def main(self):
        """Función principal del módulo de ayuda."""
        while True:
            self.menu.show_banner()
            
            # Menú principal de ayuda
            choices = [
                {
                    'name': '📚 Comandos Disponibles',
                    'value': 'comandos',
                    'description': 'Lista de todos los comandos disponibles'
                },
                {
                    'name': '🛠️ Funciones de Desarrollo',
                    'value': 'desarrollo',
                    'description': 'Herramientas y utilidades de desarrollo'
                },
                {
                    'name': '⚙️ Funciones de Sistema',
                    'value': 'sistema',
                    'description': 'Administración y monitoreo del sistema'
                },
                {
                    'name': '📁 Funciones de Proyectos',
                    'value': 'proyectos',
                    'description': 'Gestión y creación de proyectos'
                },
                {
                    'name': '🔧 Funciones de Configuración',
                    'value': 'configuracion',
                    'description': 'Configuración de consola y UTF-8'
                },
                {
                    'name': '🔍 Buscar Ayuda',
                    'value': 'buscar',
                    'description': 'Buscar ayuda específica'
                }
            ]
            
            selection = self.menu.show_menu(choices, "📖 ¿Sobre qué necesitas ayuda?")
            
            if not selection or selection == 'exit':
                break
            
            self._handle_selection(selection)
    
    def _handle_selection(self, selection: str):
        """Maneja la selección del usuario."""
        handlers = {
            'comandos': self._show_comandos,
            'desarrollo': self._show_desarrollo,
            'sistema': self._show_sistema,
            'proyectos': self._show_proyectos,
            'configuracion': self._show_configuracion,
            'buscar': self._buscar_ayuda
        }
        
        if selection in handlers:
            handlers[selection]()
            self.menu.pause()
    
    def _show_comandos(self):
        """Muestra todos los comandos disponibles."""
        self.menu.clear_screen()
        
        comandos_data = [
            ("desarrollo", "Herramientas de desarrollo"),
            ("sistema", "Administración del sistema"),
            ("proyectos", "Gestión de proyectos"),
            ("config", "Configuración UTF-8/Consola"),
            ("test-utf8", "Prueba de caracteres especiales"),
            ("ayuda", "Sistema de ayuda interactivo"),
            ("reparar", "Utilidades de reparación")
        ]
        
        # Crear tabla de comandos
        comandos_text = Text()
        comandos_text.append("COMANDO", style="bold cyan")
        comandos_text.append("          ", style="white")
        comandos_text.append("DESCRIPCIÓN", style="bold cyan")
        comandos_text.append("\\n")
        comandos_text.append("─" * 50, style="white")
        comandos_text.append("\\n")
        
        for comando, descripcion in comandos_data:
            comandos_text.append(f"{comando:<15}", style="yellow")
            comandos_text.append(f" {descripcion}", style="white")
            comandos_text.append("\\n")
        
        panel = Panel(
            comandos_text,
            title="📚 Comandos Disponibles",
            border_style="green",
            box=box.DOUBLE
        )
        
        self.menu.console.print(panel)
        
        self.menu.show_info("💡 Tip: Todos estos comandos ahora tienen menús interactivos")
        self.menu.show_info("📝 Nota: Los scripts originales están en tu carpeta Scripts")
    
    def _show_desarrollo(self):
        """Muestra ayuda sobre funciones de desarrollo."""
        self.menu.clear_screen()
        
        funciones = [
            "🔧 Abrir VS Code en directorio actual",
            "📦 Git (init, status, add, commit, push)",
            "📚 NPM/Yarn (install, update, cache clean)",
            "🐍 Python (crear estructura, servidor desarrollo)",
            "💻 PowerShell (scripts y utilidades)",
            "🔍 Diagnóstico de entorno de desarrollo",
            "🚀 Herramientas de productividad"
        ]
        
        funciones_text = Text()
        for funcion in funciones:
            funciones_text.append(f"• {funcion}", style="white")
            funciones_text.append("\\n")
        
        panel = Panel(
            funciones_text,
            title="🛠️ Funciones de Desarrollo",
            border_style="blue",
            box=box.ROUNDED
        )
        
        self.menu.console.print(panel)
        self.menu.show_info("💡 Accede a estas funciones usando el módulo 'Desarrollo'")
    
    def _show_sistema(self):
        """Muestra ayuda sobre funciones de sistema."""
        self.menu.clear_screen()
        
        funciones = [
            "📊 Información del sistema y procesos",
            "🌐 Red (IP, ping, DNS flush, conexiones)",
            "💾 Espacio en disco y uso de memoria",
            "🧹 Limpieza de archivos temporales",
            "⚡ Administrador de tareas avanzado",
            "🔒 Servicios de Windows",
            "📈 Monitoreo de rendimiento",
            "🔧 Utilidades de diagnóstico"
        ]
        
        funciones_text = Text()
        for funcion in funciones:
            funciones_text.append(f"• {funcion}", style="white")
            funciones_text.append("\\n")
        
        panel = Panel(
            funciones_text,
            title="⚙️ Funciones de Sistema",
            border_style="red",
            box=box.ROUNDED
        )
        
        self.menu.console.print(panel)
        self.menu.show_info("💡 Accede a estas funciones usando el módulo 'Sistema'")
    
    def _show_proyectos(self):
        """Muestra ayuda sobre funciones de proyectos."""
        self.menu.clear_screen()
        
        funciones = [
            "🆕 Crear proyectos (Web, Python, Node.js, React)",
            "📥 Clonar repositorios de GitHub/GitLab", 
            "📦 Backup y compresión de proyectos",
            "🚀 Deploy y testing automatizado",
            "🐳 Operaciones con Docker",
            "🔄 Gestión de dependencias",
            "📋 Templates de proyectos",
            "🗂️ Organización de workspace"
        ]
        
        funciones_text = Text()
        for funcion in funciones:
            funciones_text.append(f"• {funcion}", style="white")
            funciones_text.append("\\n")
        
        panel = Panel(
            funciones_text,
            title="📁 Funciones de Proyectos",
            border_style="magenta",
            box=box.ROUNDED
        )
        
        self.menu.console.print(panel)
        self.menu.show_info("💡 Accede a estas funciones usando el módulo 'Proyectos'")
    
    def _show_configuracion(self):
        """Muestra ayuda sobre funciones de configuración."""
        self.menu.clear_screen()
        
        funciones = [
            "🌐 Configurar UTF-8 y codificación de caracteres",
            "🎨 Cambiar fuentes y colores de consola",
            "🧪 Probar caracteres especiales y emojis",
            "🔍 Diagnóstico de problemas de codificación",
            "⚙️ Configuración de PowerShell profile",
            "🎯 Personalización de prompt",
            "📝 Variables de entorno",
            "🔧 Herramientas de diagnóstico"
        ]
        
        funciones_text = Text()
        for funcion in funciones:
            funciones_text.append(f"• {funcion}", style="white")
            funciones_text.append("\\n")
        
        panel = Panel(
            funciones_text,
            title="🔧 Funciones de Configuración",
            border_style="cyan",
            box=box.ROUNDED
        )
        
        self.menu.console.print(panel)
        self.menu.show_info("💡 Accede a estas funciones usando el módulo 'Configuración'")
    
    def _buscar_ayuda(self):
        """Permite buscar ayuda específica."""
        self.menu.clear_screen()
        
        termino = self.menu.show_input("🔍 Ingresa el término a buscar:")
        
        if not termino:
            return
        
        # Simulamos una búsqueda simple
        termino_lower = termino.lower()
        resultados = []
        
        # Base de conocimiento simple
        conocimiento = {
            "git": "Herramientas Git están en el módulo Desarrollo",
            "npm": "Comandos NPM están en el módulo Desarrollo", 
            "python": "Utilidades Python están en el módulo Desarrollo",
            "sistema": "Información del sistema está en el módulo Sistema",
            "red": "Herramientas de red están en el módulo Sistema",
            "proyectos": "Gestión de proyectos está en el módulo Proyectos",
            "utf8": "Configuración UTF-8 está en el módulo Configuración",
            "codificacion": "Problemas de codificación están en el módulo Configuración",
            "docker": "Operaciones Docker están en el módulo Proyectos"
        }
        
        for palabra, ayuda in conocimiento.items():
            if palabra in termino_lower:
                resultados.append(f"• {ayuda}")
        
        if resultados:
            self.menu.show_success(f"Resultados para '{termino}':")
            for resultado in resultados:
                self.menu.console.print(f"  {resultado}")
        else:
            self.menu.show_warning(f"No se encontraron resultados para '{termino}'")
            self.menu.show_info("💡 Intenta con términos como: git, npm, python, sistema, red, etc.")


def main():
    """Función principal del módulo."""
    ayuda_module = AyudaModule()
    ayuda_module.main()


if __name__ == "__main__":
    main()
