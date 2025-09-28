"""
Módulo de Sistema - NooxCLI
Migrado desde sistema.bat con interfaz interactiva mejorada
Herramientas de administración del sistema: información, procesos, red, disco, etc.
"""

import os
import sys
import subprocess
import platform
import tempfile
import shutil
import webbrowser
import socket
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from ..menu import NooxMenu
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

try:
    import psutil
except ImportError:
    psutil = None


@dataclass
class SystemInfo:
    hostname: str
    os_name: str
    os_version: str
    architecture: str
    total_memory: int
    available_memory: int
    cpu_count: int
    cpu_usage: float


@dataclass
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    status: str
    create_time: datetime


@dataclass
class DiskInfo:
    device: str
    mountpoint: str
    fstype: str
    total: int
    used: int
    free: int
    percent: float


@dataclass
class NetworkConnection:
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    status: str
    protocol: str


class SistemaModule:
    """Módulo de herramientas de administración del sistema."""
    
    def __init__(self):
        self.menu = NooxMenu("Sistema - NooxCLI")
        
    def main(self):
        """Función principal del módulo de sistema."""
        while True:
            self.menu.show_banner()
            
            # Mostrar información contextual
            self.menu.show_info(f"💻 Sistema: {platform.system()} {platform.release()}")
            self.menu.console.print()
            
            # Menú principal de sistema
            choices = [
                {
                    'name': '💻 Información del sistema',
                    'value': 'sysinfo',
                    'description': 'Ver información completa del sistema'
                },
                {
                    'name': '⚙️ Procesos en ejecución',
                    'value': 'processes',
                    'description': 'Gestionar procesos del sistema'
                },
                {
                    'name': '🌐 Uso de red',
                    'value': 'network',
                    'description': 'Monitorear conexiones de red'
                },
                {
                    'name': '💾 Espacio en disco',
                    'value': 'disk',
                    'description': 'Ver uso de almacenamiento'
                },
                {
                    'name': '🔧 Servicios Windows',
                    'value': 'services',
                    'description': 'Gestionar servicios del sistema'
                },
                {
                    'name': '📋 Variables de entorno',
                    'value': 'env_vars',
                    'description': 'Ver y gestionar variables'
                },
                {
                    'name': '🧹 Limpiar temporales',
                    'value': 'cleanup',
                    'description': 'Limpiar archivos temporales'
                },
                {
                    'name': '🛠️ Herramientas sistema',
                    'value': 'tools',
                    'description': 'Abrir herramientas del sistema'
                },
                {
                    'name': '🌍 Diagnóstico de red',
                    'value': 'network_diag',
                    'description': 'Herramientas de diagnóstico'
                }
            ]
            
            selection = self.menu.show_menu(choices, "🛠️ ¿Qué herramienta del sistema necesitas?")
            
            if not selection or selection == 'exit':
                break
            
            self._handle_selection(selection)
    
    def _handle_selection(self, selection: str):
        """Maneja la selección del usuario."""
        handlers = {
            'sysinfo': self._show_system_info,
            'processes': self._show_processes,
            'network': self._show_network,
            'disk': self._show_disk_usage,
            'services': self._show_services,
            'env_vars': self._show_env_vars,
            'cleanup': self._cleanup_temp_files,
            'tools': self._open_system_tools,
            'network_diag': self._network_diagnostics
        }
        
        if selection in handlers:
            try:
                handlers[selection]()
            except Exception as e:
                self.menu.show_error(f"Error ejecutando {selection}: {e}")
            self.menu.pause()
    
    def _show_system_info(self):
        """Muestra información completa del sistema."""
        self.menu.clear_screen()
        
        try:
            # Intentar obtener información usando systeminfo primero
            system_info = self._get_system_info()
            
            if system_info:
                # Crear tabla con información del sistema
                info_table = Table(title="💻 Información del Sistema", box=box.DOUBLE)
                info_table.add_column("Propiedad", style="cyan", no_wrap=True)
                info_table.add_column("Valor", style="white")
                
                info_table.add_row("🏷️ Nombre del equipo", system_info.hostname)
                info_table.add_row("💿 Sistema operativo", system_info.os_name)
                info_table.add_row("📋 Versión", system_info.os_version)
                info_table.add_row("🏗️ Arquitectura", system_info.architecture)
                info_table.add_row("🧠 Procesadores", str(system_info.cpu_count))
                info_table.add_row("⚡ Uso de CPU", f"{system_info.cpu_usage:.1f}%")
                info_table.add_row("💾 Memoria total", self._format_bytes(system_info.total_memory))
                info_table.add_row("💚 Memoria disponible", self._format_bytes(system_info.available_memory))
                
                memory_used = system_info.total_memory - system_info.available_memory
                memory_percent = (memory_used / system_info.total_memory) * 100
                info_table.add_row("📊 Uso de memoria", f"{memory_percent:.1f}%")
                
                self.menu.console.print(info_table)
                
                # Mostrar información adicional si está disponible
                if psutil:
                    self._show_additional_system_info()
                    
            else:
                self.menu.show_error("❌ No se pudo obtener información del sistema")
                
        except Exception as e:
            self.menu.show_error(f"Error obteniendo información del sistema: {e}")
    
    def _get_system_info(self) -> Optional[SystemInfo]:
        """Obtiene información del sistema usando systeminfo y psutil como fallback."""
        try:
            # Intentar usar systeminfo en Windows
            if os.name == 'nt':
                return self._get_system_info_windows()
            else:
                return self._get_system_info_fallback()
        except Exception:
            return self._get_system_info_fallback()
    
    def _get_system_info_windows(self) -> Optional[SystemInfo]:
        """Obtiene información del sistema usando systeminfo en Windows."""
        try:
            result = subprocess.run(['systeminfo'], capture_output=True, text=True, check=True, encoding='utf-8')
            return self._parse_systeminfo(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError, UnicodeDecodeError):
            return self._get_system_info_fallback()
    
    def _parse_systeminfo(self, output: str) -> Optional[SystemInfo]:
        """Parsea la salida del comando systeminfo."""
        try:
            lines = output.split('\n')
            info = {}
            
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            
            # Extraer información relevante
            hostname = info.get('Host Name', platform.node())
            os_name = info.get('OS Name', platform.system())
            os_version = info.get('OS Version', platform.release())
            architecture = info.get('System Type', platform.machine())
            
            # Memoria total
            total_memory_str = info.get('Total Physical Memory', '0')
            total_memory = self._parse_memory_string(total_memory_str)
            
            # Usar psutil para información dinámica si está disponible
            if psutil:
                cpu_count = psutil.cpu_count()
                cpu_usage = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                available_memory = memory.available
                if total_memory == 0:
                    total_memory = memory.total
            else:
                cpu_count = os.cpu_count() or 1
                cpu_usage = 0.0
                available_memory = 0
                if total_memory == 0:
                    total_memory = 0
            
            return SystemInfo(
                hostname=hostname,
                os_name=os_name,
                os_version=os_version,
                architecture=architecture,
                total_memory=total_memory,
                available_memory=available_memory,
                cpu_count=cpu_count,
                cpu_usage=cpu_usage
            )
            
        except Exception:
            return self._get_system_info_fallback()
    
    def _get_system_info_fallback(self) -> Optional[SystemInfo]:
        """Obtiene información del sistema usando métodos alternativos de Python."""
        try:
            hostname = platform.node()
            os_name = platform.system()
            os_version = platform.release()
            architecture = platform.machine()
            cpu_count = os.cpu_count() or 1
            
            if psutil:
                cpu_usage = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                total_memory = memory.total
                available_memory = memory.available
            else:
                cpu_usage = 0.0
                total_memory = 0
                available_memory = 0
            
            return SystemInfo(
                hostname=hostname,
                os_name=os_name,
                os_version=os_version,
                architecture=architecture,
                total_memory=total_memory,
                available_memory=available_memory,
                cpu_count=cpu_count,
                cpu_usage=cpu_usage
            )
            
        except Exception as e:
            self.menu.show_error(f"Error obteniendo información del sistema: {e}")
            return None
    
    def _parse_memory_string(self, memory_str: str) -> int:
        """Convierte string de memoria a bytes."""
        try:
            # Remover caracteres no numéricos excepto puntos y comas
            clean_str = ''.join(c for c in memory_str if c.isdigit() or c in '.,')
            if not clean_str:
                return 0
            
            # Convertir a número (asumir MB si no hay unidad)
            number = float(clean_str.replace(',', ''))
            
            # Detectar unidad en el string original
            memory_str_upper = memory_str.upper()
            if 'GB' in memory_str_upper:
                return int(number * 1024 * 1024 * 1024)
            elif 'MB' in memory_str_upper:
                return int(number * 1024 * 1024)
            elif 'KB' in memory_str_upper:
                return int(number * 1024)
            else:
                # Asumir MB por defecto
                return int(number * 1024 * 1024)
                
        except Exception:
            return 0
    
    def _show_additional_system_info(self):
        """Muestra información adicional del sistema usando psutil."""
        if not psutil:
            return
        
        try:
            self.menu.console.print("\n[bold cyan]📊 Información Adicional:[/bold cyan]")
            
            # Información de CPU
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                self.menu.console.print(f"  🔥 Frecuencia CPU: {cpu_freq.current:.0f} MHz")
            
            # Información de arranque
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            self.menu.console.print(f"  ⏰ Tiempo de arranque: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.menu.console.print(f"  ⏱️ Tiempo activo: {str(uptime).split('.')[0]}")
            
            # Número de procesos
            process_count = len(psutil.pids())
            self.menu.console.print(f"  ⚙️ Procesos activos: {process_count}")
            
        except Exception as e:
            self.menu.show_warning(f"⚠️ No se pudo obtener información adicional: {e}")
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Formatea bytes en unidades legibles."""
        if bytes_value == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = bytes_value
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.1f} {units[unit_index]}"
    
    def _show_processes(self):
        """Muestra y gestiona procesos del sistema."""
        if not psutil:
            self.menu.show_error("❌ psutil no está disponible. Instala con: pip install psutil")
            return
        
        while True:
            self.menu.clear_screen()
            
            # Submenú de procesos
            choices = [
                {
                    'name': '📋 Ver todos los procesos',
                    'value': 'list_all',
                    'description': 'Mostrar todos los procesos activos'
                },
                {
                    'name': '🔍 Buscar proceso',
                    'value': 'search',
                    'description': 'Buscar proceso por nombre'
                },
                {
                    'name': '💾 Procesos por memoria',
                    'value': 'by_memory',
                    'description': 'Ordenar por uso de memoria'
                },
                {
                    'name': '⚡ Procesos por CPU',
                    'value': 'by_cpu',
                    'description': 'Ordenar por uso de CPU'
                },
                {
                    'name': '🔴 Terminar proceso',
                    'value': 'kill',
                    'description': 'Terminar proceso por PID'
                }
            ]
            
            selection = self.menu.show_menu(choices, "⚙️ ¿Qué quieres hacer con los procesos?")
            
            if not selection or selection == 'exit':
                break
            
            try:
                if selection == 'list_all':
                    self._list_processes()
                elif selection == 'search':
                    self._search_processes()
                elif selection == 'by_memory':
                    self._list_processes_by_memory()
                elif selection == 'by_cpu':
                    self._list_processes_by_cpu()
                elif selection == 'kill':
                    self._kill_process()
            except Exception as e:
                self.menu.show_error(f"Error en gestión de procesos: {e}")
            
            if selection != 'kill':  # No pausar después de terminar proceso
                self.menu.pause()
    
    def _get_process_list(self, limit: int = 50) -> List[ProcessInfo]:
        """Obtiene lista de procesos del sistema."""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'create_time']):
                try:
                    pinfo = proc.info
                    if pinfo['pid'] == 0:  # Saltar proceso del sistema
                        continue
                    
                    processes.append(ProcessInfo(
                        pid=pinfo['pid'],
                        name=pinfo['name'] or 'N/A',
                        cpu_percent=pinfo['cpu_percent'] or 0.0,
                        memory_percent=pinfo['memory_percent'] or 0.0,
                        status=pinfo['status'] or 'unknown',
                        create_time=datetime.fromtimestamp(pinfo['create_time']) if pinfo['create_time'] else datetime.now()
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            self.menu.show_error(f"Error obteniendo procesos: {e}")
        
        return processes[:limit]
    
    def _list_processes(self):
        """Lista todos los procesos activos."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Obteniendo procesos...", total=None)
            processes = self._get_process_list(100)
        
        if not processes:
            self.menu.show_warning("⚠️ No se encontraron procesos")
            return
        
        # Crear tabla de procesos
        proc_table = Table(title="⚙️ Procesos del Sistema", box=box.DOUBLE)
        proc_table.add_column("PID", style="cyan", no_wrap=True, width=8)
        proc_table.add_column("Nombre", style="white", width=25)
        proc_table.add_column("CPU %", style="yellow", justify="right", width=8)
        proc_table.add_column("Memoria %", style="green", justify="right", width=10)
        proc_table.add_column("Estado", style="blue", width=12)
        proc_table.add_column("Inicio", style="magenta", width=16)
        
        for proc in processes:
            # Formatear tiempo de inicio
            start_time = proc.create_time.strftime("%H:%M:%S")
            
            # Colorear según uso de recursos
            cpu_style = "red" if proc.cpu_percent > 50 else "yellow" if proc.cpu_percent > 10 else "white"
            mem_style = "red" if proc.memory_percent > 50 else "yellow" if proc.memory_percent > 10 else "white"
            
            proc_table.add_row(
                str(proc.pid),
                proc.name[:24],
                f"[{cpu_style}]{proc.cpu_percent:.1f}[/{cpu_style}]",
                f"[{mem_style}]{proc.memory_percent:.1f}[/{mem_style}]",
                proc.status,
                start_time
            )
        
        self.menu.console.print(proc_table)
        self.menu.console.print(f"\n[cyan]📊 Total de procesos mostrados: {len(processes)}[/cyan]")
    
    def _search_processes(self):
        """Busca procesos por nombre."""
        search_term = self.menu.get_input("🔍 Ingresa el nombre del proceso a buscar")
        if not search_term:
            return
        
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Buscando procesos...", total=None)
            all_processes = self._get_process_list(500)
        
        # Filtrar procesos que coincidan
        matching_processes = [
            proc for proc in all_processes 
            if search_term.lower() in proc.name.lower()
        ]
        
        if not matching_processes:
            self.menu.show_warning(f"⚠️ No se encontraron procesos con '{search_term}'")
            return
        
        # Mostrar resultados
        proc_table = Table(title=f"🔍 Procesos que contienen '{search_term}'", box=box.DOUBLE)
        proc_table.add_column("PID", style="cyan", no_wrap=True)
        proc_table.add_column("Nombre", style="white")
        proc_table.add_column("CPU %", style="yellow", justify="right")
        proc_table.add_column("Memoria %", style="green", justify="right")
        proc_table.add_column("Estado", style="blue")
        
        for proc in matching_processes:
            proc_table.add_row(
                str(proc.pid),
                proc.name,
                f"{proc.cpu_percent:.1f}",
                f"{proc.memory_percent:.1f}",
                proc.status
            )
        
        self.menu.console.print(proc_table)
        self.menu.console.print(f"\n[cyan]📊 Procesos encontrados: {len(matching_processes)}[/cyan]")
    
    def _list_processes_by_memory(self):
        """Lista procesos ordenados por uso de memoria."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Analizando uso de memoria...", total=None)
            processes = self._get_process_list(50)
        
        # Ordenar por memoria descendente
        processes.sort(key=lambda x: x.memory_percent, reverse=True)
        
        proc_table = Table(title="💾 Procesos por Uso de Memoria", box=box.DOUBLE)
        proc_table.add_column("Ranking", style="cyan", no_wrap=True, width=8)
        proc_table.add_column("PID", style="cyan", no_wrap=True, width=8)
        proc_table.add_column("Nombre", style="white", width=25)
        proc_table.add_column("Memoria %", style="green", justify="right", width=10)
        proc_table.add_column("CPU %", style="yellow", justify="right", width=8)
        
        for i, proc in enumerate(processes[:20], 1):
            # Colorear según ranking
            rank_style = "red" if i <= 3 else "yellow" if i <= 10 else "white"
            mem_style = "red" if proc.memory_percent > 10 else "yellow" if proc.memory_percent > 5 else "white"
            
            proc_table.add_row(
                f"[{rank_style}]#{i}[/{rank_style}]",
                str(proc.pid),
                proc.name[:24],
                f"[{mem_style}]{proc.memory_percent:.1f}[/{mem_style}]",
                f"{proc.cpu_percent:.1f}"
            )
        
        self.menu.console.print(proc_table)
    
    def _list_processes_by_cpu(self):
        """Lista procesos ordenados por uso de CPU."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Analizando uso de CPU...", total=None)
            # Obtener medición de CPU más precisa
            for proc in psutil.process_iter():
                try:
                    proc.cpu_percent()  # Primera medición
                except:
                    pass
            
            # Esperar un momento para medición precisa
            import time
            time.sleep(1)
            
            processes = self._get_process_list(50)
        
        # Ordenar por CPU descendente
        processes.sort(key=lambda x: x.cpu_percent, reverse=True)
        
        proc_table = Table(title="⚡ Procesos por Uso de CPU", box=box.DOUBLE)
        proc_table.add_column("Ranking", style="cyan", no_wrap=True, width=8)
        proc_table.add_column("PID", style="cyan", no_wrap=True, width=8)
        proc_table.add_column("Nombre", style="white", width=25)
        proc_table.add_column("CPU %", style="yellow", justify="right", width=8)
        proc_table.add_column("Memoria %", style="green", justify="right", width=10)
        
        for i, proc in enumerate(processes[:20], 1):
            # Colorear según ranking y uso
            rank_style = "red" if i <= 3 else "yellow" if i <= 10 else "white"
            cpu_style = "red" if proc.cpu_percent > 50 else "yellow" if proc.cpu_percent > 10 else "white"
            
            proc_table.add_row(
                f"[{rank_style}]#{i}[/{rank_style}]",
                str(proc.pid),
                proc.name[:24],
                f"[{cpu_style}]{proc.cpu_percent:.1f}[/{cpu_style}]",
                f"{proc.memory_percent:.1f}"
            )
        
        self.menu.console.print(proc_table)
    
    def _kill_process(self):
        """Termina un proceso por PID."""
        pid_str = self.menu.get_input("🔴 Ingresa el PID del proceso a terminar")
        if not pid_str:
            return
        
        try:
            pid = int(pid_str)
        except ValueError:
            self.menu.show_error("❌ PID inválido. Debe ser un número")
            return
        
        try:
            # Verificar que el proceso existe
            proc = psutil.Process(pid)
            proc_name = proc.name()
            
            # Confirmar acción
            confirm = self.menu.get_confirmation(
                f"⚠️ ¿Estás seguro de terminar el proceso '{proc_name}' (PID: {pid})?"
            )
            
            if confirm:
                proc.terminate()
                
                # Esperar un momento y verificar si terminó
                import time
                time.sleep(2)
                
                if proc.is_running():
                    # Si no terminó, forzar
                    force = self.menu.get_confirmation(
                        "⚠️ El proceso no terminó normalmente. ¿Forzar terminación?"
                    )
                    if force:
                        proc.kill()
                        self.menu.show_success(f"✅ Proceso {proc_name} (PID: {pid}) terminado forzadamente")
                    else:
                        self.menu.show_warning("⚠️ Terminación cancelada")
                else:
                    self.menu.show_success(f"✅ Proceso {proc_name} (PID: {pid}) terminado correctamente")
            else:
                self.menu.show_info("ℹ️ Terminación cancelada")
                
        except psutil.NoSuchProcess:
            self.menu.show_error(f"❌ No existe un proceso con PID {pid}")
        except psutil.AccessDenied:
            self.menu.show_error(f"❌ Sin permisos para terminar el proceso {pid}")
        except Exception as e:
            self.menu.show_error(f"❌ Error terminando proceso: {e}")
        
        self.menu.pause()

    def _show_network(self):
        """Muestra información y conexiones de red."""
        while True:
            self.menu.clear_screen()
            
            # Submenú de red
            choices = [
                {
                    'name': '🌐 Conexiones activas',
                    'value': 'connections',
                    'description': 'Ver todas las conexiones de red'
                },
                {
                    'name': '📊 Estadísticas de red',
                    'value': 'stats',
                    'description': 'Ver estadísticas de tráfico'
                },
                {
                    'name': '🔍 Conexiones por puerto',
                    'value': 'by_port',
                    'description': 'Filtrar por puerto específico'
                },
                {
                    'name': '📡 Solo conexiones TCP',
                    'value': 'tcp_only',
                    'description': 'Mostrar solo conexiones TCP'
                },
                {
                    'name': '📢 Solo conexiones UDP',
                    'value': 'udp_only',
                    'description': 'Mostrar solo conexiones UDP'
                }
            ]
            
            selection = self.menu.show_menu(choices, "🌐 ¿Qué información de red necesitas?")
            
            if not selection or selection == 'exit':
                break
            
            try:
                if selection == 'connections':
                    self._show_all_connections()
                elif selection == 'stats':
                    self._show_network_stats()
                elif selection == 'by_port':
                    self._show_connections_by_port()
                elif selection == 'tcp_only':
                    self._show_tcp_connections()
                elif selection == 'udp_only':
                    self._show_udp_connections()
            except Exception as e:
                self.menu.show_error(f"Error en monitoreo de red: {e}")
            
            self.menu.pause()
    
    def _get_network_connections(self, kind: str = 'all') -> List[NetworkConnection]:
        """Obtiene conexiones de red del sistema."""
        connections = []
        
        if not psutil:
            # Fallback usando netstat
            return self._get_connections_netstat()
        
        try:
            # Usar psutil para obtener conexiones
            for conn in psutil.net_connections(kind=kind):
                if conn.laddr:
                    local_addr = conn.laddr.ip if conn.laddr.ip != '0.0.0.0' else 'localhost'
                    local_port = conn.laddr.port
                else:
                    local_addr = 'N/A'
                    local_port = 0
                
                if conn.raddr:
                    remote_addr = conn.raddr.ip
                    remote_port = conn.raddr.port
                else:
                    remote_addr = 'N/A'
                    remote_port = 0
                
                connections.append(NetworkConnection(
                    local_address=local_addr,
                    local_port=local_port,
                    remote_address=remote_addr,
                    remote_port=remote_port,
                    status=conn.status or 'N/A',
                    protocol=conn.type.name if hasattr(conn.type, 'name') else str(conn.type)
                ))
        except Exception as e:
            self.menu.show_warning(f"⚠️ Error con psutil, usando netstat: {e}")
            return self._get_connections_netstat()
        
        return connections
    
    def _get_connections_netstat(self) -> List[NetworkConnection]:
        """Obtiene conexiones usando netstat como fallback."""
        connections = []
        
        try:
            # Ejecutar netstat
            if os.name == 'nt':
                result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, check=True)
            else:
                result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True, check=True)
            
            lines = result.stdout.split('\n')
            
            for line in lines:
                if 'TCP' in line or 'UDP' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        protocol = parts[0]
                        local_addr_port = parts[1]
                        remote_addr_port = parts[2] if len(parts) > 2 else 'N/A:0'
                        status = parts[3] if len(parts) > 3 and protocol == 'TCP' else 'N/A'
                        
                        # Parsear direcciones y puertos
                        local_addr, local_port = self._parse_addr_port(local_addr_port)
                        remote_addr, remote_port = self._parse_addr_port(remote_addr_port)
                        
                        connections.append(NetworkConnection(
                            local_address=local_addr,
                            local_port=local_port,
                            remote_address=remote_addr,
                            remote_port=remote_port,
                            status=status,
                            protocol=protocol
                        ))
        except Exception as e:
            self.menu.show_error(f"Error ejecutando netstat: {e}")
        
        return connections
    
    def _parse_addr_port(self, addr_port: str) -> tuple:
        """Parsea dirección:puerto de netstat."""
        try:
            if ':' in addr_port:
                parts = addr_port.rsplit(':', 1)
                addr = parts[0] if parts[0] != '0.0.0.0' else 'localhost'
                port = int(parts[1])
                return addr, port
            else:
                return addr_port, 0
        except:
            return 'N/A', 0
    
    def _show_all_connections(self):
        """Muestra todas las conexiones de red."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Obteniendo conexiones de red...", total=None)
            connections = self._get_network_connections()
        
        if not connections:
            self.menu.show_warning("⚠️ No se encontraron conexiones de red")
            return
        
        # Crear tabla de conexiones
        conn_table = Table(title="🌐 Conexiones de Red Activas", box=box.DOUBLE)
        conn_table.add_column("Protocolo", style="cyan", width=8)
        conn_table.add_column("Dirección Local", style="green", width=20)
        conn_table.add_column("Puerto Local", style="green", justify="right", width=12)
        conn_table.add_column("Dirección Remota", style="yellow", width=20)
        conn_table.add_column("Puerto Remoto", style="yellow", justify="right", width=12)
        conn_table.add_column("Estado", style="blue", width=12)
        
        # Agrupar por protocolo para mejor visualización
        tcp_connections = [c for c in connections if 'TCP' in c.protocol.upper()]
        udp_connections = [c for c in connections if 'UDP' in c.protocol.upper()]
        
        # Mostrar conexiones TCP primero
        for conn in tcp_connections[:50]:  # Limitar para no saturar
            status_style = self._get_connection_status_style(conn.status)
            
            conn_table.add_row(
                conn.protocol,
                conn.local_address,
                str(conn.local_port),
                conn.remote_address,
                str(conn.remote_port) if conn.remote_port > 0 else 'N/A',
                f"[{status_style}]{conn.status}[/{status_style}]"
            )
        
        # Mostrar algunas conexiones UDP
        for conn in udp_connections[:20]:
            conn_table.add_row(
                conn.protocol,
                conn.local_address,
                str(conn.local_port),
                conn.remote_address,
                str(conn.remote_port) if conn.remote_port > 0 else 'N/A',
                f"[blue]{conn.status}[/blue]"
            )
        
        self.menu.console.print(conn_table)
        self.menu.console.print(f"\n[cyan]📊 TCP: {len(tcp_connections)} | UDP: {len(udp_connections)} | Total mostradas: {min(70, len(connections))}[/cyan]")
    
    def _get_connection_status_style(self, status: str) -> str:
        """Obtiene el estilo de color para el estado de conexión."""
        status_upper = status.upper()
        if status_upper == 'ESTABLISHED':
            return 'green'
        elif status_upper in ['LISTEN', 'LISTENING']:
            return 'blue'
        elif status_upper in ['TIME_WAIT', 'CLOSE_WAIT']:
            return 'yellow'
        elif status_upper in ['CLOSED', 'CLOSE']:
            return 'red'
        else:
            return 'white'
    
    def _show_network_stats(self):
        """Muestra estadísticas de tráfico de red."""
        if not psutil:
            self.menu.show_error("❌ psutil no está disponible para estadísticas de red")
            return
        
        self.menu.clear_screen()
        
        try:
            # Obtener estadísticas de red
            net_io = psutil.net_io_counters()
            
            # Crear tabla de estadísticas
            stats_table = Table(title="📊 Estadísticas de Tráfico de Red", box=box.DOUBLE)
            stats_table.add_column("Métrica", style="cyan", no_wrap=True)
            stats_table.add_column("Valor", style="white")
            
            stats_table.add_row("📤 Bytes enviados", self._format_bytes(net_io.bytes_sent))
            stats_table.add_row("📥 Bytes recibidos", self._format_bytes(net_io.bytes_recv))
            stats_table.add_row("📦 Paquetes enviados", f"{net_io.packets_sent:,}")
            stats_table.add_row("📦 Paquetes recibidos", f"{net_io.packets_recv:,}")
            stats_table.add_row("❌ Errores de entrada", f"{net_io.errin:,}")
            stats_table.add_row("❌ Errores de salida", f"{net_io.errout:,}")
            stats_table.add_row("🗑️ Paquetes descartados (in)", f"{net_io.dropin:,}")
            stats_table.add_row("🗑️ Paquetes descartados (out)", f"{net_io.dropout:,}")
            
            self.menu.console.print(stats_table)
            
            # Mostrar estadísticas por interfaz si está disponible
            try:
                net_io_per_nic = psutil.net_io_counters(pernic=True)
                if net_io_per_nic:
                    self.menu.console.print("\n[bold cyan]📡 Estadísticas por Interfaz:[/bold cyan]")
                    
                    for interface, stats in net_io_per_nic.items():
                        if stats.bytes_sent > 0 or stats.bytes_recv > 0:
                            self.menu.console.print(f"  🔌 {interface}:")
                            self.menu.console.print(f"    📤 Enviados: {self._format_bytes(stats.bytes_sent)}")
                            self.menu.console.print(f"    📥 Recibidos: {self._format_bytes(stats.bytes_recv)}")
            except:
                pass
                
        except Exception as e:
            self.menu.show_error(f"Error obteniendo estadísticas de red: {e}")
    
    def _show_connections_by_port(self):
        """Muestra conexiones filtradas por puerto."""
        port_str = self.menu.get_input("🔍 Ingresa el puerto a buscar")
        if not port_str:
            return
        
        try:
            port = int(port_str)
        except ValueError:
            self.menu.show_error("❌ Puerto inválido. Debe ser un número")
            return
        
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task(f"Buscando conexiones en puerto {port}...", total=None)
            connections = self._get_network_connections()
        
        # Filtrar por puerto
        matching_connections = [
            conn for conn in connections 
            if conn.local_port == port or conn.remote_port == port
        ]
        
        if not matching_connections:
            self.menu.show_warning(f"⚠️ No se encontraron conexiones en el puerto {port}")
            return
        
        # Mostrar resultados
        conn_table = Table(title=f"🔍 Conexiones en Puerto {port}", box=box.DOUBLE)
        conn_table.add_column("Protocolo", style="cyan")
        conn_table.add_column("Dirección Local", style="green")
        conn_table.add_column("Puerto Local", style="green", justify="right")
        conn_table.add_column("Dirección Remota", style="yellow")
        conn_table.add_column("Puerto Remoto", style="yellow", justify="right")
        conn_table.add_column("Estado", style="blue")
        
        for conn in matching_connections:
            status_style = self._get_connection_status_style(conn.status)
            
            conn_table.add_row(
                conn.protocol,
                conn.local_address,
                str(conn.local_port),
                conn.remote_address,
                str(conn.remote_port) if conn.remote_port > 0 else 'N/A',
                f"[{status_style}]{conn.status}[/{status_style}]"
            )
        
        self.menu.console.print(conn_table)
        self.menu.console.print(f"\n[cyan]📊 Conexiones encontradas: {len(matching_connections)}[/cyan]")
    
    def _show_tcp_connections(self):
        """Muestra solo conexiones TCP."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Obteniendo conexiones TCP...", total=None)
            connections = self._get_network_connections('tcp')
        
        if not connections:
            self.menu.show_warning("⚠️ No se encontraron conexiones TCP")
            return
        
        # Crear tabla de conexiones TCP
        conn_table = Table(title="📡 Conexiones TCP", box=box.DOUBLE)
        conn_table.add_column("Dirección Local", style="green", width=20)
        conn_table.add_column("Puerto", style="green", justify="right", width=8)
        conn_table.add_column("Dirección Remota", style="yellow", width=20)
        conn_table.add_column("Puerto", style="yellow", justify="right", width=8)
        conn_table.add_column("Estado", style="blue", width=12)
        
        for conn in connections:
            status_style = self._get_connection_status_style(conn.status)
            
            conn_table.add_row(
                conn.local_address,
                str(conn.local_port),
                conn.remote_address,
                str(conn.remote_port) if conn.remote_port > 0 else 'N/A',
                f"[{status_style}]{conn.status}[/{status_style}]"
            )
        
        self.menu.console.print(conn_table)
        self.menu.console.print(f"\n[cyan]📊 Total conexiones TCP: {len(connections)}[/cyan]")
    
    def _show_udp_connections(self):
        """Muestra solo conexiones UDP."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Obteniendo conexiones UDP...", total=None)
            connections = self._get_network_connections('udp')
        
        if not connections:
            self.menu.show_warning("⚠️ No se encontraron conexiones UDP")
            return
        
        # Crear tabla de conexiones UDP
        conn_table = Table(title="📢 Conexiones UDP", box=box.DOUBLE)
        conn_table.add_column("Dirección Local", style="green", width=25)
        conn_table.add_column("Puerto", style="green", justify="right", width=10)
        conn_table.add_column("Dirección Remota", style="yellow", width=25)
        conn_table.add_column("Puerto", style="yellow", justify="right", width=10)
        
        for conn in connections:
            conn_table.add_row(
                conn.local_address,
                str(conn.local_port),
                conn.remote_address if conn.remote_address != 'N/A' else '-',
                str(conn.remote_port) if conn.remote_port > 0 else '-'
            )
        
        self.menu.console.print(conn_table)
        self.menu.console.print(f"\n[cyan]📊 Total conexiones UDP: {len(connections)}[/cyan]")

    def _show_disk_usage(self):
        """Muestra información de uso de disco."""
        while True:
            self.menu.clear_screen()
            
            # Submenú de disco
            choices = [
                {
                    'name': '💾 Todas las unidades',
                    'value': 'all_drives',
                    'description': 'Ver información de todas las unidades'
                },
                {
                    'name': '📊 Uso detallado',
                    'value': 'detailed',
                    'description': 'Información detallada con gráficos'
                },
                {
                    'name': '⚠️ Unidades con poco espacio',
                    'value': 'low_space',
                    'description': 'Mostrar solo unidades con poco espacio'
                },
                {
                    'name': '🗂️ Archivos temporales',
                    'value': 'temp_files',
                    'description': 'Ver tamaño de archivos temporales'
                },
                {
                    'name': '🔍 Analizar directorio',
                    'value': 'analyze_dir',
                    'description': 'Analizar uso de espacio en directorio'
                }
            ]
            
            selection = self.menu.show_menu(choices, "💾 ¿Qué información de disco necesitas?")
            
            if not selection or selection == 'exit':
                break
            
            try:
                if selection == 'all_drives':
                    self._show_all_drives()
                elif selection == 'detailed':
                    self._show_detailed_disk_usage()
                elif selection == 'low_space':
                    self._show_low_space_drives()
                elif selection == 'temp_files':
                    self._show_temp_files_size()
                elif selection == 'analyze_dir':
                    self._analyze_directory()
            except Exception as e:
                self.menu.show_error(f"Error en información de disco: {e}")
            
            self.menu.pause()
    
    def _get_disk_info(self) -> List[DiskInfo]:
        """Obtiene información de todas las unidades de disco."""
        disks = []
        
        try:
            if psutil:
                # Usar psutil para obtener información de particiones
                partitions = psutil.disk_partitions()
                
                for partition in partitions:
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        
                        disks.append(DiskInfo(
                            device=partition.device,
                            mountpoint=partition.mountpoint,
                            fstype=partition.fstype,
                            total=usage.total,
                            used=usage.used,
                            free=usage.free,
                            percent=(usage.used / usage.total) * 100 if usage.total > 0 else 0
                        ))
                    except (PermissionError, OSError):
                        # Saltar unidades no accesibles
                        continue
            else:
                # Fallback usando shutil para unidad actual
                usage = shutil.disk_usage('.')
                disks.append(DiskInfo(
                    device='Current Drive',
                    mountpoint='.',
                    fstype='Unknown',
                    total=usage.total,
                    used=usage.total - usage.free,
                    free=usage.free,
                    percent=((usage.total - usage.free) / usage.total) * 100 if usage.total > 0 else 0
                ))
        except Exception as e:
            self.menu.show_error(f"Error obteniendo información de disco: {e}")
        
        return disks
    
    def _show_all_drives(self):
        """Muestra información de todas las unidades."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Analizando unidades de disco...", total=None)
            disks = self._get_disk_info()
        
        if not disks:
            self.menu.show_warning("⚠️ No se encontraron unidades de disco")
            return
        
        # Crear tabla de unidades
        disk_table = Table(title="💾 Información de Unidades de Disco", box=box.DOUBLE)
        disk_table.add_column("Unidad", style="cyan", no_wrap=True, width=12)
        disk_table.add_column("Tipo", style="blue", width=10)
        disk_table.add_column("Tamaño Total", style="white", justify="right", width=12)
        disk_table.add_column("Usado", style="yellow", justify="right", width=12)
        disk_table.add_column("Libre", style="green", justify="right", width=12)
        disk_table.add_column("% Usado", style="red", justify="right", width=10)
        disk_table.add_column("Estado", style="white", width=10)
        
        for disk in disks:
            # Determinar color y estado según el porcentaje usado
            if disk.percent >= 90:
                percent_style = "red"
                status = "🔴 Crítico"
            elif disk.percent >= 80:
                percent_style = "yellow"
                status = "🟡 Advertencia"
            elif disk.percent >= 70:
                percent_style = "orange"
                status = "🟠 Atención"
            else:
                percent_style = "green"
                status = "🟢 Normal"
            
            disk_table.add_row(
                disk.device,
                disk.fstype,
                self._format_bytes(disk.total),
                self._format_bytes(disk.used),
                self._format_bytes(disk.free),
                f"[{percent_style}]{disk.percent:.1f}%[/{percent_style}]",
                status
            )
        
        self.menu.console.print(disk_table)
        
        # Mostrar resumen
        total_space = sum(disk.total for disk in disks)
        total_used = sum(disk.used for disk in disks)
        total_free = sum(disk.free for disk in disks)
        
        self.menu.console.print(f"\n[cyan]📊 Resumen Total:[/cyan]")
        self.menu.console.print(f"  💾 Espacio total: {self._format_bytes(total_space)}")
        self.menu.console.print(f"  📊 Espacio usado: {self._format_bytes(total_used)}")
        self.menu.console.print(f"  💚 Espacio libre: {self._format_bytes(total_free)}")
    
    def _show_detailed_disk_usage(self):
        """Muestra uso detallado de disco con gráficos."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Generando análisis detallado...", total=None)
            disks = self._get_disk_info()
        
        if not disks:
            self.menu.show_warning("⚠️ No se encontraron unidades de disco")
            return
        
        for disk in disks:
            # Crear panel para cada unidad
            self.menu.console.print(f"\n[bold cyan]💾 Unidad {disk.device}[/bold cyan]")
            
            # Crear barra de progreso visual
            bar_length = 40
            used_blocks = int((disk.percent / 100) * bar_length)
            free_blocks = bar_length - used_blocks
            
            # Colorear la barra según el porcentaje
            if disk.percent >= 90:
                bar_color = "red"
            elif disk.percent >= 80:
                bar_color = "yellow"
            else:
                bar_color = "green"
            
            bar = f"[{bar_color}]{'█' * used_blocks}[/{bar_color}]{'░' * free_blocks}"
            
            info_panel = Panel(
                f"📁 Punto de montaje: {disk.mountpoint}\n"
                f"🗂️ Sistema de archivos: {disk.fstype}\n"
                f"📊 Uso: {bar} {disk.percent:.1f}%\n"
                f"💾 Total: {self._format_bytes(disk.total)}\n"
                f"📊 Usado: {self._format_bytes(disk.used)}\n"
                f"💚 Libre: {self._format_bytes(disk.free)}",
                title=f"[bold]{disk.device}[/bold]",
                border_style="blue"
            )
            
            self.menu.console.print(info_panel)
    
    def _show_low_space_drives(self):
        """Muestra solo unidades con poco espacio libre."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Buscando unidades con poco espacio...", total=None)
            disks = self._get_disk_info()
        
        # Filtrar unidades con más del 70% de uso
        low_space_disks = [disk for disk in disks if disk.percent >= 70]
        
        if not low_space_disks:
            self.menu.show_success("✅ Todas las unidades tienen espacio suficiente")
            return
        
        # Mostrar advertencia
        self.menu.show_warning(f"⚠️ Se encontraron {len(low_space_disks)} unidades con poco espacio")
        
        # Crear tabla de unidades con poco espacio
        disk_table = Table(title="⚠️ Unidades con Poco Espacio", box=box.DOUBLE)
        disk_table.add_column("Unidad", style="cyan", no_wrap=True)
        disk_table.add_column("% Usado", style="red", justify="right")
        disk_table.add_column("Espacio Libre", style="green", justify="right")
        disk_table.add_column("Prioridad", style="white")
        
        for disk in sorted(low_space_disks, key=lambda x: x.percent, reverse=True):
            if disk.percent >= 90:
                priority = "🔴 CRÍTICO"
                priority_style = "red"
            elif disk.percent >= 80:
                priority = "🟡 ALTO"
                priority_style = "yellow"
            else:
                priority = "🟠 MEDIO"
                priority_style = "orange"
            
            disk_table.add_row(
                disk.device,
                f"{disk.percent:.1f}%",
                self._format_bytes(disk.free),
                f"[{priority_style}]{priority}[/{priority_style}]"
            )
        
        self.menu.console.print(disk_table)
        
        # Sugerencias
        self.menu.console.print("\n[bold cyan]💡 Sugerencias:[/bold cyan]")
        self.menu.console.print("  🧹 Ejecuta 'Limpiar temporales' para liberar espacio")
        self.menu.console.print("  📁 Revisa la carpeta de Descargas y Documentos")
        self.menu.console.print("  🗑️ Vacía la Papelera de reciclaje")
        self.menu.console.print("  💿 Considera mover archivos grandes a otra unidad")
    
    def _show_temp_files_size(self):
        """Muestra el tamaño de archivos temporales."""
        self.menu.clear_screen()
        
        temp_dirs = []
        
        # Directorios temporales comunes
        if os.name == 'nt':
            temp_dirs = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
                os.path.join(os.environ.get('WINDIR', ''), 'Temp'),
                tempfile.gettempdir()
            ]
        else:
            temp_dirs = [
                '/tmp',
                '/var/tmp',
                tempfile.gettempdir()
            ]
        
        # Remover duplicados y directorios vacíos
        temp_dirs = list(set([d for d in temp_dirs if d and os.path.exists(d)]))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Analizando archivos temporales...", total=len(temp_dirs))
            
            temp_table = Table(title="🗂️ Archivos Temporales", box=box.DOUBLE)
            temp_table.add_column("Directorio", style="cyan", width=40)
            temp_table.add_column("Archivos", style="yellow", justify="right")
            temp_table.add_column("Tamaño", style="green", justify="right")
            temp_table.add_column("Estado", style="white")
            
            total_size = 0
            total_files = 0
            
            for temp_dir in temp_dirs:
                try:
                    dir_size, file_count = self._calculate_directory_size(temp_dir)
                    total_size += dir_size
                    total_files += file_count
                    
                    if dir_size > 100 * 1024 * 1024:  # > 100MB
                        status = "🔴 Grande"
                    elif dir_size > 10 * 1024 * 1024:  # > 10MB
                        status = "🟡 Medio"
                    else:
                        status = "🟢 Pequeño"
                    
                    temp_table.add_row(
                        temp_dir,
                        f"{file_count:,}",
                        self._format_bytes(dir_size),
                        status
                    )
                except Exception as e:
                    temp_table.add_row(
                        temp_dir,
                        "Error",
                        "N/A",
                        f"❌ {str(e)[:20]}..."
                    )
                
                progress.advance(task)
        
        self.menu.console.print(temp_table)
        
        # Mostrar resumen
        self.menu.console.print(f"\n[cyan]📊 Resumen de Archivos Temporales:[/cyan]")
        self.menu.console.print(f"  📁 Total de archivos: {total_files:,}")
        self.menu.console.print(f"  💾 Tamaño total: {self._format_bytes(total_size)}")
        
        if total_size > 500 * 1024 * 1024:  # > 500MB
            self.menu.console.print(f"\n[yellow]💡 Considera limpiar archivos temporales para liberar {self._format_bytes(total_size)}[/yellow]")
    
    def _analyze_directory(self):
        """Analiza el uso de espacio en un directorio específico."""
        directory = self.menu.get_input("📁 Ingresa la ruta del directorio a analizar")
        if not directory:
            return
        
        if not os.path.exists(directory):
            self.menu.show_error(f"❌ El directorio '{directory}' no existe")
            return
        
        if not os.path.isdir(directory):
            self.menu.show_error(f"❌ '{directory}' no es un directorio")
            return
        
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task(f"Analizando {directory}...", total=None)
            
            try:
                # Analizar subdirectorios
                subdirs = []
                total_size = 0
                
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    if os.path.isdir(item_path):
                        try:
                            size, file_count = self._calculate_directory_size(item_path)
                            subdirs.append((item, size, file_count))
                            total_size += size
                        except:
                            continue
                
                # Ordenar por tamaño
                subdirs.sort(key=lambda x: x[1], reverse=True)
                
                # Mostrar resultados
                dir_table = Table(title=f"📁 Análisis de {directory}", box=box.DOUBLE)
                dir_table.add_column("Subdirectorio", style="cyan", width=30)
                dir_table.add_column("Archivos", style="yellow", justify="right")
                dir_table.add_column("Tamaño", style="green", justify="right")
                dir_table.add_column("% del Total", style="blue", justify="right")
                
                for name, size, file_count in subdirs[:20]:  # Top 20
                    percentage = (size / total_size) * 100 if total_size > 0 else 0
                    
                    dir_table.add_row(
                        name,
                        f"{file_count:,}",
                        self._format_bytes(size),
                        f"{percentage:.1f}%"
                    )
                
                self.menu.console.print(dir_table)
                self.menu.console.print(f"\n[cyan]📊 Tamaño total analizado: {self._format_bytes(total_size)}[/cyan]")
                
            except Exception as e:
                self.menu.show_error(f"Error analizando directorio: {e}")
    
    def _calculate_directory_size(self, directory: str) -> tuple:
        """Calcula el tamaño total y número de archivos en un directorio."""
        total_size = 0
        file_count = 0
        
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    try:
                        filepath = os.path.join(dirpath, filename)
                        total_size += os.path.getsize(filepath)
                        file_count += 1
                    except (OSError, IOError):
                        continue
        except (OSError, IOError):
            pass
        
        return total_size, file_count

    def _show_services(self):
        """Muestra y gestiona servicios de Windows."""
        if os.name != 'nt':
            self.menu.show_error("❌ La gestión de servicios solo está disponible en Windows")
            return
        
        while True:
            self.menu.clear_screen()
            
            # Submenú de servicios
            choices = [
                {
                    'name': '📋 Ver todos los servicios',
                    'value': 'all_services',
                    'description': 'Mostrar todos los servicios del sistema'
                },
                {
                    'name': '✅ Solo servicios en ejecución',
                    'value': 'running_only',
                    'description': 'Filtrar solo servicios activos'
                },
                {
                    'name': '🔍 Buscar servicio',
                    'value': 'search',
                    'description': 'Buscar servicio por nombre'
                },
                {
                    'name': '▶️ Iniciar servicio',
                    'value': 'start',
                    'description': 'Iniciar un servicio específico'
                },
                {
                    'name': '⏹️ Detener servicio',
                    'value': 'stop',
                    'description': 'Detener un servicio específico'
                },
                {
                    'name': '🔄 Reiniciar servicio',
                    'value': 'restart',
                    'description': 'Reiniciar un servicio específico'
                }
            ]
            
            selection = self.menu.show_menu(choices, "🔧 ¿Qué quieres hacer con los servicios?")
            
            if not selection or selection == 'exit':
                break
            
            try:
                if selection == 'all_services':
                    self._list_all_services()
                elif selection == 'running_only':
                    self._list_running_services()
                elif selection == 'search':
                    self._search_services()
                elif selection == 'start':
                    self._start_service()
                elif selection == 'stop':
                    self._stop_service()
                elif selection == 'restart':
                    self._restart_service()
            except Exception as e:
                self.menu.show_error(f"Error en gestión de servicios: {e}")
            
            self.menu.pause()
    
    def _get_services_list(self, running_only: bool = False) -> List[Dict[str, str]]:
        """Obtiene lista de servicios usando sc query."""
        services = []
        
        try:
            # Comando para obtener servicios
            if running_only:
                cmd = ['sc', 'query', 'state=', 'running']
            else:
                cmd = ['sc', 'query', 'state=', 'all']
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
            
            # Parsear la salida
            services_text = result.stdout
            service_blocks = services_text.split('\n\n')
            
            for block in service_blocks:
                if 'SERVICE_NAME:' in block:
                    service_info = {}
                    lines = block.strip().split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('SERVICE_NAME:'):
                            service_info['name'] = line.split(':', 1)[1].strip()
                        elif line.startswith('DISPLAY_NAME:'):
                            service_info['display_name'] = line.split(':', 1)[1].strip()
                        elif line.startswith('STATE'):
                            # Extraer estado de la línea STATE
                            parts = line.split()
                            if len(parts) >= 4:
                                service_info['state'] = parts[3]
                            else:
                                service_info['state'] = 'UNKNOWN'
                        elif line.startswith('TYPE'):
                            # Extraer tipo de servicio
                            parts = line.split()
                            if len(parts) >= 3:
                                service_info['type'] = ' '.join(parts[2:])
                            else:
                                service_info['type'] = 'UNKNOWN'
                    
                    # Solo agregar si tiene información básica
                    if 'name' in service_info and 'state' in service_info:
                        if 'display_name' not in service_info:
                            service_info['display_name'] = service_info['name']
                        if 'type' not in service_info:
                            service_info['type'] = 'SERVICE'
                        services.append(service_info)
            
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"Error ejecutando sc query: {e}")
        except UnicodeDecodeError:
            # Intentar con codificación diferente
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='cp1252')
                # Repetir el parseo con la nueva codificación
                # (código similar al anterior)
            except Exception as e2:
                self.menu.show_error(f"Error de codificación obteniendo servicios: {e2}")
        except Exception as e:
            self.menu.show_error(f"Error obteniendo servicios: {e}")
        
        return services
    
    def _list_all_services(self):
        """Lista todos los servicios del sistema."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Obteniendo lista de servicios...", total=None)
            services = self._get_services_list(running_only=False)
        
        if not services:
            self.menu.show_warning("⚠️ No se pudieron obtener los servicios")
            return
        
        # Ordenar por nombre
        services.sort(key=lambda x: x['display_name'].lower())
        
        # Crear tabla de servicios
        services_table = Table(title="🔧 Servicios del Sistema", box=box.DOUBLE)
        services_table.add_column("Nombre del Servicio", style="cyan", width=25)
        services_table.add_column("Nombre Técnico", style="blue", width=20)
        services_table.add_column("Estado", style="white", width=12)
        services_table.add_column("Tipo", style="magenta", width=15)
        
        # Contadores por estado
        running_count = 0
        stopped_count = 0
        other_count = 0
        
        for service in services:
            state = service.get('state', 'UNKNOWN')
            display_name = service.get('display_name', 'N/A')
            name = service.get('name', 'N/A')
            service_type = service.get('type', 'N/A')
            
            # Colorear según estado
            if state == 'RUNNING':
                state_style = 'green'
                running_count += 1
            elif state == 'STOPPED':
                state_style = 'red'
                stopped_count += 1
            else:
                state_style = 'yellow'
                other_count += 1
            
            services_table.add_row(
                display_name[:24],
                name[:19],
                f"[{state_style}]{state}[/{state_style}]",
                service_type[:14]
            )
        
        self.menu.console.print(services_table)
        
        # Mostrar resumen
        self.menu.console.print(f"\n[cyan]📊 Resumen de Servicios:[/cyan]")
        self.menu.console.print(f"  ✅ En ejecución: [green]{running_count}[/green]")
        self.menu.console.print(f"  ⏹️ Detenidos: [red]{stopped_count}[/red]")
        self.menu.console.print(f"  ❓ Otros estados: [yellow]{other_count}[/yellow]")
        self.menu.console.print(f"  📋 Total: {len(services)}")
    
    def _list_running_services(self):
        """Lista solo los servicios en ejecución."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Obteniendo servicios en ejecución...", total=None)
            services = self._get_services_list(running_only=True)
        
        if not services:
            self.menu.show_warning("⚠️ No se encontraron servicios en ejecución")
            return
        
        # Ordenar por nombre
        services.sort(key=lambda x: x['display_name'].lower())
        
        # Crear tabla de servicios activos
        services_table = Table(title="✅ Servicios en Ejecución", box=box.DOUBLE)
        services_table.add_column("Nombre del Servicio", style="cyan", width=30)
        services_table.add_column("Nombre Técnico", style="blue", width=25)
        services_table.add_column("Tipo", style="magenta", width=15)
        
        for service in services:
            display_name = service.get('display_name', 'N/A')
            name = service.get('name', 'N/A')
            service_type = service.get('type', 'N/A')
            
            services_table.add_row(
                display_name[:29],
                name[:24],
                service_type[:14]
            )
        
        self.menu.console.print(services_table)
        self.menu.console.print(f"\n[green]✅ Total de servicios en ejecución: {len(services)}[/green]")
    
    def _search_services(self):
        """Busca servicios por nombre."""
        search_term = self.menu.get_input("🔍 Ingresa el nombre del servicio a buscar")
        if not search_term:
            return
        
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Buscando servicios...", total=None)
            all_services = self._get_services_list(running_only=False)
        
        # Filtrar servicios que coincidan
        matching_services = []
        search_lower = search_term.lower()
        
        for service in all_services:
            display_name = service.get('display_name', '').lower()
            name = service.get('name', '').lower()
            
            if search_lower in display_name or search_lower in name:
                matching_services.append(service)
        
        if not matching_services:
            self.menu.show_warning(f"⚠️ No se encontraron servicios con '{search_term}'")
            return
        
        # Mostrar resultados
        services_table = Table(title=f"🔍 Servicios que contienen '{search_term}'", box=box.DOUBLE)
        services_table.add_column("Nombre del Servicio", style="cyan", width=30)
        services_table.add_column("Nombre Técnico", style="blue", width=20)
        services_table.add_column("Estado", style="white", width=12)
        
        for service in matching_services:
            state = service.get('state', 'UNKNOWN')
            display_name = service.get('display_name', 'N/A')
            name = service.get('name', 'N/A')
            
            # Colorear según estado
            if state == 'RUNNING':
                state_style = 'green'
            elif state == 'STOPPED':
                state_style = 'red'
            else:
                state_style = 'yellow'
            
            services_table.add_row(
                display_name[:29],
                name[:19],
                f"[{state_style}]{state}[/{state_style}]"
            )
        
        self.menu.console.print(services_table)
        self.menu.console.print(f"\n[cyan]📊 Servicios encontrados: {len(matching_services)}[/cyan]")
    
    def _start_service(self):
        """Inicia un servicio específico."""
        service_name = self.menu.get_input("▶️ Ingresa el nombre técnico del servicio a iniciar")
        if not service_name:
            return
        
        # Verificar que el servicio existe
        if not self._service_exists(service_name):
            self.menu.show_error(f"❌ El servicio '{service_name}' no existe")
            return
        
        # Verificar estado actual
        current_state = self._get_service_state(service_name)
        if current_state == 'RUNNING':
            self.menu.show_warning(f"⚠️ El servicio '{service_name}' ya está en ejecución")
            return
        
        # Confirmar acción
        confirm = self.menu.get_confirmation(
            f"⚠️ ¿Estás seguro de iniciar el servicio '{service_name}'?"
        )
        
        if not confirm:
            self.menu.show_info("ℹ️ Operación cancelada")
            return
        
        try:
            # Intentar iniciar el servicio
            result = subprocess.run(
                ['sc', 'start', service_name],
                capture_output=True, text=True, check=True, encoding='utf-8'
            )
            
            if 'START_PENDING' in result.stdout or 'RUNNING' in result.stdout:
                self.menu.show_success(f"✅ Servicio '{service_name}' iniciado correctamente")
            else:
                self.menu.show_warning(f"⚠️ Respuesta inesperada: {result.stdout}")
                
        except subprocess.CalledProcessError as e:
            if 'ACCESS_DENIED' in str(e) or 'access is denied' in str(e).lower():
                self.menu.show_error("❌ Acceso denegado. Ejecuta como administrador para gestionar servicios")
            elif 'already running' in str(e).lower():
                self.menu.show_warning(f"⚠️ El servicio '{service_name}' ya está en ejecución")
            else:
                self.menu.show_error(f"❌ Error iniciando servicio: {e}")
        except Exception as e:
            self.menu.show_error(f"❌ Error inesperado: {e}")
    
    def _stop_service(self):
        """Detiene un servicio específico."""
        service_name = self.menu.get_input("⏹️ Ingresa el nombre técnico del servicio a detener")
        if not service_name:
            return
        
        # Verificar que el servicio existe
        if not self._service_exists(service_name):
            self.menu.show_error(f"❌ El servicio '{service_name}' no existe")
            return
        
        # Verificar estado actual
        current_state = self._get_service_state(service_name)
        if current_state == 'STOPPED':
            self.menu.show_warning(f"⚠️ El servicio '{service_name}' ya está detenido")
            return
        
        # Confirmar acción
        confirm = self.menu.get_confirmation(
            f"⚠️ ¿Estás seguro de detener el servicio '{service_name}'?"
        )
        
        if not confirm:
            self.menu.show_info("ℹ️ Operación cancelada")
            return
        
        try:
            # Intentar detener el servicio
            result = subprocess.run(
                ['sc', 'stop', service_name],
                capture_output=True, text=True, check=True, encoding='utf-8'
            )
            
            if 'STOP_PENDING' in result.stdout or 'STOPPED' in result.stdout:
                self.menu.show_success(f"✅ Servicio '{service_name}' detenido correctamente")
            else:
                self.menu.show_warning(f"⚠️ Respuesta inesperada: {result.stdout}")
                
        except subprocess.CalledProcessError as e:
            if 'ACCESS_DENIED' in str(e) or 'access is denied' in str(e).lower():
                self.menu.show_error("❌ Acceso denegado. Ejecuta como administrador para gestionar servicios")
            elif 'not started' in str(e).lower():
                self.menu.show_warning(f"⚠️ El servicio '{service_name}' no está en ejecución")
            else:
                self.menu.show_error(f"❌ Error deteniendo servicio: {e}")
        except Exception as e:
            self.menu.show_error(f"❌ Error inesperado: {e}")
    
    def _restart_service(self):
        """Reinicia un servicio específico."""
        service_name = self.menu.get_input("🔄 Ingresa el nombre técnico del servicio a reiniciar")
        if not service_name:
            return
        
        # Verificar que el servicio existe
        if not self._service_exists(service_name):
            self.menu.show_error(f"❌ El servicio '{service_name}' no existe")
            return
        
        # Confirmar acción
        confirm = self.menu.get_confirmation(
            f"⚠️ ¿Estás seguro de reiniciar el servicio '{service_name}'?"
        )
        
        if not confirm:
            self.menu.show_info("ℹ️ Operación cancelada")
            return
        
        try:
            current_state = self._get_service_state(service_name)
            
            # Si está corriendo, detenerlo primero
            if current_state == 'RUNNING':
                self.menu.console.print("🔄 Deteniendo servicio...")
                subprocess.run(
                    ['sc', 'stop', service_name],
                    capture_output=True, text=True, check=True, encoding='utf-8'
                )
                
                # Esperar un momento
                import time
                time.sleep(2)
            
            # Iniciar el servicio
            self.menu.console.print("🔄 Iniciando servicio...")
            result = subprocess.run(
                ['sc', 'start', service_name],
                capture_output=True, text=True, check=True, encoding='utf-8'
            )
            
            if 'START_PENDING' in result.stdout or 'RUNNING' in result.stdout:
                self.menu.show_success(f"✅ Servicio '{service_name}' reiniciado correctamente")
            else:
                self.menu.show_warning(f"⚠️ Respuesta inesperada: {result.stdout}")
                
        except subprocess.CalledProcessError as e:
            if 'ACCESS_DENIED' in str(e) or 'access is denied' in str(e).lower():
                self.menu.show_error("❌ Acceso denegado. Ejecuta como administrador para gestionar servicios")
            else:
                self.menu.show_error(f"❌ Error reiniciando servicio: {e}")
        except Exception as e:
            self.menu.show_error(f"❌ Error inesperado: {e}")
    
    def _service_exists(self, service_name: str) -> bool:
        """Verifica si un servicio existe."""
        try:
            result = subprocess.run(
                ['sc', 'query', service_name],
                capture_output=True, text=True, check=True, encoding='utf-8'
            )
            return 'SERVICE_NAME:' in result.stdout
        except subprocess.CalledProcessError:
            return False
        except Exception:
            return False
    
    def _get_service_state(self, service_name: str) -> str:
        """Obtiene el estado actual de un servicio."""
        try:
            result = subprocess.run(
                ['sc', 'query', service_name],
                capture_output=True, text=True, check=True, encoding='utf-8'
            )
            
            lines = result.stdout.split('\n')
            for line in lines:
                if 'STATE' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        return parts[3]
            
            return 'UNKNOWN'
        except Exception:
            return 'UNKNOWN'

    def _command_exists(self, command: str) -> bool:
        """Verifica si un comando existe en el sistema."""
        try:
            subprocess.run([command, '--version'], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _show_env_vars(self):
        """Muestra y gestiona variables de entorno del sistema."""
        while True:
            self.menu.clear_screen()
            
            # Submenú de variables de entorno
            choices = [
                {
                    'name': '📋 Ver todas las variables',
                    'value': 'list_all',
                    'description': 'Mostrar todas las variables de entorno'
                },
                {
                    'name': '🔍 Buscar variable',
                    'value': 'search',
                    'description': 'Buscar variable por nombre'
                },
                {
                    'name': '🎯 Variables del sistema',
                    'value': 'system_vars',
                    'description': 'Mostrar solo variables del sistema'
                },
                {
                    'name': '👤 Variables del usuario',
                    'value': 'user_vars',
                    'description': 'Mostrar solo variables del usuario'
                },
                {
                    'name': '💾 Exportar a archivo',
                    'value': 'export',
                    'description': 'Exportar variables a archivo de texto'
                }
            ]
            
            selection = self.menu.show_menu(choices, "📋 ¿Qué quieres hacer con las variables de entorno?")
            
            if not selection or selection == 'exit':
                break
            
            try:
                if selection == 'list_all':
                    self._list_all_env_vars()
                elif selection == 'search':
                    self._search_env_vars()
                elif selection == 'system_vars':
                    self._list_system_env_vars()
                elif selection == 'user_vars':
                    self._list_user_env_vars()
                elif selection == 'export':
                    self._export_env_vars()
            except Exception as e:
                self.menu.show_error(f"Error en variables de entorno: {e}")
            
            self.menu.pause()

    def _list_all_env_vars(self):
        """Lista todas las variables de entorno."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Obteniendo variables de entorno...", total=None)
            env_vars = dict(os.environ)
        
        # Ordenar variables alfabéticamente
        sorted_vars = sorted(env_vars.items())
        
        # Crear tabla de variables
        env_table = Table(title="📋 Variables de Entorno", box=box.DOUBLE)
        env_table.add_column("Variable", style="cyan", no_wrap=True, width=30)
        env_table.add_column("Valor", style="white", width=60)
        
        for name, value in sorted_vars:
            # Truncar valores muy largos
            display_value = value[:57] + "..." if len(value) > 60 else value
            
            # Colorear variables importantes
            name_style = "yellow" if name in ['PATH', 'PYTHONPATH', 'HOME', 'USER', 'USERNAME'] else "cyan"
            
            env_table.add_row(
                f"[{name_style}]{name}[/{name_style}]",
                display_value
            )
        
        self.menu.console.print(env_table)
        self.menu.console.print(f"\n[cyan]📊 Total de variables: {len(env_vars)}[/cyan]")

    def _search_env_vars(self):
        """Busca variables de entorno por nombre."""
        search_term = self.menu.get_input("🔍 Ingresa el nombre de la variable a buscar")
        if not search_term:
            return
        
        self.menu.clear_screen()
        
        env_vars = dict(os.environ)
        
        # Filtrar variables que coincidan
        matching_vars = {
            name: value for name, value in env_vars.items()
            if search_term.lower() in name.lower()
        }
        
        if not matching_vars:
            self.menu.show_warning(f"⚠️ No se encontraron variables que contengan '{search_term}'")
            return
        
        # Mostrar resultados
        env_table = Table(title=f"🔍 Variables que contienen '{search_term}'", box=box.DOUBLE)
        env_table.add_column("Variable", style="cyan", no_wrap=True)
        env_table.add_column("Valor", style="white")
        
        for name, value in sorted(matching_vars.items()):
            # Resaltar el término de búsqueda
            highlighted_name = name.replace(
                search_term, f"[yellow]{search_term}[/yellow]"
            )
            
            env_table.add_row(highlighted_name, value[:80] + "..." if len(value) > 80 else value)
        
        self.menu.console.print(env_table)
        self.menu.console.print(f"\n[cyan]📊 Variables encontradas: {len(matching_vars)}[/cyan]")

    def _list_system_env_vars(self):
        """Lista variables de entorno del sistema."""
        self.menu.clear_screen()
        
        # Variables típicas del sistema
        system_vars = [
            'PATH', 'PATHEXT', 'SYSTEMROOT', 'WINDIR', 'PROGRAMFILES', 
            'PROGRAMFILES(X86)', 'PROGRAMDATA', 'COMSPEC', 'PROCESSOR_ARCHITECTURE',
            'PROCESSOR_IDENTIFIER', 'NUMBER_OF_PROCESSORS', 'OS', 'COMPUTERNAME'
        ]
        
        env_vars = dict(os.environ)
        found_system_vars = {}
        
        for var in system_vars:
            if var in env_vars:
                found_system_vars[var] = env_vars[var]
        
        if not found_system_vars:
            self.menu.show_warning("⚠️ No se encontraron variables del sistema")
            return
        
        # Crear tabla de variables del sistema
        sys_table = Table(title="🖥️ Variables del Sistema", box=box.DOUBLE)
        sys_table.add_column("Variable", style="yellow", no_wrap=True, width=25)
        sys_table.add_column("Valor", style="white", width=70)
        
        for name, value in sorted(found_system_vars.items()):
            # Formatear PATH de manera especial
            if name == 'PATH':
                paths = value.split(os.pathsep)
                display_value = f"{len(paths)} rutas (ver detalles abajo)"
            else:
                display_value = value[:67] + "..." if len(value) > 70 else value
            
            sys_table.add_row(name, display_value)
        
        self.menu.console.print(sys_table)
        
        # Mostrar PATH detallado si existe
        if 'PATH' in found_system_vars:
            self.menu.console.print("\n[bold yellow]📁 Rutas en PATH:[/bold yellow]")
            paths = found_system_vars['PATH'].split(os.pathsep)
            for i, path in enumerate(paths[:20], 1):  # Mostrar solo las primeras 20
                exists_marker = "✅" if os.path.exists(path) else "❌"
                self.menu.console.print(f"  {i:2d}. {exists_marker} {path}")
            
            if len(paths) > 20:
                self.menu.console.print(f"  ... y {len(paths) - 20} rutas más")
        
        self.menu.console.print(f"\n[cyan]📊 Variables del sistema encontradas: {len(found_system_vars)}[/cyan]")

    def _list_user_env_vars(self):
        """Lista variables de entorno del usuario."""
        self.menu.clear_screen()
        
        # Variables típicas del usuario
        user_vars = [
            'USERNAME', 'USERPROFILE', 'HOMEPATH', 'HOMEDRIVE', 'APPDATA',
            'LOCALAPPDATA', 'TEMP', 'TMP', 'USERDOMAIN', 'LOGONSERVER'
        ]
        
        env_vars = dict(os.environ)
        found_user_vars = {}
        
        for var in user_vars:
            if var in env_vars:
                found_user_vars[var] = env_vars[var]
        
        # También incluir variables que empiecen con USER
        for name, value in env_vars.items():
            if name.startswith('USER') and name not in found_user_vars:
                found_user_vars[name] = value
        
        if not found_user_vars:
            self.menu.show_warning("⚠️ No se encontraron variables del usuario")
            return
        
        # Crear tabla de variables del usuario
        user_table = Table(title="👤 Variables del Usuario", box=box.DOUBLE)
        user_table.add_column("Variable", style="green", no_wrap=True, width=25)
        user_table.add_column("Valor", style="white", width=70)
        
        for name, value in sorted(found_user_vars.items()):
            display_value = value[:67] + "..." if len(value) > 70 else value
            user_table.add_row(name, display_value)
        
        self.menu.console.print(user_table)
        self.menu.console.print(f"\n[cyan]📊 Variables del usuario encontradas: {len(found_user_vars)}[/cyan]")

    def _export_env_vars(self):
        """Exporta variables de entorno a un archivo."""
        filename = self.menu.get_input("💾 Nombre del archivo (sin extensión)", "variables_entorno")
        if not filename:
            return
        
        # Asegurar extensión .txt
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        try:
            env_vars = dict(os.environ)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# Variables de Entorno del Sistema\n")
                f.write(f"# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Sistema: {platform.system()} {platform.release()}\n")
                f.write(f"# Total de variables: {len(env_vars)}\n\n")
                
                # Escribir variables ordenadas
                for name, value in sorted(env_vars.items()):
                    f.write(f"{name}={value}\n")
            
            file_size = os.path.getsize(filename)
            self.menu.show_success(f"✅ Variables exportadas a '{filename}' ({self._format_bytes(file_size)})")
            
            # Preguntar si abrir el archivo
            if self.menu.get_confirmation("¿Abrir el archivo generado?"):
                try:
                    if os.name == 'nt':
                        os.startfile(filename)
                    else:
                        subprocess.run(['xdg-open', filename])
                except Exception as e:
                    self.menu.show_warning(f"⚠️ No se pudo abrir el archivo: {e}")
            
        except Exception as e:
            self.menu.show_error(f"❌ Error exportando variables: {e}")

    def _cleanup_temp_files(self):
        """Limpia archivos temporales del sistema."""
        while True:
            self.menu.clear_screen()
            
            # Submenú de limpieza
            choices = [
                {
                    'name': '📊 Ver tamaño de temporales',
                    'value': 'show_size',
                    'description': 'Mostrar tamaño actual de archivos temporales'
                },
                {
                    'name': '🧹 Limpiar temporales del usuario',
                    'value': 'clean_user',
                    'description': 'Limpiar archivos temporales del usuario actual'
                },
                {
                    'name': '🗑️ Limpiar temporales del sistema',
                    'value': 'clean_system',
                    'description': 'Limpiar archivos temporales del sistema (requiere permisos)'
                },
                {
                    'name': '🔍 Análisis detallado',
                    'value': 'detailed',
                    'description': 'Análisis detallado de archivos temporales'
                },
                {
                    'name': '⚡ Limpieza completa',
                    'value': 'full_cleanup',
                    'description': 'Limpiar todos los archivos temporales posibles'
                }
            ]
            
            selection = self.menu.show_menu(choices, "🧹 ¿Qué tipo de limpieza quieres realizar?")
            
            if not selection or selection == 'exit':
                break
            
            try:
                if selection == 'show_size':
                    self._show_temp_size()
                elif selection == 'clean_user':
                    self._clean_user_temp()
                elif selection == 'clean_system':
                    self._clean_system_temp()
                elif selection == 'detailed':
                    self._detailed_temp_analysis()
                elif selection == 'full_cleanup':
                    self._full_temp_cleanup()
            except Exception as e:
                self.menu.show_error(f"Error en limpieza de temporales: {e}")
            
            self.menu.pause()

    def _get_temp_directories(self) -> List[str]:
        """Obtiene lista de directorios temporales del sistema."""
        temp_dirs = []
        
        # Directorio temporal del usuario
        user_temp = tempfile.gettempdir()
        if user_temp and os.path.exists(user_temp):
            temp_dirs.append(user_temp)
        
        # Directorios temporales adicionales en Windows
        if os.name == 'nt':
            additional_temps = [
                os.environ.get('TEMP'),
                os.environ.get('TMP'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
                r'C:\Windows\Temp',
                r'C:\Temp',
                os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp')
            ]
            
            for temp_dir in additional_temps:
                if temp_dir and os.path.exists(temp_dir) and temp_dir not in temp_dirs:
                    temp_dirs.append(temp_dir)
        
        return temp_dirs

    def _calculate_temp_size(self, directory: str) -> tuple:
        """Calcula el tamaño total de archivos temporales en un directorio."""
        total_size = 0
        file_count = 0
        error_count = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            total_size += os.path.getsize(file_path)
                            file_count += 1
                    except (OSError, PermissionError):
                        error_count += 1
                        continue
        except (OSError, PermissionError):
            pass
        
        return total_size, file_count, error_count

    def _show_temp_size(self):
        """Muestra el tamaño actual de archivos temporales."""
        self.menu.clear_screen()
        
        temp_dirs = self._get_temp_directories()
        
        if not temp_dirs:
            self.menu.show_warning("⚠️ No se encontraron directorios temporales")
            return
        
        # Crear tabla de directorios temporales
        temp_table = Table(title="📊 Tamaño de Archivos Temporales", box=box.DOUBLE)
        temp_table.add_column("Directorio", style="cyan", width=50)
        temp_table.add_column("Tamaño", style="yellow", justify="right", width=12)
        temp_table.add_column("Archivos", style="green", justify="right", width=10)
        temp_table.add_column("Errores", style="red", justify="right", width=8)
        
        total_size = 0
        total_files = 0
        total_errors = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Analizando directorios temporales...", total=len(temp_dirs))
            
            for temp_dir in temp_dirs:
                progress.update(task, description=f"Analizando {os.path.basename(temp_dir)}...")
                
                size, files, errors = self._calculate_temp_size(temp_dir)
                total_size += size
                total_files += files
                total_errors += errors
                
                # Colorear según tamaño
                size_style = "red" if size > 1024*1024*100 else "yellow" if size > 1024*1024*10 else "white"
                
                temp_table.add_row(
                    temp_dir,
                    f"[{size_style}]{self._format_bytes(size)}[/{size_style}]",
                    str(files),
                    str(errors) if errors > 0 else "-"
                )
                
                progress.advance(task)
        
        self.menu.console.print(temp_table)
        
        # Resumen total
        self.menu.console.print(f"\n[bold cyan]📊 Resumen Total:[/bold cyan]")
        self.menu.console.print(f"  💾 Tamaño total: [yellow]{self._format_bytes(total_size)}[/yellow]")
        self.menu.console.print(f"  📄 Total de archivos: [green]{total_files:,}[/green]")
        if total_errors > 0:
            self.menu.console.print(f"  ❌ Archivos con errores: [red]{total_errors}[/red]")
        
        if total_size > 1024*1024*50:  # Más de 50MB
            self.menu.console.print(f"\n[yellow]💡 Considera limpiar archivos temporales para liberar {self._format_bytes(total_size)}[/yellow]")

    def _clean_user_temp(self):
        """Limpia archivos temporales del usuario."""
        user_temp = tempfile.gettempdir()
        
        if not user_temp or not os.path.exists(user_temp):
            self.menu.show_error("❌ No se encontró directorio temporal del usuario")
            return
        
        # Mostrar tamaño antes de limpiar
        size_before, files_before, _ = self._calculate_temp_size(user_temp)
        
        self.menu.console.print(f"📊 Directorio: [cyan]{user_temp}[/cyan]")
        self.menu.console.print(f"📊 Tamaño actual: [yellow]{self._format_bytes(size_before)}[/yellow]")
        self.menu.console.print(f"📊 Archivos: [green]{files_before:,}[/green]")
        
        if not self.menu.get_confirmation("¿Proceder con la limpieza de archivos temporales del usuario?"):
            self.menu.show_info("ℹ️ Limpieza cancelada")
            return
        
        # Realizar limpieza
        deleted_files = 0
        deleted_size = 0
        errors = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Limpiando archivos temporales...", total=None)
            
            try:
                for root, dirs, files in os.walk(user_temp):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            if os.path.isfile(file_path):
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                deleted_files += 1
                                deleted_size += file_size
                        except (OSError, PermissionError) as e:
                            errors.append(f"{file}: {str(e)}")
                            continue
                    
                    # Intentar eliminar directorios vacíos
                    for dir_name in dirs:
                        try:
                            dir_path = os.path.join(root, dir_name)
                            if os.path.isdir(dir_path) and not os.listdir(dir_path):
                                os.rmdir(dir_path)
                        except (OSError, PermissionError):
                            continue
            except Exception as e:
                self.menu.show_error(f"❌ Error durante la limpieza: {e}")
                return
        
        # Mostrar resultados
        self.menu.console.print(f"\n[bold green]✅ Limpieza Completada:[/bold green]")
        self.menu.console.print(f"  🗑️ Archivos eliminados: [green]{deleted_files:,}[/green]")
        self.menu.console.print(f"  💾 Espacio liberado: [yellow]{self._format_bytes(deleted_size)}[/yellow]")
        
        if errors:
            self.menu.console.print(f"  ❌ Archivos no eliminados: [red]{len(errors)}[/red]")
            if len(errors) <= 10:
                for error in errors:
                    self.menu.console.print(f"    • {error}")
            else:
                for error in errors[:5]:
                    self.menu.console.print(f"    • {error}")
                self.menu.console.print(f"    ... y {len(errors) - 5} errores más")

    def _clean_system_temp(self):
        """Limpia archivos temporales del sistema (requiere permisos administrativos)."""
        if os.name != 'nt':
            self.menu.show_warning("⚠️ Esta función está diseñada para Windows")
            return
        
        system_temp = r'C:\Windows\Temp'
        
        if not os.path.exists(system_temp):
            self.menu.show_error("❌ No se encontró directorio temporal del sistema")
            return
        
        # Advertencia sobre permisos
        self.menu.show_warning("⚠️ Esta operación requiere permisos administrativos")
        self.menu.show_warning("⚠️ Algunos archivos pueden estar en uso y no se podrán eliminar")
        
        # Mostrar tamaño antes de limpiar
        size_before, files_before, _ = self._calculate_temp_size(system_temp)
        
        self.menu.console.print(f"📊 Directorio: [cyan]{system_temp}[/cyan]")
        self.menu.console.print(f"📊 Tamaño actual: [yellow]{self._format_bytes(size_before)}[/yellow]")
        self.menu.console.print(f"📊 Archivos: [green]{files_before:,}[/green]")
        
        if not self.menu.get_confirmation("¿Proceder con la limpieza de archivos temporales del sistema?"):
            self.menu.show_info("ℹ️ Limpieza cancelada")
            return
        
        # Realizar limpieza
        deleted_files = 0
        deleted_size = 0
        errors = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Limpiando archivos del sistema...", total=None)
            
            try:
                for root, dirs, files in os.walk(system_temp):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            if os.path.isfile(file_path):
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                deleted_files += 1
                                deleted_size += file_size
                        except (OSError, PermissionError) as e:
                            errors.append(f"{file}: {str(e)}")
                            continue
            except Exception as e:
                self.menu.show_error(f"❌ Error durante la limpieza: {e}")
                return
        
        # Mostrar resultados
        self.menu.console.print(f"\n[bold green]✅ Limpieza del Sistema Completada:[/bold green]")
        self.menu.console.print(f"  🗑️ Archivos eliminados: [green]{deleted_files:,}[/green]")
        self.menu.console.print(f"  💾 Espacio liberado: [yellow]{self._format_bytes(deleted_size)}[/yellow]")
        
        if errors:
            self.menu.console.print(f"  ❌ Archivos no eliminados: [red]{len(errors)}[/red]")
            self.menu.console.print("  💡 Algunos archivos pueden estar en uso por el sistema")

    def _detailed_temp_analysis(self):
        """Realiza un análisis detallado de archivos temporales."""
        self.menu.clear_screen()
        
        temp_dirs = self._get_temp_directories()
        
        if not temp_dirs:
            self.menu.show_warning("⚠️ No se encontraron directorios temporales")
            return
        
        self.menu.console.print("[bold cyan]🔍 Análisis Detallado de Archivos Temporales[/bold cyan]\n")
        
        for temp_dir in temp_dirs:
            self.menu.console.print(f"[bold yellow]📁 Analizando: {temp_dir}[/bold yellow]")
            
            try:
                # Análisis por extensión
                extensions = {}
                total_size = 0
                total_files = 0
                
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            if os.path.isfile(file_path):
                                size = os.path.getsize(file_path)
                                ext = os.path.splitext(file)[1].lower() or 'sin_extension'
                                
                                if ext not in extensions:
                                    extensions[ext] = {'count': 0, 'size': 0}
                                
                                extensions[ext]['count'] += 1
                                extensions[ext]['size'] += size
                                total_size += size
                                total_files += 1
                        except (OSError, PermissionError):
                            continue
                
                if extensions:
                    # Mostrar top 10 extensiones por tamaño
                    sorted_ext = sorted(extensions.items(), key=lambda x: x[1]['size'], reverse=True)
                    
                    ext_table = Table(box=box.SIMPLE)
                    ext_table.add_column("Extensión", style="cyan", width=15)
                    ext_table.add_column("Archivos", style="green", justify="right", width=10)
                    ext_table.add_column("Tamaño", style="yellow", justify="right", width=12)
                    ext_table.add_column("%", style="magenta", justify="right", width=8)
                    
                    for ext, data in sorted_ext[:10]:
                        percentage = (data['size'] / total_size * 100) if total_size > 0 else 0
                        ext_table.add_row(
                            ext,
                            f"{data['count']:,}",
                            self._format_bytes(data['size']),
                            f"{percentage:.1f}%"
                        )
                    
                    self.menu.console.print(ext_table)
                    self.menu.console.print(f"  📊 Total: {total_files:,} archivos, {self._format_bytes(total_size)}\n")
                else:
                    self.menu.console.print("  📭 Directorio vacío o sin acceso\n")
                    
            except Exception as e:
                self.menu.console.print(f"  ❌ Error analizando directorio: {e}\n")

    def _full_temp_cleanup(self):
        """Realiza una limpieza completa de todos los archivos temporales posibles."""
        self.menu.clear_screen()
        
        self.menu.show_warning("⚠️ Esta operación limpiará TODOS los archivos temporales posibles")
        self.menu.show_warning("⚠️ Algunos archivos pueden estar en uso y no se podrán eliminar")
        self.menu.show_warning("⚠️ Se recomienda cerrar otras aplicaciones antes de continuar")
        
        if not self.menu.get_confirmation("¿Estás seguro de realizar una limpieza completa?"):
            self.menu.show_info("ℹ️ Limpieza cancelada")
            return
        
        temp_dirs = self._get_temp_directories()
        
        if not temp_dirs:
            self.menu.show_error("❌ No se encontraron directorios temporales")
            return
        
        total_deleted_files = 0
        total_deleted_size = 0
        total_errors = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            main_task = progress.add_task("Limpieza completa en progreso...", total=len(temp_dirs))
            
            for temp_dir in temp_dirs:
                progress.update(main_task, description=f"Limpiando {os.path.basename(temp_dir)}...")
                
                deleted_files = 0
                deleted_size = 0
                errors = 0
                
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                if os.path.isfile(file_path):
                                    file_size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    deleted_files += 1
                                    deleted_size += file_size
                            except (OSError, PermissionError):
                                errors += 1
                                continue
                        
                        # Intentar eliminar directorios vacíos
                        for dir_name in dirs:
                            try:
                                dir_path = os.path.join(root, dir_name)
                                if os.path.isdir(dir_path) and not os.listdir(dir_path):
                                    os.rmdir(dir_path)
                            except (OSError, PermissionError):
                                continue
                
                except Exception:
                    errors += 1
                
                total_deleted_files += deleted_files
                total_deleted_size += deleted_size
                total_errors += errors
                
                progress.advance(main_task)
        
        # Mostrar resultados finales
        self.menu.console.print(f"\n[bold green]✅ Limpieza Completa Finalizada:[/bold green]")
        self.menu.console.print(f"  📁 Directorios procesados: [cyan]{len(temp_dirs)}[/cyan]")
        self.menu.console.print(f"  🗑️ Total de archivos eliminados: [green]{total_deleted_files:,}[/green]")
        self.menu.console.print(f"  💾 Total de espacio liberado: [yellow]{self._format_bytes(total_deleted_size)}[/yellow]")
        
        if total_errors > 0:
            self.menu.console.print(f"  ❌ Archivos no eliminados: [red]{total_errors:,}[/red]")
            self.menu.console.print("  💡 Algunos archivos pueden estar en uso por aplicaciones activas")
        
        if total_deleted_size > 1024*1024*100:  # Más de 100MB liberados
            self.menu.console.print(f"\n[bold green]🎉 ¡Excelente! Se liberaron {self._format_bytes(total_deleted_size)} de espacio en disco[/bold green]")

    def _open_system_tools(self):
        """Abre herramientas del sistema como Task Manager y Registry Editor."""
        while True:
            self.menu.clear_screen()
            
            # Submenú de herramientas del sistema
            choices = [
                {
                    'name': '⚙️ Administrador de tareas',
                    'value': 'taskmgr',
                    'description': 'Abrir el Administrador de tareas de Windows'
                },
                {
                    'name': '📝 Editor del registro',
                    'value': 'regedit',
                    'description': 'Abrir el Editor del registro (¡Usar con precaución!)'
                },
                {
                    'name': '🖥️ Información del sistema',
                    'value': 'msinfo32',
                    'description': 'Abrir la herramienta de información del sistema'
                },
                {
                    'name': '🔧 Configuración del sistema',
                    'value': 'msconfig',
                    'description': 'Abrir la configuración del sistema'
                },
                {
                    'name': '💾 Administrador de discos',
                    'value': 'diskmgmt',
                    'description': 'Abrir el Administrador de discos'
                },
                {
                    'name': '🌐 Configuración de red',
                    'value': 'ncpa',
                    'description': 'Abrir conexiones de red'
                }
            ]
            
            selection = self.menu.show_menu(choices, "🛠️ ¿Qué herramienta del sistema quieres abrir?")
            
            if not selection or selection == 'exit':
                break
            
            try:
                if selection == 'taskmgr':
                    self._open_task_manager()
                elif selection == 'regedit':
                    self._open_registry_editor()
                elif selection == 'msinfo32':
                    self._open_system_info_tool()
                elif selection == 'msconfig':
                    self._open_system_config()
                elif selection == 'diskmgmt':
                    self._open_disk_management()
                elif selection == 'ncpa':
                    self._open_network_connections()
            except Exception as e:
                self.menu.show_error(f"Error abriendo herramienta: {e}")
            
            self.menu.pause()

    def _open_task_manager(self):
        """Abre el Administrador de tareas."""
        try:
            # Verificar que taskmgr.exe existe
            if not self._tool_exists('taskmgr.exe'):
                self.menu.show_error("❌ No se encontró el Administrador de tareas (taskmgr.exe)")
                return
            
            self.menu.show_info("🔄 Abriendo Administrador de tareas...")
            
            if os.name == 'nt':
                subprocess.Popen(['taskmgr.exe'])
                self.menu.show_success("✅ Administrador de tareas abierto correctamente")
            else:
                # En sistemas no Windows, intentar abrir monitor del sistema equivalente
                alternatives = ['gnome-system-monitor', 'ksysguard', 'htop']
                opened = False
                
                for alt in alternatives:
                    if self._tool_exists(alt):
                        subprocess.Popen([alt])
                        self.menu.show_success(f"✅ {alt} abierto correctamente")
                        opened = True
                        break
                
                if not opened:
                    self.menu.show_error("❌ No se encontró un monitor de sistema compatible")
                    
        except Exception as e:
            self.menu.show_error(f"❌ Error abriendo Administrador de tareas: {e}")

    def _open_registry_editor(self):
        """Abre el Editor del registro con advertencias de seguridad."""
        # Mostrar advertencias de seguridad
        self.menu.show_warning("⚠️ ADVERTENCIA DE SEGURIDAD ⚠️")
        self.menu.show_warning("El Editor del registro es una herramienta avanzada")
        self.menu.show_warning("Modificar el registro incorrectamente puede dañar el sistema")
        self.menu.show_warning("Solo continúa si sabes lo que estás haciendo")
        
        if not self.menu.get_confirmation("¿Estás seguro de que quieres abrir el Editor del registro?"):
            self.menu.show_info("ℹ️ Apertura del Editor del registro cancelada")
            return
        
        try:
            # Verificar que regedit.exe existe
            if not self._tool_exists('regedit.exe'):
                self.menu.show_error("❌ No se encontró el Editor del registro (regedit.exe)")
                return
            
            self.menu.show_info("🔄 Abriendo Editor del registro...")
            
            if os.name == 'nt':
                subprocess.Popen(['regedit.exe'])
                self.menu.show_success("✅ Editor del registro abierto correctamente")
                self.menu.show_warning("⚠️ Recuerda: Haz backup antes de hacer cambios importantes")
            else:
                self.menu.show_error("❌ El Editor del registro solo está disponible en Windows")
                
        except Exception as e:
            self.menu.show_error(f"❌ Error abriendo Editor del registro: {e}")

    def _open_system_info_tool(self):
        """Abre la herramienta de información del sistema."""
        try:
            if not self._tool_exists('msinfo32.exe'):
                self.menu.show_error("❌ No se encontró la herramienta de información del sistema (msinfo32.exe)")
                return
            
            self.menu.show_info("🔄 Abriendo información del sistema...")
            
            if os.name == 'nt':
                subprocess.Popen(['msinfo32.exe'])
                self.menu.show_success("✅ Información del sistema abierta correctamente")
            else:
                self.menu.show_error("❌ msinfo32 solo está disponible en Windows")
                
        except Exception as e:
            self.menu.show_error(f"❌ Error abriendo información del sistema: {e}")

    def _open_system_config(self):
        """Abre la configuración del sistema."""
        try:
            if not self._tool_exists('msconfig.exe'):
                self.menu.show_error("❌ No se encontró la configuración del sistema (msconfig.exe)")
                return
            
            self.menu.show_info("🔄 Abriendo configuración del sistema...")
            
            if os.name == 'nt':
                subprocess.Popen(['msconfig.exe'])
                self.menu.show_success("✅ Configuración del sistema abierta correctamente")
            else:
                self.menu.show_error("❌ msconfig solo está disponible en Windows")
                
        except Exception as e:
            self.menu.show_error(f"❌ Error abriendo configuración del sistema: {e}")

    def _open_disk_management(self):
        """Abre el Administrador de discos."""
        try:
            self.menu.show_info("🔄 Abriendo Administrador de discos...")
            
            if os.name == 'nt':
                # Usar diskmgmt.msc a través de mmc
                subprocess.Popen(['mmc.exe', 'diskmgmt.msc'])
                self.menu.show_success("✅ Administrador de discos abierto correctamente")
            else:
                # En sistemas no Windows, intentar abrir herramientas equivalentes
                alternatives = ['gnome-disks', 'gparted', 'kde-partitionmanager']
                opened = False
                
                for alt in alternatives:
                    if self._tool_exists(alt):
                        subprocess.Popen([alt])
                        self.menu.show_success(f"✅ {alt} abierto correctamente")
                        opened = True
                        break
                
                if not opened:
                    self.menu.show_error("❌ No se encontró un administrador de discos compatible")
                
        except Exception as e:
            self.menu.show_error(f"❌ Error abriendo Administrador de discos: {e}")

    def _open_network_connections(self):
        """Abre las conexiones de red."""
        try:
            self.menu.show_info("🔄 Abriendo conexiones de red...")
            
            if os.name == 'nt':
                # Usar ncpa.cpl a través del panel de control
                subprocess.Popen(['control.exe', 'ncpa.cpl'])
                self.menu.show_success("✅ Conexiones de red abiertas correctamente")
            else:
                # En sistemas no Windows, intentar abrir configuración de red
                alternatives = ['nm-connection-editor', 'network-manager-gnome', 'systemsettings5']
                opened = False
                
                for alt in alternatives:
                    if self._tool_exists(alt):
                        subprocess.Popen([alt])
                        self.menu.show_success(f"✅ {alt} abierto correctamente")
                        opened = True
                        break
                
                if not opened:
                    self.menu.show_error("❌ No se encontró un administrador de red compatible")
                
        except Exception as e:
            self.menu.show_error(f"❌ Error abriendo conexiones de red: {e}")

    def _tool_exists(self, tool_name: str) -> bool:
        """Verifica si una herramienta del sistema existe."""
        try:
            if os.name == 'nt':
                # En Windows, verificar en PATH y directorios del sistema
                result = subprocess.run(['where', tool_name], 
                                      capture_output=True, 
                                      text=True, 
                                      check=False)
                return result.returncode == 0
            else:
                # En sistemas Unix-like, usar which
                result = subprocess.run(['which', tool_name], 
                                      capture_output=True, 
                                      text=True, 
                                      check=False)
                return result.returncode == 0
        except Exception:
            return False

    def _network_diagnostics(self):
        """Herramientas de diagnóstico de red."""
        while True:
            self.menu.clear_screen()
            
            # Submenú de diagnóstico de red
            choices = [
                {
                    'name': '🌍 Información de IP/Red',
                    'value': 'ip_info',
                    'description': 'Ver IP local y pública, configuración de red'
                },
                {
                    'name': '📡 Ping a servidor',
                    'value': 'ping',
                    'description': 'Hacer ping interactivo a servidores'
                },
                {
                    'name': '🔄 Flush DNS',
                    'value': 'flush_dns',
                    'description': 'Limpiar cache DNS del sistema'
                },
                {
                    'name': '⚙️ Configuración completa',
                    'value': 'full_config',
                    'description': 'Ver configuración completa con ipconfig'
                },
                {
                    'name': '🔍 Test de conectividad',
                    'value': 'connectivity_test',
                    'description': 'Probar conectividad a servicios comunes'
                }
            ]
            
            selection = self.menu.show_menu(choices, "🌍 ¿Qué diagnóstico de red necesitas?")
            
            if not selection or selection == 'exit':
                break
            
            try:
                if selection == 'ip_info':
                    self._show_ip_info()
                elif selection == 'ping':
                    self._interactive_ping()
                elif selection == 'flush_dns':
                    self._flush_dns()
                elif selection == 'full_config':
                    self._show_full_network_config()
                elif selection == 'connectivity_test':
                    self._connectivity_test()
            except Exception as e:
                self.menu.show_error(f"Error en diagnóstico de red: {e}")
            
            self.menu.pause()
    
    def _show_ip_info(self):
        """Muestra información de IP local y pública."""
        self.menu.clear_screen()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Obteniendo información de red...", total=None)
            
            # Crear tabla de información de red
            ip_table = Table(title="🌍 Información de IP y Red", box=box.DOUBLE)
            ip_table.add_column("Tipo", style="cyan", no_wrap=True)
            ip_table.add_column("Valor", style="white")
            
            # IP local
            local_ip = self._get_local_ip()
            ip_table.add_row("🏠 IP Local", local_ip or "No disponible")
            
            # IP pública
            public_ip = self._get_public_ip()
            ip_table.add_row("🌐 IP Pública", public_ip or "No disponible")
            
            # Hostname
            hostname = platform.node()
            ip_table.add_row("🏷️ Hostname", hostname)
            
            # Gateway predeterminado
            gateway = self._get_default_gateway()
            ip_table.add_row("🚪 Gateway", gateway or "No disponible")
            
            # Servidores DNS
            dns_servers = self._get_dns_servers()
            if dns_servers:
                for i, dns in enumerate(dns_servers[:3], 1):
                    ip_table.add_row(f"🔍 DNS {i}", dns)
            else:
                ip_table.add_row("🔍 DNS", "No disponible")
        
        self.menu.console.print(ip_table)
        
        # Mostrar interfaces de red si psutil está disponible
        if psutil:
            self._show_network_interfaces()
    
    def _get_local_ip(self) -> Optional[str]:
        """Obtiene la IP local del sistema."""
        try:
            # Método 1: Conectar a un servidor externo para obtener IP local
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            try:
                # Método 2: Usar hostname
                import socket
                hostname = socket.gethostname()
                return socket.gethostbyname(hostname)
            except Exception:
                return None
    
    def _get_public_ip(self) -> Optional[str]:
        """Obtiene la IP pública del sistema."""
        services = [
            "https://api.ipify.org",
            "https://ipecho.net/plain",
            "https://icanhazip.com",
            "https://ident.me"
        ]
        
        for service in services:
            try:
                import urllib.request
                with urllib.request.urlopen(service, timeout=5) as response:
                    return response.read().decode('utf-8').strip()
            except Exception:
                continue
        
        return None
    
    def _get_default_gateway(self) -> Optional[str]:
        """Obtiene el gateway predeterminado."""
        try:
            if os.name == 'nt':
                # Windows: usar route print
                result = subprocess.run(['route', 'print', '0.0.0.0'], 
                                      capture_output=True, text=True, check=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if '0.0.0.0' in line and 'Gateway' not in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            return parts[2]
            else:
                # Linux/Unix: usar ip route
                result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                      capture_output=True, text=True, check=True)
                if 'via' in result.stdout:
                    return result.stdout.split('via')[1].split()[0]
        except Exception:
            pass
        
        # Fallback con psutil si está disponible
        if psutil:
            try:
                gateways = psutil.net_if_addrs()
                # Esto es una implementación simplificada
                return "Usar ipconfig para ver gateway"
            except Exception:
                pass
        
        return None
    
    def _get_dns_servers(self) -> List[str]:
        """Obtiene los servidores DNS configurados."""
        dns_servers = []
        
        try:
            if os.name == 'nt':
                # Windows: usar nslookup para obtener DNS
                result = subprocess.run(['nslookup'], 
                                      input='\n', 
                                      capture_output=True, 
                                      text=True, 
                                      check=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Server:' in line or 'Servidor:' in line:
                        # Buscar la siguiente línea con la IP
                        continue
                    if 'Address:' in line or 'Dirección:' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            dns_ip = parts[1].strip()
                            if dns_ip and dns_ip != '127.0.0.1':
                                dns_servers.append(dns_ip)
                                break
            else:
                # Linux/Unix: leer /etc/resolv.conf
                try:
                    with open('/etc/resolv.conf', 'r') as f:
                        for line in f:
                            if line.startswith('nameserver'):
                                dns_ip = line.split()[1]
                                dns_servers.append(dns_ip)
                except Exception:
                    pass
        except Exception:
            pass
        
        return dns_servers
    
    def _show_network_interfaces(self):
        """Muestra información de interfaces de red."""
        if not psutil:
            return
        
        try:
            self.menu.console.print("\n[bold cyan]🔌 Interfaces de Red:[/bold cyan]")
            
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            
            for interface_name, addresses in interfaces.items():
                if interface_name.startswith('lo'):  # Skip loopback
                    continue
                
                # Estado de la interfaz
                if interface_name in stats:
                    status = "🟢 Activa" if stats[interface_name].isup else "🔴 Inactiva"
                    speed = stats[interface_name].speed
                    speed_text = f" ({speed} Mbps)" if speed > 0 else ""
                else:
                    status = "❓ Desconocido"
                    speed_text = ""
                
                self.menu.console.print(f"\n  📡 {interface_name}: {status}{speed_text}")
                
                # Direcciones de la interfaz
                for addr in addresses:
                    if addr.family == socket.AF_INET:  # IPv4
                        self.menu.console.print(f"    IPv4: {addr.address}")
                        if addr.netmask:
                            self.menu.console.print(f"    Máscara: {addr.netmask}")
                    elif addr.family == socket.AF_INET6:  # IPv6
                        self.menu.console.print(f"    IPv6: {addr.address}")
                        
        except Exception as e:
            self.menu.show_warning(f"⚠️ No se pudo obtener información de interfaces: {e}")
    
    def _interactive_ping(self):
        """Permite hacer ping interactivo a servidores."""
        self.menu.clear_screen()
        
        # Servidores predefinidos
        predefined_servers = {
            '1': ('Google DNS', '8.8.8.8'),
            '2': ('Cloudflare DNS', '1.1.1.1'),
            '3': ('Google', 'google.com'),
            '4': ('GitHub', 'github.com'),
            '5': ('Microsoft', 'microsoft.com'),
            '6': ('Custom', None)
        }
        
        self.menu.console.print("[bold cyan]📡 Ping a Servidor[/bold cyan]\n")
        
        # Mostrar opciones
        for key, (name, host) in predefined_servers.items():
            if host:
                self.menu.console.print(f"  {key}. {name} ({host})")
            else:
                self.menu.console.print(f"  {key}. {name} (servidor personalizado)")
        
        choice = self.menu.get_input("\n🎯 Selecciona una opción (1-6)")
        
        if choice in predefined_servers:
            if choice == '6':
                # Servidor personalizado
                target = self.menu.get_input("🌐 Ingresa la dirección IP o dominio")
                if not target:
                    return
            else:
                _, target = predefined_servers[choice]
            
            # Configurar parámetros de ping
            count = self.menu.get_input("📊 Número de pings (default: 4)", "4")
            try:
                count = int(count)
                if count <= 0 or count > 100:
                    count = 4
            except ValueError:
                count = 4
            
            self._execute_ping(target, count)
        else:
            self.menu.show_warning("⚠️ Opción inválida")
    
    def _execute_ping(self, target: str, count: int = 4):
        """Ejecuta ping a un objetivo específico."""
        self.menu.clear_screen()
        
        self.menu.console.print(f"[bold cyan]📡 Ping a {target}[/bold cyan]\n")
        
        try:
            # Preparar comando de ping según el OS
            if os.name == 'nt':
                cmd = ['ping', '-n', str(count), target]
            else:
                cmd = ['ping', '-c', str(count), target]
            
            # Ejecutar ping en tiempo real
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                     text=True, universal_newlines=True)
            
            success_count = 0
            total_time = 0
            times = []
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                
                if output:
                    line = output.strip()
                    self.menu.console.print(line)
                    
                    # Analizar respuesta para estadísticas
                    if 'time=' in line.lower() or 'tiempo=' in line.lower():
                        success_count += 1
                        # Extraer tiempo de respuesta
                        try:
                            if 'time=' in line.lower():
                                time_part = line.lower().split('time=')[1].split()[0]
                            else:
                                time_part = line.lower().split('tiempo=')[1].split()[0]
                            
                            time_ms = float(time_part.replace('ms', ''))
                            times.append(time_ms)
                            total_time += time_ms
                        except:
                            pass
            
            # Mostrar estadísticas finales
            if success_count > 0:
                avg_time = total_time / success_count
                min_time = min(times) if times else 0
                max_time = max(times) if times else 0
                loss_percent = ((count - success_count) / count) * 100
                
                stats_table = Table(title="📊 Estadísticas de Ping", box=box.DOUBLE)
                stats_table.add_column("Métrica", style="cyan")
                stats_table.add_column("Valor", style="white")
                
                stats_table.add_row("🎯 Objetivo", target)
                stats_table.add_row("📦 Paquetes enviados", str(count))
                stats_table.add_row("✅ Paquetes recibidos", str(success_count))
                stats_table.add_row("❌ Pérdida de paquetes", f"{loss_percent:.1f}%")
                
                if times:
                    stats_table.add_row("⚡ Tiempo mínimo", f"{min_time:.1f} ms")
                    stats_table.add_row("📊 Tiempo promedio", f"{avg_time:.1f} ms")
                    stats_table.add_row("🔥 Tiempo máximo", f"{max_time:.1f} ms")
                
                self.menu.console.print("\n")
                self.menu.console.print(stats_table)
                
                # Evaluación de conectividad
                if loss_percent == 0:
                    self.menu.show_success("✅ Conectividad excelente")
                elif loss_percent < 10:
                    self.menu.show_warning("⚠️ Conectividad buena con pérdida mínima")
                elif loss_percent < 50:
                    self.menu.show_warning("⚠️ Conectividad regular con pérdida significativa")
                else:
                    self.menu.show_error("❌ Conectividad pobre o sin conexión")
            else:
                self.menu.show_error(f"❌ No se pudo conectar a {target}")
                
        except Exception as e:
            self.menu.show_error(f"❌ Error ejecutando ping: {e}")
    
    def _flush_dns(self):
        """Limpia la cache DNS del sistema."""
        self.menu.clear_screen()
        
        self.menu.console.print("[bold cyan]🔄 Flush DNS Cache[/bold cyan]\n")
        
        confirm = self.menu.get_confirmation("¿Deseas limpiar la cache DNS del sistema?")
        
        if not confirm:
            self.menu.show_info("ℹ️ Operación cancelada")
            return
        
        try:
            if os.name == 'nt':
                # Windows: usar ipconfig /flushdns
                self.menu.show_info("🔄 Limpiando cache DNS...")
                
                result = subprocess.run(['ipconfig', '/flushdns'], 
                                      capture_output=True, text=True, check=True)
                
                self.menu.show_success("✅ Cache DNS limpiada correctamente")
                
                # Mostrar salida del comando
                if result.stdout:
                    self.menu.console.print(f"\n[dim]{result.stdout}[/dim]")
                    
            else:
                # Linux/Unix: diferentes métodos según el sistema
                methods = [
                    (['sudo', 'systemctl', 'restart', 'systemd-resolved'], "systemd-resolved"),
                    (['sudo', 'service', 'nscd', 'restart'], "nscd"),
                    (['sudo', 'service', 'dnsmasq', 'restart'], "dnsmasq"),
                    (['sudo', '/etc/init.d/nscd', 'restart'], "nscd (init.d)")
                ]
                
                success = False
                for cmd, service_name in methods:
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                        self.menu.show_success(f"✅ Cache DNS limpiada usando {service_name}")
                        success = True
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                
                if not success:
                    self.menu.show_warning("⚠️ No se pudo limpiar automáticamente la cache DNS")
                    self.menu.show_info("ℹ️ Puedes intentar manualmente con:")
                    self.menu.console.print("  • sudo systemctl restart systemd-resolved")
                    self.menu.console.print("  • sudo service nscd restart")
                    
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"❌ Error limpiando cache DNS: {e}")
        except Exception as e:
            self.menu.show_error(f"❌ Error inesperado: {e}")
    
    def _show_full_network_config(self):
        """Muestra la configuración completa de red usando ipconfig."""
        self.menu.clear_screen()
        
        self.menu.console.print("[bold cyan]⚙️ Configuración Completa de Red[/bold cyan]\n")
        
        try:
            if os.name == 'nt':
                # Windows: usar ipconfig /all
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.menu.console
                ) as progress:
                    task = progress.add_task("Obteniendo configuración de red...", total=None)
                    
                    result = subprocess.run(['ipconfig', '/all'], 
                                          capture_output=True, text=True, check=True)
                
                # Mostrar la salida formateada
                lines = result.stdout.split('\n')
                current_adapter = None
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Detectar adaptadores
                    if 'adapter' in line.lower() or 'adaptador' in line.lower():
                        current_adapter = line
                        self.menu.console.print(f"\n[bold yellow]📡 {line}[/bold yellow]")
                    elif ':' in line:
                        # Información del adaptador
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Colorear según el tipo de información
                        if 'IP' in key or 'ip' in key.lower():
                            self.menu.console.print(f"  [cyan]{key}:[/cyan] [white]{value}[/white]")
                        elif 'DNS' in key or 'dns' in key.lower():
                            self.menu.console.print(f"  [green]{key}:[/green] [white]{value}[/white]")
                        elif 'Gateway' in key or 'gateway' in key.lower():
                            self.menu.console.print(f"  [yellow]{key}:[/yellow] [white]{value}[/white]")
                        else:
                            self.menu.console.print(f"  [dim]{key}:[/dim] {value}")
                    else:
                        # Otras líneas
                        self.menu.console.print(f"  {line}")
                        
            else:
                # Linux/Unix: usar ip addr y otras herramientas
                self.menu.show_info("🔄 Obteniendo configuración de red...")
                
                # ip addr show
                try:
                    result = subprocess.run(['ip', 'addr', 'show'], 
                                          capture_output=True, text=True, check=True)
                    self.menu.console.print("\n[bold yellow]📡 Interfaces de Red:[/bold yellow]")
                    self.menu.console.print(result.stdout)
                except:
                    pass
                
                # ip route show
                try:
                    result = subprocess.run(['ip', 'route', 'show'], 
                                          capture_output=True, text=True, check=True)
                    self.menu.console.print("\n[bold yellow]🛣️ Rutas de Red:[/bold yellow]")
                    self.menu.console.print(result.stdout)
                except:
                    pass
                
                # DNS servers
                try:
                    with open('/etc/resolv.conf', 'r') as f:
                        content = f.read()
                    self.menu.console.print("\n[bold yellow]🔍 Configuración DNS:[/bold yellow]")
                    self.menu.console.print(content)
                except:
                    pass
                    
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"❌ Error obteniendo configuración: {e}")
        except Exception as e:
            self.menu.show_error(f"❌ Error inesperado: {e}")
    
    def _connectivity_test(self):
        """Prueba conectividad a servicios comunes."""
        self.menu.clear_screen()
        
        self.menu.console.print("[bold cyan]🔍 Test de Conectividad[/bold cyan]\n")
        
        # Servicios a probar
        test_services = [
            ('Google DNS', '8.8.8.8'),
            ('Cloudflare DNS', '1.1.1.1'),
            ('Google', 'google.com'),
            ('GitHub', 'github.com'),
            ('Microsoft', 'microsoft.com'),
            ('Stack Overflow', 'stackoverflow.com')
        ]
        
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.menu.console
        ) as progress:
            task = progress.add_task("Probando conectividad...", total=len(test_services))
            
            for service_name, target in test_services:
                progress.update(task, description=f"Probando {service_name}...")
                
                # Hacer ping rápido (1 ping)
                try:
                    if os.name == 'nt':
                        cmd = ['ping', '-n', '1', '-w', '3000', target]
                    else:
                        cmd = ['ping', '-c', '1', '-W', '3', target]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, 
                                          check=True, timeout=5)
                    
                    # Extraer tiempo de respuesta
                    output = result.stdout.lower()
                    if 'time=' in output or 'tiempo=' in output:
                        status = "✅ Conectado"
                        # Intentar extraer tiempo
                        try:
                            if 'time=' in output:
                                time_part = output.split('time=')[1].split()[0]
                            else:
                                time_part = output.split('tiempo=')[1].split()[0]
                            time_ms = time_part.replace('ms', '')
                            status += f" ({time_ms}ms)"
                        except:
                            pass
                    else:
                        status = "✅ Conectado"
                        
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    status = "❌ Sin conexión"
                except Exception:
                    status = "⚠️ Error"
                
                results.append((service_name, target, status))
                progress.advance(task)
        
        # Mostrar resultados
        results_table = Table(title="🔍 Resultados de Conectividad", box=box.DOUBLE)
        results_table.add_column("Servicio", style="cyan", width=20)
        results_table.add_column("Objetivo", style="white", width=20)
        results_table.add_column("Estado", style="white", width=20)
        
        connected_count = 0
        for service_name, target, status in results:
            results_table.add_row(service_name, target, status)
            if "✅" in status:
                connected_count += 1
        
        self.menu.console.print("\n")
        self.menu.console.print(results_table)
        
        # Resumen de conectividad
        total_services = len(test_services)
        success_rate = (connected_count / total_services) * 100
        
        self.menu.console.print(f"\n[bold cyan]📊 Resumen:[/bold cyan]")
        self.menu.console.print(f"  Servicios probados: {total_services}")
        self.menu.console.print(f"  Conexiones exitosas: {connected_count}")
        self.menu.console.print(f"  Tasa de éxito: {success_rate:.1f}%")
        
        if success_rate >= 80:
            self.menu.show_success("✅ Conectividad excelente")
        elif success_rate >= 50:
            self.menu.show_warning("⚠️ Conectividad regular")
        else:
            self.menu.show_error("❌ Problemas de conectividad detectados")


def main():
    """Función principal del módulo."""
    sistema_module = SistemaModule()
    sistema_module.main()


if __name__ == "__main__":
    main()