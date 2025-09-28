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
        
        if self._open_vscode_improved():
            self.menu.show_success("✅ VS Code abierto correctamente")
        else:
            self.menu.show_error("❌ VS Code no está instalado o no se pudo abrir")
            self.menu.show_info("💡 Instala VS Code desde: https://code.visualstudio.com/")
    
    def _open_vscode_improved(self) -> bool:
        """Abre VS Code con mejor detección de rutas."""
        # Lista de comandos a probar en orden de preferencia
        vscode_commands = [
            'code.cmd',  # Comando que funciona en tu sistema
            'code',      # Comando directo
            rf"C:\Users\{os.environ.get('USERNAME', '')}\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
            rf"C:\Users\{os.environ.get('USERNAME', '')}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
        ]
        
        for vscode_cmd in vscode_commands:
            try:
                # Si es solo 'code' o 'code.cmd', intentar como comando
                if vscode_cmd in ['code', 'code.cmd']:
                    subprocess.run([vscode_cmd, '.'], check=True, timeout=10)
                    return True
                
                # Para rutas específicas, verificar que exista primero
                if os.path.exists(vscode_cmd):
                    subprocess.Popen([vscode_cmd, '.'])
                    return True
                    
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
            except Exception:
                continue
        
        return False
    
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
        """Abre PowerShell en el directorio actual con opciones mejoradas."""
        self.menu.clear_screen()
        
        # Verificar si Windows Terminal está disponible
        wt_available = self._command_exists('wt')
        
        # Ofrecer opciones de terminal
        terminal_options = [
            {'name': '🖥️ Terminal normal', 'value': 'normal'},
            {'name': '🧹 Terminal limpio (sin perfil)', 'value': 'clean'},
            {'name': '📦 CMD tradicional', 'value': 'cmd'}
        ]
        
        # Agregar opción de Windows Terminal si no está disponible
        if not wt_available:
            terminal_options.append({
                'name': '💡 Instalar Windows Terminal', 
                'value': 'install_wt',
                'description': 'Mejor experiencia con iconos y colores'
            })
        
        terminal_choice = self.menu.show_menu(terminal_options, "🖥️ Tipo de terminal:")
        
        if not terminal_choice or terminal_choice == 'exit':
            return
        
        try:
            if terminal_choice == 'install_wt':
                self._install_windows_terminal()
            elif terminal_choice == 'clean':
                success = self._open_clean_terminal()
            elif terminal_choice == 'cmd':
                success = self._open_cmd_terminal()
            else:
                success = self._open_terminal()
                
            if terminal_choice != 'install_wt':
                if success:
                    self.menu.show_success("✅ Terminal abierto en directorio actual")
                else:
                    self.menu.show_error("❌ No se pudo abrir el terminal")
                
        except Exception as e:
            self.menu.show_error(f"Error abriendo terminal: {e}")
    
    def _open_terminal(self) -> bool:
        """Abre terminal normal en el directorio actual."""
        try:
            if os.name == 'nt':
                # PRIORIDAD 1: Intentar Windows Terminal (wt command)
                if self._command_exists('wt'):
                    try:
                        # Si ya estamos en Windows Terminal, abrir nueva pestaña
                        if os.environ.get('WT_SESSION'):
                            subprocess.run([
                                'wt', 'new-tab', '--startingDirectory', str(self.current_dir)
                            ])
                        else:
                            # Si no estamos en WT, abrir nueva ventana
                            subprocess.run([
                                'wt', '-d', str(self.current_dir)
                            ])
                        return True
                    except FileNotFoundError:
                        pass
                
                # PRIORIDAD 2: Buscar Windows Terminal en ubicaciones comunes
                wt_executable = self._find_windows_terminal()
                if wt_executable:
                    try:
                        # Intentar abrir Windows Terminal directamente
                        if os.environ.get('WT_SESSION'):
                            subprocess.run([
                                wt_executable, 'new-tab', '--startingDirectory', str(self.current_dir)
                            ])
                        else:
                            subprocess.run([
                                wt_executable, '-d', str(self.current_dir)
                            ])
                        return True
                    except Exception:
                        pass
                
                # Intentar PowerShell 7 con configuración limpia
                try:
                    subprocess.Popen([
                        'pwsh', '-NoExit', '-NoLogo', '-Command', 
                        f"Set-Location '{self.current_dir}'"
                    ], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    return True
                except FileNotFoundError:
                    pass
                
                # Fallback a PowerShell 5.1 con configuración limpia
                try:
                    subprocess.Popen([
                        'powershell', '-NoExit', '-NoLogo', '-Command', 
                        f"Set-Location '{self.current_dir}'"
                    ], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    return True
                except Exception:
                    pass
                
                # Último recurso: CMD
                try:
                    subprocess.Popen([
                        'cmd', '/k', f'cd /d "{self.current_dir}" && title Desarrollo: {self.current_dir.name}'
                    ], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    return True
                except Exception:
                    pass
                    
            else:  # Linux/macOS
                terminals = ['gnome-terminal', 'xterm', 'konsole']
                for terminal in terminals:
                    try:
                        subprocess.Popen([terminal, '--working-directory', str(self.current_dir)])
                        return True
                    except FileNotFoundError:
                        continue
            
            return False
            
        except Exception:
            return False
    
    def _open_clean_terminal(self) -> bool:
        """Abre terminal sin cargar perfil para evitar conflictos."""
        try:
            if os.name == 'nt':
                # Intentar Windows Terminal con PowerShell sin perfil
                if self._command_exists('wt'):
                    try:
                        if os.environ.get('WT_SESSION'):
                            # Nueva pestaña en Windows Terminal existente
                            subprocess.run([
                                'wt', 'new-tab', '--startingDirectory', str(self.current_dir),
                                'pwsh', '-NoProfile', '-NoLogo', '-Command',
                                f"Set-Location '{self.current_dir}'; Write-Host 'Terminal limpio - Desarrollo: {self.current_dir.name}' -ForegroundColor Cyan"
                            ])
                        else:
                            # Nueva ventana de Windows Terminal
                            subprocess.run([
                                'wt', '-d', str(self.current_dir),
                                'pwsh', '-NoProfile', '-NoLogo', '-Command',
                                f"Set-Location '{self.current_dir}'; Write-Host 'Terminal limpio - Desarrollo: {self.current_dir.name}' -ForegroundColor Cyan"
                            ])
                        return True
                    except FileNotFoundError:
                        pass
                
                # Fallback: PowerShell 7 sin perfil en ventana separada
                try:
                    subprocess.Popen([
                        'pwsh', '-NoProfile', '-NoExit', '-NoLogo', '-Command', 
                        f"Set-Location '{self.current_dir}'; Write-Host 'Terminal limpio - Desarrollo: {self.current_dir.name}' -ForegroundColor Cyan"
                    ], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    return True
                except FileNotFoundError:
                    pass
                
                # Fallback a PowerShell 5.1 sin perfil
                try:
                    subprocess.Popen([
                        'powershell', '-NoProfile', '-NoExit', '-NoLogo', '-Command', 
                        f"Set-Location '{self.current_dir}'; Write-Host 'Terminal limpio - Desarrollo: {self.current_dir.name}' -ForegroundColor Cyan"
                    ], creationflags=subprocess.CREATE_NEW_CONSOLE)
                    return True
                except Exception:
                    return False
            
            return False
            
        except Exception:
            return False
    
    def _open_cmd_terminal(self) -> bool:
        """Abre CMD tradicional (más estable)."""
        try:
            if os.name == 'nt':
                # Intentar Windows Terminal con CMD
                if self._command_exists('wt'):
                    try:
                        if os.environ.get('WT_SESSION'):
                            # Nueva pestaña CMD en Windows Terminal existente
                            subprocess.run([
                                'wt', 'new-tab', '--startingDirectory', str(self.current_dir),
                                'cmd', '/k', f'title Desarrollo: {self.current_dir.name} && echo Directorio de desarrollo: {self.current_dir}'
                            ])
                        else:
                            # Nueva ventana de Windows Terminal con CMD
                            subprocess.run([
                                'wt', '-d', str(self.current_dir),
                                'cmd', '/k', f'title Desarrollo: {self.current_dir.name} && echo Directorio de desarrollo: {self.current_dir}'
                            ])
                        return True
                    except FileNotFoundError:
                        pass
                
                # Fallback: CMD en ventana separada
                subprocess.Popen([
                    'cmd', '/k', 
                    f'cd /d "{self.current_dir}" && title Desarrollo: {self.current_dir.name} && echo Directorio de desarrollo: {self.current_dir}'
                ], creationflags=subprocess.CREATE_NEW_CONSOLE)
                return True
            
            return False
            
        except Exception:
            return False
    
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
                         capture_output=True, check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            # Para VS Code, intentar variaciones del comando
            if command == 'code':
                try:
                    subprocess.run(['code.cmd', '--version'], capture_output=True, check=True, timeout=5)
                    return True
                except:
                    return self._check_vscode_installation()
            elif command == 'wt':
                # Para Windows Terminal, verificar de manera diferente
                try:
                    subprocess.run(['wt', '--help'], capture_output=True, check=True, timeout=5)
                    return True
                except:
                    return False
            return False
    
    def _check_vscode_installation(self) -> bool:
        """Verifica si VS Code está instalado en ubicaciones comunes."""
        import os
        
        # Rutas comunes donde se instala VS Code
        common_paths = [
            rf"C:\Users\{os.environ.get('USERNAME', '')}\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
            rf"C:\Users\{os.environ.get('USERNAME', '')}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
        ]
        
        for path in common_paths:
            try:
                if os.path.exists(path):
                    return True
                subprocess.run([path, '--version'], capture_output=True, check=True, timeout=5)
                return True
            except:
                continue
        
        return False
    
    def _find_windows_terminal(self) -> Optional[str]:
        """Busca Windows Terminal en ubicaciones comunes y retorna la ruta si lo encuentra."""
        # Primero intentar el comando wt
        if self._command_exists('wt'):
            return 'wt'
        
        # Buscar ejecutable en ubicaciones comunes
        wt_paths = [
            # Microsoft Store - usuario actual
            os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe'),
            # Microsoft Store - sistema (con wildcard)
            r'C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_*\wt.exe',
            # Instalación manual
            r'C:\Program Files\Windows Terminal\wt.exe',
            r'C:\Program Files (x86)\Windows Terminal\wt.exe',
            # Otras ubicaciones posibles
            os.path.expandvars(r'%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\Microsoft.WindowsTerminal_*\wt.exe'),
            os.path.expandvars(r'%PROGRAMFILES%\WindowsApps\Microsoft.WindowsTerminal_*\wt.exe')
        ]
        
        for wt_path in wt_paths:
            try:
                # Para rutas con wildcards, usar glob
                if '*' in wt_path:
                    import glob
                    matching_paths = glob.glob(wt_path)
                    if matching_paths:
                        # Ordenar para obtener la versión más reciente
                        matching_paths.sort(reverse=True)
                        wt_path = matching_paths[0]
                    else:
                        continue
                
                if os.path.exists(wt_path):
                    return wt_path
            except Exception:
                continue
        
        return None
    
    def _install_windows_terminal(self):
        """Ayuda al usuario a instalar Windows Terminal."""
        self.menu.clear_screen()
        
        self.menu.show_info("💡 Windows Terminal - Mejor experiencia de terminal")
        self.menu.console.print()
        
        # Mostrar beneficios
        benefits_text = """🎨 Beneficios de Windows Terminal:
• Pestañas múltiples en una sola ventana
• Iconos y colores personalizables  
• Mejor rendimiento y compatibilidad
• Soporte completo para UTF-8
• Temas y personalización avanzada"""
        
        benefits_panel = Panel(benefits_text, title="✨ ¿Por qué Windows Terminal?", border_style="cyan")
        self.menu.console.print(benefits_panel)
        self.menu.console.print()
        
        # Opciones de instalación
        install_options = [
            {'name': '🏪 Microsoft Store (recomendado)', 'value': 'store'},
            {'name': '📦 winget (línea de comandos)', 'value': 'winget'},
            {'name': '🌐 Descargar manualmente', 'value': 'manual'},
            {'name': '❌ Cancelar', 'value': 'cancel'}
        ]
        
        selection = self.menu.show_menu(install_options, "📥 ¿Cómo quieres instalar Windows Terminal?")
        
        if selection == 'store':
            self.menu.show_info("🏪 Abriendo Microsoft Store...")
            try:
                subprocess.run(['start', 'ms-windows-store://pdp/?ProductId=9N0DX20HK701'], shell=True)
                self.menu.show_success("✅ Microsoft Store abierto")
                self.menu.show_info("💡 Busca 'Windows Terminal' e instálalo")
            except Exception as e:
                self.menu.show_error(f"Error abriendo Store: {e}")
        
        elif selection == 'winget':
            if self._command_exists('winget'):
                self.menu.show_info("📦 Instalando Windows Terminal con winget...")
                try:
                    result = subprocess.run(['winget', 'install', '--id=Microsoft.WindowsTerminal', '-e'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        self.menu.show_success("✅ Windows Terminal instalado correctamente")
                        self.menu.show_info("🔄 Reinicia NooxCLI para usar Windows Terminal")
                    else:
                        self.menu.show_error("❌ Error instalando con winget")
                        self.menu.show_info("💡 Prueba con Microsoft Store")
                except Exception as e:
                    self.menu.show_error(f"Error ejecutando winget: {e}")
            else:
                self.menu.show_error("❌ winget no está disponible")
                self.menu.show_info("💡 Usa Microsoft Store en su lugar")
        
        elif selection == 'manual':
            self.menu.show_info("🌐 Abriendo página de descarga...")
            try:
                webbrowser.open('https://github.com/microsoft/terminal/releases')
                self.menu.show_success("✅ Página de descarga abierta")
                self.menu.show_info("💡 Descarga la última versión (.msixbundle)")
            except Exception as e:
                self.menu.show_error(f"Error abriendo navegador: {e}")
        
        elif selection == 'cancel':
            self.menu.show_info("ℹ️ Instalación cancelada")
        
        self.menu.console.print()
        self.menu.show_info("💡 Después de instalar, reinicia NooxCLI para mejor experiencia")


def main():
    """Función principal del módulo."""
    desarrollo_module = DesarrolloModule()
    desarrollo_module.main()


if __name__ == "__main__":
    main()
