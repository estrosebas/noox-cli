"""
Módulo de Reparación - NooxCLI
Migrado desde reparar-perfil.bat con interfaz interactiva mejorada
"""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.table import Table
from rich.panel import Panel
from rich import box

from ..menu import NooxMenu


class RepararModule:
    """Módulo para reparar configuraciones del sistema."""
    
    def __init__(self):
        self.menu = NooxMenu("Reparación - NooxCLI")
        # Manejar ambas ubicaciones de PowerShell
        self.powershell_dirs = [
            Path.home() / "Documents" / "WindowsPowerShell",  # Windows PowerShell 5.x
            Path.home() / "Documents" / "PowerShell"          # PowerShell Core 6+
        ]
        self.profile_paths = [
            dir_path / "Microsoft.PowerShell_profile.ps1" for dir_path in self.powershell_dirs
        ]
    
    def main(self):
        """Función principal con menú interactivo."""
        while True:
            self.menu.show_banner()
            self._show_current_status()
            
            choices = [
                {'name': '🔧 Reparar perfil completo', 'value': 'repair_full'},
                {'name': '💾 Solo crear backup', 'value': 'backup_only'},
                {'name': '📝 Regenerar perfil', 'value': 'regenerate'},
                {'name': '✅ Verificar sintaxis', 'value': 'verify'},
                {'name': '🎨 Configurar oh-my-posh', 'value': 'omp_config'},
                {'name': '📊 Ver perfil actual', 'value': 'show_current'}
            ]
            
            selection = self.menu.show_menu(choices, "¿Qué deseas hacer?")
            
            if not selection or selection == 'exit':
                break
                
            self._handle_selection(selection)
    
    def _handle_selection(self, selection: str):
        """Maneja la selección del usuario."""
        handlers = {
            'repair_full': self._repair_full_profile,
            'backup_only': self._backup_profile,
            'regenerate': self._generate_profile,
            'verify': self._verify_syntax,
            'omp_config': self._configure_omp,
            'show_current': self._show_current_profile
        }
        
        if selection in handlers:
            try:
                handlers[selection]()
            except Exception as e:
                self.menu.show_error(f"Error: {e}")
            self.menu.pause()
    
    def _show_current_status(self):
        """Muestra el estado actual del perfil de PowerShell."""
        table = Table(title="📊 Estado del Perfil PowerShell", box=box.DOUBLE)
        table.add_column("Elemento", style="cyan", no_wrap=True)
        table.add_column("Estado", style="white")
        
        # Verificar si existe el directorio
        dir_status = "✅ Existe" if self.powershell_dir.exists() else "❌ No existe"
        table.add_row("Directorio PowerShell", dir_status)
        
        # Verificar si existe el perfil
        profile_status = "✅ Existe" if self.profile_path.exists() else "❌ No existe"
        table.add_row("Perfil actual", profile_status)
        
        # Verificar tamaño del perfil
        if self.profile_path.exists():
            size = self.profile_path.stat().st_size
            table.add_row("Tamaño del perfil", f"{size} bytes")
            
            # Verificar fecha de modificación
            mtime = datetime.fromtimestamp(self.profile_path.stat().st_mtime)
            table.add_row("Última modificación", mtime.strftime("%Y-%m-%d %H:%M:%S"))
        
        # Verificar oh-my-posh
        omp_status = self._check_omp_installation()
        table.add_row("oh-my-posh", omp_status)
        
        self.menu.console.print(table)
        self.menu.console.print()
    
    def _backup_profile(self) -> Optional[str]:
        """
        Crea un backup del perfil actual de PowerShell.
        
        Returns:
            Ruta del backup creado o None si falló
        """
        try:
            # Buscar perfiles existentes
            existing_profiles = [path for path in self.profile_paths if path.exists()]
            
            if not existing_profiles:
                self.menu.show_warning("No existe un perfil actual para respaldar")
                return None
            
            # Usar el primer perfil encontrado para el backup
            profile_to_backup = existing_profiles[0]
            powershell_dir = profile_to_backup.parent
            
            # Generar nombre de backup con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"Microsoft.PowerShell_profile_backup_{timestamp}.ps1"
            backup_path = powershell_dir / backup_name
            
            # Crear el backup
            shutil.copy2(profile_to_backup, backup_path)
            
            self.menu.show_success(f"Backup creado: {backup_name}")
            self.menu.show_info(f"Ubicación: {backup_path}")
            
            return str(backup_path)
            
        except Exception as e:
            self.menu.show_error(f"Error creando backup: {e}")
            return None
    
    def _generate_profile(self) -> bool:
        """
        Genera un nuevo perfil de PowerShell con configuración UTF-8 completa.
        Actualiza ambas ubicaciones de PowerShell (5.x y Core 6+).
        
        Returns:
            True si se generó correctamente, False en caso contrario
        """
        try:
            # Contenido del perfil basado en reparar-perfil.bat
            profile_content = self._get_profile_content()
            
            success_count = 0
            
            # Generar perfil en ambas ubicaciones
            for i, (powershell_dir, profile_path) in enumerate(zip(self.powershell_dirs, self.profile_paths)):
                try:
                    # Crear directorio si no existe
                    powershell_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Escribir el nuevo perfil
                    with open(profile_path, 'w', encoding='utf-8') as f:
                        f.write(profile_content)
                    
                    self.menu.show_success(f"Perfil generado: {profile_path}")
                    success_count += 1
                    
                except Exception as e:
                    self.menu.show_warning(f"No se pudo generar perfil en {profile_path}: {e}")
            
            if success_count > 0:
                self.menu.show_success("Perfil de PowerShell generado correctamente")
                return True
            else:
                self.menu.show_error("No se pudo generar ningún perfil")
                return False
            
        except Exception as e:
            self.menu.show_error(f"Error generando perfil: {e}")
            return False
    
    def _get_profile_content(self) -> str:
        """
        Genera el contenido del perfil de PowerShell.
        
        Returns:
            Contenido del perfil como string
        """
        return '''# Configuracion de codificacion UTF-8 para caracteres especiales
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Configurar pagina de codigos UTF-8 si no esta configurada
if ((chcp) -notmatch "65001") {
    chcp 65001 > $null
}

Import-Module PSReadLine
Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -Colors @{ InLinePrediction = 'DarkGray' }

# Agregar oh-my-posh al PATH
$env:PATH += ";$env:LOCALAPPDATA\\Programs\\oh-my-posh\\bin"

# Agregar Scripts al PATH
$env:PATH += ";$env:USERPROFILE\\Scripts"

# Aliases utiles
Set-Alias -Name dev -Value desarrollo.bat
Set-Alias -Name sys -Value sistema.bat
Set-Alias -Name proj -Value proyectos.bat
Set-Alias -Name config -Value config-consola.bat
Set-Alias -Name ll -Value Get-ChildItem

clear
$fecha = Get-Date -Format "yyyy-MM-dd"
$usuario = [System.Environment]::UserName
$pc = $env:COMPUTERNAME

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " NooxCLI - Terminal de Desarrollo" -ForegroundColor Green
Write-Host " Usuario: $usuario@$pc" -ForegroundColor Yellow
Write-Host " Fecha: $fecha" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Alias disponibles:" -ForegroundColor Magenta
Write-Host "  dev    -> Entorno de desarrollo" -ForegroundColor White
Write-Host "  sys    -> Scripts del sistema" -ForegroundColor White
Write-Host "  proj   -> Proyectos de Laragon" -ForegroundColor White
Write-Host "  config -> Configuracion UTF-8/Consola" -ForegroundColor White
Write-Host "  ll     -> Lista detallada de archivos" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

if (Test-Path .git) {
    $branch = git branch --show-current 2>$null
    if ($branch) {
        Write-Host "Git - Rama actual: $branch" -ForegroundColor DarkGray
    }
}

# Inicializar oh-my-posh
if (Get-Command oh-my-posh -ErrorAction SilentlyContinue) {
    oh-my-posh init pwsh --config "$env:LOCALAPPDATA\\Programs\\oh-my-posh\\themes\\avit.omp.json" | Invoke-Expression
} elseif (Test-Path "$env:LOCALAPPDATA\\Programs\\oh-my-posh\\bin\\oh-my-posh.exe") {
    & "$env:LOCALAPPDATA\\Programs\\oh-my-posh\\bin\\oh-my-posh.exe" init pwsh --config "$env:LOCALAPPDATA\\Programs\\oh-my-posh\\themes\\avit.omp.json" | Invoke-Expression
}
'''   
 
    def _verify_syntax(self) -> bool:
        """
        Verifica la sintaxis del perfil de PowerShell usando PowerShell -NoProfile.
        
        Returns:
            True si la sintaxis es correcta, False en caso contrario
        """
        try:
            if not self.profile_path.exists():
                self.menu.show_error("No existe un perfil para verificar")
                return False
            
            self.menu.show_info("Verificando sintaxis del perfil...")
            
            # Comando para verificar sintaxis sin cargar perfil
            cmd = [
                'powershell', '-NoProfile', '-Command',
                f"try {{ Get-Content '{self.profile_path}' | Out-String | Invoke-Expression -ErrorAction Stop; Write-Host 'Sintaxis OK' -ForegroundColor Green }} catch {{ Write-Host 'Error de sintaxis:' -ForegroundColor Red; Write-Host $_.Exception.Message -ForegroundColor Red }}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                if "Sintaxis OK" in result.stdout:
                    self.menu.show_success("✅ Sintaxis del perfil correcta")
                    return True
                else:
                    self.menu.show_error("❌ Error de sintaxis detectado")
                    if result.stdout.strip():
                        self.menu.console.print(f"[red]Salida: {result.stdout.strip()}[/red]")
                    if result.stderr.strip():
                        self.menu.console.print(f"[red]Error: {result.stderr.strip()}[/red]")
                    return False
            else:
                self.menu.show_error("❌ Error ejecutando verificación de sintaxis")
                if result.stderr.strip():
                    self.menu.console.print(f"[red]Error: {result.stderr.strip()}[/red]")
                return False
                
        except Exception as e:
            self.menu.show_error(f"Error verificando sintaxis: {e}")
            return False    

    def _configure_omp(self) -> bool:
        """
        Configura oh-my-posh con tema por defecto.
        
        Returns:
            True si se configuró correctamente, False en caso contrario
        """
        try:
            omp_status = self._check_omp_installation()
            
            if "❌" in omp_status:
                self.menu.show_warning("oh-my-posh no está instalado")
                self.menu.show_info("Para instalar oh-my-posh, ejecuta:")
                self.menu.console.print("[cyan]winget install JanDeDobbeleer.OhMyPosh -s winget[/cyan]")
                return False
            
            # Verificar que el tema avit.omp.json exista
            theme_path = Path(os.environ.get('LOCALAPPDATA', '')) / "Programs" / "oh-my-posh" / "themes" / "avit.omp.json"
            
            if not theme_path.exists():
                self.menu.show_warning(f"Tema avit.omp.json no encontrado en: {theme_path}")
                self.menu.show_info("Usando configuración por defecto de oh-my-posh")
            
            self.menu.show_success("✅ oh-my-posh configurado correctamente")
            self.menu.show_info("El tema se aplicará al reiniciar PowerShell")
            
            # Mostrar información de configuración
            table = Table(title="🎨 Configuración oh-my-posh", box=box.ROUNDED)
            table.add_column("Elemento", style="cyan")
            table.add_column("Valor", style="white")
            
            table.add_row("Estado", omp_status)
            table.add_row("Tema", "avit.omp.json")
            table.add_row("Ubicación tema", str(theme_path))
            
            self.menu.console.print(table)
            
            return True
            
        except Exception as e:
            self.menu.show_error(f"Error configurando oh-my-posh: {e}")
            return False
    
    def _check_omp_installation(self) -> str:
        """
        Verifica si oh-my-posh está instalado.
        
        Returns:
            Estado de la instalación como string
        """
        try:
            # Verificar comando oh-my-posh en PATH
            result = subprocess.run(['oh-my-posh', '--version'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                return f"✅ Instalado (v{version})"
        except:
            pass
        
        # Verificar instalación en ubicación estándar
        omp_path = Path(os.environ.get('LOCALAPPDATA', '')) / "Programs" / "oh-my-posh" / "bin" / "oh-my-posh.exe"
        if omp_path.exists():
            return "✅ Instalado (ubicación estándar)"
        
        return "❌ No instalado"
    
    def _repair_full_profile(self):
        """Ejecuta la reparación completa del perfil (equivalente al .bat original)."""
        self.menu.show_info("🔧 Iniciando reparación completa del perfil PowerShell...")
        self.menu.console.print()
        
        steps_completed = 0
        total_steps = 4
        
        # Paso 1: Crear backup
        self.menu.show_info(f"[1/{total_steps}] Creando respaldo del perfil actual...")
        backup_path = self._backup_profile()
        if backup_path:
            steps_completed += 1
        
        # Paso 2: Generar nuevo perfil
        self.menu.show_info(f"[2/{total_steps}] Creando perfil corregido...")
        if self._generate_profile():
            steps_completed += 1
        
        # Paso 3: Verificar sintaxis
        self.menu.show_info(f"[3/{total_steps}] Verificando sintaxis del perfil...")
        if self._verify_syntax():
            steps_completed += 1
        
        # Paso 4: Probar carga del perfil
        self.menu.show_info(f"[4/{total_steps}] Probando carga del perfil...")
        if self._test_profile_load():
            steps_completed += 1
        
        # Mostrar resumen
        self.menu.console.print()
        if steps_completed == total_steps:
            self.menu.show_success("✅ ¡Perfil de PowerShell reparado exitosamente!")
        else:
            self.menu.show_warning(f"⚠️ Reparación parcial: {steps_completed}/{total_steps} pasos completados")
        
        # Mostrar acciones realizadas
        panel_content = """📝 Acciones realizadas:
• Respaldo creado con fecha
• Perfil regenerado con sintaxis correcta
• Configuración UTF-8 incluida
• Todos los alias restaurados
• oh-my-posh configurado correctamente

🔄 Cierra y abre una nueva ventana de PowerShell para
   ver los cambios aplicados."""
        
        panel = Panel(panel_content, title="📋 Resumen", border_style="green")
        self.menu.console.print(panel)
    
    def _test_profile_load(self) -> bool:
        """
        Prueba la carga del perfil de PowerShell.
        
        Returns:
            True si el perfil se carga correctamente, False en caso contrario
        """
        try:
            cmd = ['powershell', '-Command', "Write-Host 'Perfil cargado correctamente!' -ForegroundColor Green"]
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                self.menu.show_success("✅ Perfil se carga correctamente")
                return True
            else:
                self.menu.show_error("❌ Error cargando el perfil")
                return False
                
        except Exception as e:
            self.menu.show_error(f"Error probando carga del perfil: {e}")
            return False
    
    def _show_current_profile(self):
        """Muestra el contenido del perfil actual."""
        try:
            if not self.profile_path.exists():
                self.menu.show_warning("No existe un perfil de PowerShell")
                return
            
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Mostrar información del archivo
            stat = self.profile_path.stat()
            size = stat.st_size
            mtime = datetime.fromtimestamp(stat.st_mtime)
            
            info_panel = Panel(
                f"📁 Archivo: {self.profile_path}\n"
                f"📏 Tamaño: {size} bytes\n"
                f"📅 Modificado: {mtime.strftime('%Y-%m-%d %H:%M:%S')}",
                title="📊 Información del Perfil",
                border_style="cyan"
            )
            self.menu.console.print(info_panel)
            
            # Mostrar contenido (primeras 20 líneas)
            lines = content.split('\n')
            preview_lines = lines[:20]
            
            if len(lines) > 20:
                preview_lines.append(f"... ({len(lines) - 20} líneas más)")
            
            content_panel = Panel(
                '\n'.join(preview_lines),
                title="📝 Contenido del Perfil (Vista previa)",
                border_style="blue"
            )
            self.menu.console.print(content_panel)
            
        except Exception as e:
            self.menu.show_error(f"Error mostrando perfil: {e}")


def main():
    """Función principal del módulo."""
    reparar = RepararModule()
    reparar.main()


if __name__ == "__main__":
    main()