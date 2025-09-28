"""
Módulo de Desarrollo - NooxCLI
Migrado desde desarrollo.bat con interfaz interactiva mejorada
Herramientas para desarrollo: Git, NPM, Python, VS Code, etc.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..menu import NooxMenu
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box


class DesarrolloModule:
    """Módulo de herramientas de desarrollo."""
    
    def __init__(self):
        self.menu = NooxMenu("Desarrollo - NooxCLI")
        self.current_dir = Path.cwd()
        
    def main(self):
        """Función principal del módulo de desarrollo."""
        while True:
            self.menu.show_banner()
            
            # Mostrar directorio actual
            self.menu.show_info(f"📁 Directorio actual: {self.current_dir}")
            self.menu.console.print()
            
            # Menú principal de desarrollo
            choices = [
                {
                    'name': '💻 Abrir VS Code',
                    'value': 'vscode',
                    'description': 'Abrir VS Code en directorio actual'
                },
                {
                    'name': '🔄 Git - Inicializar proyecto',
                    'value': 'git_init',
                    'description': 'Inicializar repositorio Git'
                },
                {
                    'name': '📦 Node.js - Instalar dependencias',
                    'value': 'npm_install',
                    'description': 'npm/yarn install'
                },
                {
                    'name': '🐍 Python - Crear estructura',
                    'value': 'python_struct',
                    'description': 'Crear estructura de proyecto Python'
                },
                {
                    'name': '🌐 Servidor local',
                    'value': 'local_server',
                    'description': 'Lanzar servidor de desarrollo'
                },
                {
                    'name': '⚡ PowerShell aquí',
                    'value': 'powershell',
                    'description': 'Abrir PowerShell en directorio'
                },
                {
                    'name': '📊 Git - Estado',
                    'value': 'git_status',
                    'description': 'Ver estado y commits recientes'
                },
                {
                    'name': '🚀 Git - Push rápido',
                    'value': 'git_push',
                    'description': 'Add, commit y push'
                },
                {
                    'name': '🧹 Limpiar cache',
                    'value': 'clean_cache',
                    'description': 'Limpiar cache npm/yarn/pip'
                },
                {
                    'name': '🔧 Herramientas adicionales',
                    'value': 'extra_tools',
                    'description': 'Más herramientas de desarrollo'
                }
            ]
            
            selection = self.menu.show_menu(choices, "🛠️ ¿Qué herramienta necesitas?")
            
            if not selection or selection == 'exit':
                break
            
            self._handle_selection(selection)
    
    def _handle_selection(self, selection: str):
        """Maneja la selección del usuario."""
        handlers = {
            'vscode': self._open_vscode,
            'git_init': self._git_init,
            'npm_install': self._npm_install,
            'python_struct': self._create_python_structure,
            'local_server': self._local_server,
            'powershell': self._open_powershell,
            'git_status': self._git_status,
            'git_push': self._git_push,
            'clean_cache': self._clean_cache,
            'extra_tools': self._extra_tools
        }
        
        if selection in handlers:
            try:
                handlers[selection]()
            except Exception as e:
                self.menu.show_error(f"Error ejecutando {selection}: {e}")
            self.menu.pause()
    
    def _open_vscode(self):
        """Abre VS Code en el directorio actual."""
        self.menu.clear_screen()
        
        try:
            if self._command_exists('code'):
                subprocess.run(['code', '.'], check=True)
                self.menu.show_success("✅ VS Code abierto correctamente")
            else:
                self.menu.show_error("❌ VS Code no está instalado o no está en PATH")
                self.menu.show_info("💡 Instala VS Code desde: https://code.visualstudio.com")
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"Error abriendo VS Code: {e}")
    
    def _git_init(self):
        """Inicializa un repositorio Git."""
        self.menu.clear_screen()
        
        # Verificar si ya existe un repositorio
        if (self.current_dir / '.git').exists():
            self.menu.show_warning("⚠️ Ya existe un repositorio Git en este directorio")
            return
        
        if not self._command_exists('git'):
            self.menu.show_error("❌ Git no está instalado")
            return
        
        try:
            self.menu.show_info("🔄 Inicializando repositorio Git...")
            
            # git init
            subprocess.run(['git', 'init'], check=True, capture_output=True)
            self.menu.show_success("✅ Repositorio inicializado")
            
            # git add .
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
            self.menu.show_success("✅ Archivos agregados al staging")
            
            # git commit
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True, capture_output=True)
            self.menu.show_success("✅ Commit inicial creado")
            
            self.menu.show_info("🎉 Repositorio Git configurado exitosamente!")
            
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"Error configurando Git: {e}")
    
    def _npm_install(self):
        """Instala dependencias de Node.js."""
        self.menu.clear_screen()
        
        # Verificar si existe package.json
        if not (self.current_dir / 'package.json').exists():
            self.menu.show_warning("⚠️ No se encontró package.json en este directorio")
            
            if self.menu.show_confirmation("¿Quieres inicializar un proyecto Node.js?"):
                try:
                    subprocess.run(['npm', 'init', '-y'], check=True)
                    self.menu.show_success("✅ package.json creado")
                except subprocess.CalledProcessError:
                    self.menu.show_error("❌ Error inicializando proyecto Node.js")
                    return
            else:
                return
        
        # Seleccionar gestor de paquetes
        package_managers = [
            {'name': '📦 npm install', 'value': 'npm'},
            {'name': '🧶 yarn install', 'value': 'yarn'},
            {'name': '⚡ pnpm install', 'value': 'pnpm'}
        ]
        
        selection = self.menu.show_menu(package_managers, "📦 Selecciona gestor de paquetes:")
        
        if not selection or selection == 'exit':
            return
        
        try:
            if selection == 'npm' and self._command_exists('npm'):
                self.menu.show_info("📦 Ejecutando npm install...")
                subprocess.run(['npm', 'install'], check=True)
                self.menu.show_success("✅ Dependencias instaladas con npm")
                
            elif selection == 'yarn' and self._command_exists('yarn'):
                self.menu.show_info("🧶 Ejecutando yarn install...")
                subprocess.run(['yarn', 'install'], check=True)
                self.menu.show_success("✅ Dependencias instaladas con yarn")
                
            elif selection == 'pnpm' and self._command_exists('pnpm'):
                self.menu.show_info("⚡ Ejecutando pnpm install...")
                subprocess.run(['pnpm', 'install'], check=True)
                self.menu.show_success("✅ Dependencias instaladas con pnpm")
                
            else:
                self.menu.show_error(f"❌ {selection} no está instalado")
                
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"Error instalando dependencias: {e}")
    
    def _create_python_structure(self):
        """Crea estructura básica de proyecto Python."""
        self.menu.clear_screen()
        
        try:
            # Crear directorios
            directories = ['src', 'tests', 'docs']
            for directory in directories:
                (self.current_dir / directory).mkdir(exist_ok=True)
            
            # Crear archivos básicos
            files = {
                'README.md': '# Proyecto Python\n\nDescripción del proyecto.\n',
                'requirements.txt': '# Dependencias del proyecto\n',
                'main.py': 'from src import main\n\nif __name__ == "__main__":\n    main()\n',
                'src/__init__.py': '',
                'src/main.py': 'def main():\n    print("¡Hola, mundo!")\n',
                'tests/__init__.py': '',
                'tests/test_main.py': 'import unittest\nfrom src.main import main\n\nclass TestMain(unittest.TestCase):\n    def test_main(self):\n        # Agregar tests aquí\n        pass\n'
            }
            
            for file_path, content in files.items():
                file_full_path = self.current_dir / file_path
                file_full_path.parent.mkdir(parents=True, exist_ok=True)
                file_full_path.write_text(content, encoding='utf-8')
            
            self.menu.show_success("✅ Estructura de proyecto Python creada")
            self.menu.show_info("📁 Directorios creados: src/, tests/, docs/")
            self.menu.show_info("📄 Archivos creados: README.md, requirements.txt, main.py, etc.")
            
        except Exception as e:
            self.menu.show_error(f"Error creando estructura Python: {e}")
    
    def _local_server(self):
        """Lanza servidor local de desarrollo."""
        self.menu.clear_screen()
        
        servers = [
            {'name': '🐍 Python HTTP Server (puerto 8000)', 'value': 'python'},
            {'name': '📦 Node.js Express (crear proyecto)', 'value': 'node'},
            {'name': '⚛️ React Development Server', 'value': 'react'},
            {'name': '🌐 Servidor PHP (si disponible)', 'value': 'php'}
        ]
        
        selection = self.menu.show_menu(servers, "🌐 Selecciona tipo de servidor:")
        
        if not selection or selection == 'exit':
            return
        
        try:
            if selection == 'python':
                self.menu.show_info("🐍 Iniciando servidor Python en puerto 8000...")
                self.menu.show_info("🌐 Accede a: http://localhost:8000")
                self.menu.show_warning("⚠️ Presiona Ctrl+C para detener el servidor")
                subprocess.run([sys.executable, '-m', 'http.server', '8000'])
                
            elif selection == 'node':
                if self._command_exists('npx'):
                    self.menu.show_info("📦 Creando proyecto React con TypeScript...")
                    subprocess.run(['npx', 'create-react-app', '.', '--template', 'typescript'], check=True)
                    self.menu.show_success("✅ Proyecto React creado")
                else:
                    self.menu.show_error("❌ npx no está disponible")
                    
            elif selection == 'react':
                if (self.current_dir / 'package.json').exists():
                    self.menu.show_info("⚛️ Iniciando servidor de desarrollo React...")
                    subprocess.run(['npm', 'start'])
                else:
                    self.menu.show_error("❌ No se encontró un proyecto React válido")
                    
            elif selection == 'php':
                if self._command_exists('php'):
                    self.menu.show_info("🌐 Iniciando servidor PHP en puerto 8080...")
                    self.menu.show_info("🌐 Accede a: http://localhost:8080")
                    subprocess.run(['php', '-S', 'localhost:8080'])
                else:
                    self.menu.show_error("❌ PHP no está instalado")
                    
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"Error iniciando servidor: {e}")
        except KeyboardInterrupt:
            self.menu.show_info("\n🛑 Servidor detenido")
    
    def _open_powershell(self):
        """Abre PowerShell en el directorio actual."""
        self.menu.clear_screen()
        
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen([
                    'powershell', '-NoExit', '-Command', 
                    f"cd '{self.current_dir}'"
                ])
                self.menu.show_success("✅ PowerShell abierto en directorio actual")
            else:  # Linux/macOS
                # Abrir terminal nativo
                if self._command_exists('gnome-terminal'):
                    subprocess.Popen(['gnome-terminal', '--working-directory', str(self.current_dir)])
                elif self._command_exists('xterm'):
                    subprocess.Popen(['xterm'], cwd=str(self.current_dir))
                else:
                    self.menu.show_warning("⚠️ No se pudo detectar un emulador de terminal")
                    
        except Exception as e:
            self.menu.show_error(f"Error abriendo terminal: {e}")
    
    def _git_status(self):
        """Muestra estado de Git y commits recientes."""
        self.menu.clear_screen()
        
        if not (self.current_dir / '.git').exists():
            self.menu.show_error("❌ No es un repositorio Git")
            return
        
        if not self._command_exists('git'):
            self.menu.show_error("❌ Git no está instalado")
            return
        
        try:
            # Git status
            self.menu.console.print("[bold cyan]📊 Estado del repositorio:[/bold cyan]")
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                status_lines = result.stdout.strip().split('\n')
                table = Table(title="📁 Archivos modificados", box=box.SIMPLE)
                table.add_column("Estado", style="yellow", width=8)
                table.add_column("Archivo", style="white")
                
                for line in status_lines:
                    if len(line) >= 3:
                        status = line[:2]
                        file_name = line[3:]
                        status_desc = self._get_git_status_description(status)
                        table.add_row(status_desc, file_name)
                
                self.menu.console.print(table)
            else:
                self.menu.show_success("✅ No hay cambios pendientes")
            
            # Commits recientes
            self.menu.console.print("\n[bold cyan]📝 Commits recientes:[/bold cyan]")
            result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                  capture_output=True, text=True, check=True)
            
            if result.stdout.strip():
                commits = result.stdout.strip().split('\n')
                for i, commit in enumerate(commits, 1):
                    self.menu.console.print(f"  {i}. {commit}")
            else:
                self.menu.show_info("ℹ️ No hay commits en el repositorio")
                
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"Error consultando Git: {e}")
    
    def _git_push(self):
        """Realiza add, commit y push rápido."""
        self.menu.clear_screen()
        
        if not (self.current_dir / '.git').exists():
            self.menu.show_error("❌ No es un repositorio Git")
            return
        
        if not self._command_exists('git'):
            self.menu.show_error("❌ Git no está instalado")
            return
        
        # Solicitar mensaje de commit
        commit_message = self.menu.show_input("💬 Mensaje del commit:", "Update files")
        
        if not commit_message:
            self.menu.show_warning("⚠️ Commit cancelado")
            return
        
        try:
            # git add .
            self.menu.show_info("📦 Agregando archivos...")
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
            
            # git commit
            self.menu.show_info("💾 Creando commit...")
            subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True)
            
            # git push
            self.menu.show_info("🚀 Haciendo push...")
            result = subprocess.run(['git', 'push'], check=True, capture_output=True, text=True)
            
            self.menu.show_success("✅ Push completado exitosamente!")
            
        except subprocess.CalledProcessError as e:
            if "no changes added to commit" in str(e):
                self.menu.show_warning("⚠️ No hay cambios para commitear")
            elif "no upstream branch" in str(e):
                self.menu.show_warning("⚠️ No hay rama upstream configurada")
                if self.menu.show_confirmation("¿Configurar upstream automáticamente?"):
                    try:
                        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
                        self.menu.show_success("✅ Push con upstream configurado!")
                    except subprocess.CalledProcessError:
                        self.menu.show_error("❌ Error configurando upstream")
            else:
                self.menu.show_error(f"Error en Git: {e}")
    
    def _clean_cache(self):
        """Limpia cache de diferentes herramientas."""
        self.menu.clear_screen()
        
        cache_options = [
            {'name': '📦 npm cache', 'value': 'npm'},
            {'name': '🧶 yarn cache', 'value': 'yarn'},
            {'name': '🐍 pip cache', 'value': 'pip'},
            {'name': '⚡ pnpm cache', 'value': 'pnpm'},
            {'name': '🧹 Limpiar todo', 'value': 'all'}
        ]
        
        selection = self.menu.show_menu(cache_options, "🧹 ¿Qué cache quieres limpiar?")
        
        if not selection or selection == 'exit':
            return
        
        try:
            cleaned = []
            
            if selection in ['npm', 'all'] and self._command_exists('npm'):
                self.menu.show_info("🧹 Limpiando cache npm...")
                subprocess.run(['npm', 'cache', 'clean', '--force'], 
                             check=True, capture_output=True)
                cleaned.append('npm')
            
            if selection in ['yarn', 'all'] and self._command_exists('yarn'):
                self.menu.show_info("🧹 Limpiando cache yarn...")
                subprocess.run(['yarn', 'cache', 'clean'], 
                             check=True, capture_output=True)
                cleaned.append('yarn')
            
            if selection in ['pip', 'all'] and self._command_exists('pip'):
                self.menu.show_info("🧹 Limpiando cache pip...")
                subprocess.run([sys.executable, '-m', 'pip', 'cache', 'purge'], 
                             check=True, capture_output=True)
                cleaned.append('pip')
            
            if selection in ['pnpm', 'all'] and self._command_exists('pnpm'):
                self.menu.show_info("🧹 Limpiando cache pnpm...")
                subprocess.run(['pnpm', 'store', 'prune'], 
                             check=True, capture_output=True)
                cleaned.append('pnpm')
            
            if cleaned:
                self.menu.show_success(f"✅ Cache limpiado: {', '.join(cleaned)}")
            else:
                self.menu.show_warning("⚠️ No se encontraron herramientas para limpiar")
                
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"Error limpiando cache: {e}")
    
    def _extra_tools(self):
        """Herramientas adicionales de desarrollo."""
        self.menu.clear_screen()
        
        tools = [
            {'name': '🌐 Abrir en navegador (localhost)', 'value': 'browser'},
            {'name': '📋 Copiar ruta actual', 'value': 'copy_path'},
            {'name': '🔍 Explorar directorio', 'value': 'explorer'},
            {'name': '📊 Información del proyecto', 'value': 'project_info'},
            {'name': '🔧 Variables de entorno', 'value': 'env_vars'}
        ]
        
        selection = self.menu.show_menu(tools, "🔧 Herramientas adicionales:")
        
        if not selection or selection == 'exit':
            return
        
        if selection == 'browser':
            ports = ['3000', '8000', '8080', '5000']
            for port in ports:
                url = f"http://localhost:{port}"
                self.menu.show_info(f"🌐 Abriendo {url}")
                webbrowser.open(url)
        
        elif selection == 'copy_path':
            if os.name == 'nt':
                subprocess.run(['clip'], input=str(self.current_dir), text=True)
            else:
                subprocess.run(['xclip', '-selection', 'clipboard'], 
                             input=str(self.current_dir), text=True)
            self.menu.show_success("✅ Ruta copiada al portapapeles")
        
        elif selection == 'explorer':
            if os.name == 'nt':
                subprocess.run(['explorer', str(self.current_dir)])
            else:
                subprocess.run(['xdg-open', str(self.current_dir)])
            self.menu.show_success("📁 Explorador abierto")
        
        elif selection == 'project_info':
            self._show_project_info()
        
        elif selection == 'env_vars':
            self._show_env_vars()
    
    def _show_project_info(self):
        """Muestra información del proyecto actual."""
        self.menu.clear_screen()
        
        info_table = Table(title="📊 Información del Proyecto", box=box.DOUBLE)
        info_table.add_column("Propiedad", style="cyan", no_wrap=True)
        info_table.add_column("Valor", style="white")
        
        # Información básica
        info_table.add_row("📁 Directorio", str(self.current_dir))
        info_table.add_row("🏷️ Nombre", self.current_dir.name)
        
        # Detectar tipo de proyecto
        project_types = []
        if (self.current_dir / 'package.json').exists():
            project_types.append('Node.js')
        if (self.current_dir / 'requirements.txt').exists():
            project_types.append('Python')
        if (self.current_dir / 'composer.json').exists():
            project_types.append('PHP')
        if (self.current_dir / '.git').exists():
            project_types.append('Git')
        
        info_table.add_row("🔧 Tipo", ', '.join(project_types) if project_types else 'Desconocido')
        
        # Tamaño del directorio
        try:
            total_size = sum(f.stat().st_size for f in self.current_dir.rglob('*') if f.is_file())
            size_mb = total_size / (1024 * 1024)
            info_table.add_row("💾 Tamaño", f"{size_mb:.1f} MB")
        except Exception:
            info_table.add_row("💾 Tamaño", "No calculable")
        
        self.menu.console.print(info_table)
    
    def _show_env_vars(self):
        """Muestra variables de entorno relevantes para desarrollo."""
        self.menu.clear_screen()
        
        env_vars = [
            'PATH', 'PYTHONPATH', 'NODE_PATH', 'JAVA_HOME', 
            'ANDROID_HOME', 'FLUTTER_ROOT', 'GOPATH', 'CARGO_HOME'
        ]
        
        env_table = Table(title="🔧 Variables de Entorno", box=box.SIMPLE)
        env_table.add_column("Variable", style="cyan", no_wrap=True)
        env_table.add_column("Valor", style="white")
        
        for var in env_vars:
            value = os.environ.get(var, 'No definida')
            if len(value) > 80:
                value = value[:77] + '...'
            env_table.add_row(var, value)
        
        self.menu.console.print(env_table)
    
    def _get_git_status_description(self, status: str) -> str:
        """Convierte el código de estado de Git a descripción legible."""
        status_map = {
            '??': '🆕 Nuevo',
            ' M': '📝 Modificado',
            'M ': '✅ Staged',
            ' D': '🗑️ Eliminado',
            'D ': '🗑️ Staged del',
            'A ': '➕ Agregado',
            'AM': '📝 Mod+Staged',
            'MM': '📝 Mod+Mod'
        }
        return status_map.get(status, status)
    
    def _command_exists(self, command: str) -> bool:
        """Verifica si un comando existe en el sistema."""
        try:
            subprocess.run([command, '--version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


def main():
    """Función principal del módulo."""
    desarrollo_module = DesarrolloModule()
    desarrollo_module.main()


if __name__ == "__main__":
    main()
