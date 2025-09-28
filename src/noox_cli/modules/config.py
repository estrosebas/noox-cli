"""
Módulo de Configuración - NooxCLI
Migrado desde config-consola.bat con interfaz interactiva mejorada
Configuración de UTF-8 y personalización de consola
"""

import os
import sys
import subprocess
from typing import List, Dict, Any, Optional
from ..menu import NooxMenu
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
import winreg  # Para Windows Registry


class ConfigModule:
    """Módulo de configuración de consola y UTF-8."""
    
    def __init__(self):
        self.menu = NooxMenu("Configuración - NooxCLI")
        self.console_reg_key = r"Console"
        
    def main(self):
        """Función principal del módulo de configuración."""
        while True:
            self.menu.show_banner()
            
            # Menú principal de configuración
            choices = [
                {
                    'name': '⚡ Configuración Completa',
                    'value': 'completa',
                    'description': 'Aplicar configuración UTF-8 completa (recomendado)'
                },
                {
                    'name': '🔤 Solo UTF-8',
                    'value': 'utf8_only',
                    'description': 'Cambiar solo página de códigos a UTF-8'
                },
                {
                    'name': '🎨 Configurar Fuente',
                    'value': 'fuente',
                    'description': 'Cambiar fuente de consola'
                },
                {
                    'name': '🔄 Restaurar Configuración',
                    'value': 'restaurar',
                    'description': 'Volver a configuración predeterminada'
                },
                {
                    'name': '📊 Ver Configuración Actual',
                    'value': 'ver_config',
                    'description': 'Mostrar configuración actual del sistema'
                },
                {
                    'name': '🧪 Probar UTF-8',
                    'value': 'test_utf8',
                    'description': 'Probar caracteres especiales y UTF-8'
                },
                {
                    'name': '🔧 Diagnóstico',
                    'value': 'diagnostico',
                    'description': 'Diagnosticar problemas de codificación'
                }
            ]
            
            selection = self.menu.show_menu(choices, "🔧 ¿Qué configuración deseas aplicar?")
            
            if not selection or selection == 'exit':
                break
            
            self._handle_selection(selection)
    
    def _handle_selection(self, selection: str):
        """Maneja la selección del usuario."""
        handlers = {
            'completa': self._configuracion_completa,
            'utf8_only': self._utf8_solo,
            'fuente': self._configurar_fuente,
            'restaurar': self._restaurar_configuracion,
            'ver_config': self._ver_configuracion,
            'test_utf8': self._test_utf8,
            'diagnostico': self._diagnostico
        }
        
        if selection in handlers:
            handlers[selection]()
            self.menu.pause()
    
    def _configuracion_completa(self):
        """Aplica configuración UTF-8 completa."""
        self.menu.clear_screen()
        self.menu.show_info("⚙️ Aplicando configuración completa...")
        
        try:
            steps = [
                ("[1/4] Configurando página de códigos UTF-8...", self._set_utf8_codepage),
                ("[2/4] Configurando fuente de consola...", self._set_console_font),
                ("[3/4] Configurando opciones adicionales...", self._set_console_options),
                ("[4/4] Configurando PowerShell...", self._configure_powershell)
            ]
            
            for step_msg, step_func in steps:
                self.menu.show_info(step_msg)
                step_func()
            
            self.menu.show_success("✅ ¡Configuración completa aplicada!")
            
            # Mostrar resumen de cambios
            self._show_applied_changes()
            
            self.menu.show_warning("⚠️ IMPORTANTE: Cierra y abre una nueva consola para que")
            self.menu.show_warning("   todos los cambios surtan efecto.")
            
        except Exception as e:
            self.menu.show_error(f"Error aplicando configuración: {e}")
    
    def _utf8_solo(self):
        """Cambia solo la página de códigos a UTF-8."""
        self.menu.clear_screen()
        
        try:
            self.menu.show_info("⚙️ Cambiando página de códigos a UTF-8...")
            self._set_utf8_codepage()
            self.menu.show_success("✅ Página de códigos cambiada a UTF-8")
            
        except Exception as e:
            self.menu.show_error(f"Error cambiando página de códigos: {e}")
    
    def _configurar_fuente(self):
        """Configuración de fuente de consola."""
        self.menu.clear_screen()
        
        fuentes = [
            {'name': '🔤 Cascadia Code (recomendada)', 'value': 'Cascadia Code'},
            {'name': '📝 Consolas', 'value': 'Consolas'},
            {'name': '🔢 Cascadia Mono', 'value': 'Cascadia Mono'},
            {'name': '⚡ JetBrains Mono', 'value': 'JetBrains Mono'},
            {'name': '💻 Fira Code', 'value': 'Fira Code'}
        ]
        
        selection = self.menu.show_menu(fuentes, "🎨 Selecciona una fuente:")
        
        if selection and selection != 'exit':
            try:
                self._set_console_font(selection)
                self.menu.show_success(f"✅ Fuente configurada: {selection}")
                self.menu.show_warning("⚠️ Cierra y abre una nueva consola para ver los cambios.")
                
            except Exception as e:
                self.menu.show_error(f"Error configurando fuente: {e}")
    
    def _restaurar_configuracion(self):
        """Restaura la configuración predeterminada."""
        self.menu.clear_screen()
        
        if self.menu.show_confirmation("¿Estás seguro de restaurar la configuración predeterminada?"):
            try:
                self.menu.show_info("⚙️ Restaurando configuración predeterminada...")
                self._restore_default_config()
                self.menu.show_success("✅ Configuración restaurada")
                
            except Exception as e:
                self.menu.show_error(f"Error restaurando configuración: {e}")
    
    def _ver_configuracion(self):
        """Muestra la configuración actual del sistema."""
        self.menu.clear_screen()
        
        try:
            # Crear tabla de configuración
            table = Table(title="📊 Configuración Actual del Sistema", box=box.DOUBLE)
            table.add_column("Configuración", style="cyan", no_wrap=True)
            table.add_column("Valor", style="white")
            
            # Página de códigos activa
            codepage = self._get_current_codepage()
            table.add_row("Página de códigos", f"{codepage}")
            
            # Configuración del registro
            reg_config = self._get_registry_config()
            for key, value in reg_config.items():
                table.add_row(key, str(value))
            
            # Codificación de Python
            encoding_info = self._get_python_encoding()
            table.add_row("Python sys.stdout.encoding", encoding_info['stdout'])
            table.add_row("Python locale", encoding_info['locale'])
            
            # Codificación de PowerShell (como en el .bat original)
            ps_encoding = self._get_powershell_encoding()
            table.add_row("PowerShell OutputEncoding", ps_encoding['output'])
            table.add_row("PowerShell Console.OutputEncoding", ps_encoding['console'])
            
            self.menu.console.print(table)
            
        except Exception as e:
            self.menu.show_error(f"Error obteniendo configuración: {e}")
    
    def _test_utf8(self):
        """Prueba caracteres UTF-8 y emojis."""
        self.menu.clear_screen()
        
        test_strings = [
            ("Caracteres básicos", "áéíóú ñÑ çÇ"),
            ("Símbolos", "€ £ ¥ © ® ™ § ¶"),
            ("Emojis básicos", "😀 😎 🚀 ❤️ 🎉 ⚡ 🔥"),
            ("Símbolos técnicos", "→ ← ↑ ↓ ✓ ✗ ★ ☆"),
            ("Cajas y líneas", "╔═══╗ ║ ✓ ║ ╚═══╝"),
            ("Caracteres asiáticos", "こんにちは 你好 안녕하세요"),
            ("Matemáticas", "α β γ π Σ ∆ ∞ ≠ ≤ ≥")
        ]
        
        panel_content = Text()
        panel_content.append("🧪 Prueba de Caracteres UTF-8\n\n", style="bold cyan")
        
        for categoria, texto in test_strings:
            panel_content.append(f"{categoria}:\n", style="bold yellow")
            panel_content.append(f"  {texto}\n\n", style="white")
        
        panel = Panel(
            panel_content,
            title="🌐 Test de Codificación UTF-8",
            border_style="green",
            box=box.ROUNDED
        )
        
        self.menu.console.print(panel)
        
        # Información adicional
        self.menu.show_info("💡 Si ves caracteres extraños (�, ?, cuadros), hay problemas de codificación")
        self.menu.show_info("🔧 Usa 'Configuración Completa' para solucionarlo")
    
    def _diagnostico(self):
        """Ejecuta diagnóstico de problemas de codificación."""
        self.menu.clear_screen()
        
        self.menu.show_info("🔍 Ejecutando diagnóstico de codificación...")
        
        diagnostics = []
        
        # Verificar página de códigos
        codepage = self._get_current_codepage()
        if codepage == "65001":
            diagnostics.append(("✅", "Página de códigos", "UTF-8 activo"))
        else:
            diagnostics.append(("❌", "Página de códigos", f"Actual: {codepage}, Esperado: 65001"))
        
        # Verificar configuración del registro
        reg_config = self._get_registry_config()
        if 'CodePage' in reg_config and reg_config['CodePage'] == 65001:
            diagnostics.append(("✅", "Registro CodePage", "Configurado correctamente"))
        else:
            diagnostics.append(("⚠️", "Registro CodePage", "No configurado para UTF-8"))
        
        # Verificar Python encoding
        encoding_info = self._get_python_encoding()
        if 'utf-8' in encoding_info['stdout'].lower():
            diagnostics.append(("✅", "Python encoding", "UTF-8 activo"))
        else:
            diagnostics.append(("❌", "Python encoding", f"Actual: {encoding_info['stdout']}"))
        
        # Mostrar resultados
        table = Table(title="🔍 Diagnóstico de Codificación", box=box.DOUBLE)
        table.add_column("Estado", style="white", width=4)
        table.add_column("Componente", style="cyan")
        table.add_column("Resultado", style="white")
        
        for status, component, result in diagnostics:
            table.add_row(status, component, result)
        
        self.menu.console.print(table)
        
        # Recomendaciones
        problemas = [d for d in diagnostics if d[0] == "❌"]
        if problemas:
            self.menu.show_warning(f"Se encontraron {len(problemas)} problema(s)")
            self.menu.show_info("💡 Ejecuta 'Configuración Completa' para solucionarlos")
        else:
            self.menu.show_success("¡Todo está configurado correctamente!")
    
    # Métodos auxiliares
    def _set_utf8_codepage(self):
        """Establece la página de códigos UTF-8."""
        if os.name == 'nt':
            subprocess.run(['chcp', '65001'], shell=True, capture_output=True)
    
    def _set_console_font(self, font_name: str = "Cascadia Code"):
        """Configura la fuente de consola."""
        if os.name == 'nt':
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.console_reg_key, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, "FaceName", 0, winreg.REG_SZ, font_name)
                    winreg.SetValueEx(key, "FontFamily", 0, winreg.REG_DWORD, 54)
                    winreg.SetValueEx(key, "FontSize", 0, winreg.REG_DWORD, 1048576)
                    winreg.SetValueEx(key, "FontWeight", 0, winreg.REG_DWORD, 400)
            except Exception:
                # Fallback usando PowerShell
                ps_commands = [
                    f"Set-ItemProperty -Path 'HKCU:\\Console' -Name 'FaceName' -Value '{font_name}'",
                    "Set-ItemProperty -Path 'HKCU:\\Console' -Name 'FontFamily' -Value 54",
                    "Set-ItemProperty -Path 'HKCU:\\Console' -Name 'FontSize' -Value 1048576"
                ]
                for cmd in ps_commands:
                    subprocess.run(['powershell', '-Command', cmd], shell=True, capture_output=True)
    
    def _set_console_options(self):
        """Configura opciones adicionales de consola."""
        if os.name == 'nt':
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.console_reg_key, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, "CodePage", 0, winreg.REG_DWORD, 65001)
                    winreg.SetValueEx(key, "CurrentCodePage", 0, winreg.REG_DWORD, 65001)
            except Exception:
                # Fallback usando PowerShell
                ps_commands = [
                    "Set-ItemProperty -Path 'HKCU:\\Console' -Name 'CodePage' -Value 65001",
                    "Set-ItemProperty -Path 'HKCU:\\Console' -Name 'CurrentCodePage' -Value 65001"
                ]
                for cmd in ps_commands:
                    subprocess.run(['powershell', '-Command', cmd], shell=True, capture_output=True)
    
    def _configure_powershell(self):
        """Configura PowerShell para UTF-8."""
        if os.name == 'nt':
            ps_commands = [
                "$OutputEncoding = [System.Text.Encoding]::UTF8",
                "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8"
            ]
            for cmd in ps_commands:
                subprocess.run(['powershell', '-Command', cmd], shell=True, capture_output=True)
    
    def _restore_default_config(self):
        """Restaura la configuración predeterminada."""
        if os.name == 'nt':
            try:
                # Intentar eliminar configuraciones del registro
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.console_reg_key, 0, winreg.KEY_SET_VALUE) as key:
                    try:
                        winreg.DeleteValue(key, "CodePage")
                        winreg.DeleteValue(key, "FontFamily")
                        winreg.DeleteValue(key, "FontSize")
                        winreg.DeleteValue(key, "FaceName")
                    except FileNotFoundError:
                        pass  # Valor no existe, está bien
            except Exception:
                # Fallback usando PowerShell
                ps_commands = [
                    "Remove-ItemProperty -Path 'HKCU:\\Console' -Name 'CodePage' -ErrorAction SilentlyContinue",
                    "Remove-ItemProperty -Path 'HKCU:\\Console' -Name 'FontFamily' -ErrorAction SilentlyContinue",
                    "Remove-ItemProperty -Path 'HKCU:\\Console' -Name 'FontSize' -ErrorAction SilentlyContinue",
                    "Remove-ItemProperty -Path 'HKCU:\\Console' -Name 'FaceName' -ErrorAction SilentlyContinue"
                ]
                for cmd in ps_commands:
                    subprocess.run(['powershell', '-Command', cmd], shell=True, capture_output=True)
            
            # Cambiar a página de códigos predeterminada
            subprocess.run(['chcp', '850'], shell=True, capture_output=True)
    
    def _get_current_codepage(self) -> str:
        """Obtiene la página de códigos actual."""
        try:
            result = subprocess.run(['chcp'], shell=True, capture_output=True, text=True)
            if result.stdout:
                # Extraer número de la salida "Active code page: 65001"
                return result.stdout.strip().split(':')[-1].strip()
        except Exception:
            pass
        return "Desconocido"
    
    def _get_registry_config(self) -> Dict[str, Any]:
        """Obtiene configuración del registro."""
        config = {}
        if os.name == 'nt':
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.console_reg_key, 0, winreg.KEY_READ) as key:
                    for value_name in ['CodePage', 'FontFamily', 'FontSize', 'FontWeight', 'FaceName']:
                        try:
                            value, _ = winreg.QueryValueEx(key, value_name)
                            config[value_name] = value
                        except FileNotFoundError:
                            config[value_name] = "No configurado"
            except Exception:
                config['Error'] = "No se pudo acceder al registro"
        
        return config
    
    def _get_python_encoding(self) -> Dict[str, str]:
        """Obtiene información de codificación de Python."""
        import locale
        return {
            'stdout': sys.stdout.encoding or "No disponible",
            'locale': locale.getpreferredencoding()
        }
    
    def _get_powershell_encoding(self) -> Dict[str, str]:
        """Obtiene información de codificación de PowerShell."""
        try:
            # Obtener OutputEncoding de PowerShell
            result_output = subprocess.run([
                'powershell', '-Command', 
                'Write-Host $OutputEncoding.EncodingName -NoNewline'
            ], capture_output=True, text=True, shell=True)
            
            # Obtener Console.OutputEncoding de PowerShell
            result_console = subprocess.run([
                'powershell', '-Command', 
                'Write-Host [Console]::OutputEncoding.EncodingName -NoNewline'
            ], capture_output=True, text=True, shell=True)
            
            return {
                'output': result_output.stdout.strip() if result_output.stdout else "No disponible",
                'console': result_console.stdout.strip() if result_console.stdout else "No disponible"
            }
        except Exception:
            return {
                'output': "Error al obtener",
                'console': "Error al obtener"
            }
    
    def _show_applied_changes(self):
        """Muestra un resumen de los cambios aplicados."""
        changes_text = Text()
        changes_text.append("📝 Cambios aplicados:\n\n", style="bold cyan")
        changes_text.append("• Página de códigos: UTF-8 (65001)\n", style="green")
        changes_text.append("• Fuente: Cascadia Code/Consolas\n", style="green")
        changes_text.append("• Codificación de salida: UTF-8\n", style="green")
        changes_text.append("• Configuración del registro actualizada\n", style="green")
        
        panel = Panel(
            changes_text,
            title="✅ Configuración Aplicada",
            border_style="green",
            box=box.ROUNDED
        )
        
        self.menu.console.print(panel)


def main():
    """Función principal del módulo."""
    config_module = ConfigModule()
    config_module.main()


if __name__ == "__main__":
    main()
