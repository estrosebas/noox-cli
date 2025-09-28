"""
Módulo de Test UTF-8 - NooxCLI
Migrado desde test-utf8.bat con interfaz interactiva mejorada
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Dict, Any, Optional
from ..menu import NooxMenu
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box


class TestUtf8Module:
    """Módulo de pruebas UTF-8 y caracteres especiales."""
    
    def __init__(self):
        self.menu = NooxMenu("Test UTF-8 - NooxCLI")
        
    def main(self):
        """Función principal del módulo de test UTF-8."""
        while True:
            self.menu.show_banner()
            
            # Mostrar información de codificación actual
            self._show_current_encoding()
            self.menu.console.print()
            
            # Menú principal
            choices = [
                {
                    'name': '🎯 Test completo UTF-8',
                    'value': 'full_test',
                    'description': 'Ejecutar todas las pruebas de caracteres'
                },
                {
                    'name': '📝 Solo caracteres básicos',
                    'value': 'basic_chars',
                    'description': 'Probar ñ, acentos, diéresis'
                },
                {
                    'name': '📦 Símbolos de caja',
                    'value': 'box_chars',
                    'description': 'Box drawing characters'
                },
                {
                    'name': '🎨 Emojis y símbolos',
                    'value': 'emojis',
                    'description': 'Emojis y símbolos Unicode'
                },
                {
                    'name': '🌈 Test de colores',
                    'value': 'colors',
                    'description': 'Códigos de color ANSI'
                },
                {
                    'name': '🔍 Diagnóstico completo',
                    'value': 'diagnostic',
                    'description': 'Información detallada de codificación'
                },
                {
                    'name': '💻 Info codificación',
                    'value': 'encoding_info',
                    'description': 'Mostrar configuración actual'
                }
            ]
            
            selection = self.menu.show_menu(choices, "¿Qué prueba quieres ejecutar?")
            
            if not selection or selection == 'exit':
                break
                
            self._handle_selection(selection)
    
    def _handle_selection(self, selection: str):
        """Maneja la selección del usuario."""
        handlers = {
            'full_test': self._run_full_test,
            'basic_chars': self._test_basic_chars,
            'box_chars': self._test_box_chars,
            'emojis': self._test_emojis,
            'colors': self._test_colors,
            'diagnostic': self._diagnostic_encoding,
            'encoding_info': self._show_encoding_info
        }
        
        if selection in handlers:
            try:
                handlers[selection]()
            except Exception as e:
                self.menu.show_error(f"Error ejecutando prueba: {e}")
            self.menu.pause()
    
    def _show_current_encoding(self):
        """Muestra información básica de codificación actual."""
        try:
            # Obtener página de códigos actual
            if platform.system() == "Windows":
                result = subprocess.run(['chcp'], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    codepage = result.stdout.strip()
                else:
                    codepage = "No disponible"
            else:
                codepage = f"UTF-8 (Locale: {os.environ.get('LANG', 'No definido')})"
            
            encoding_info = f"📊 Página de códigos: {codepage}"
            self.menu.show_info(encoding_info)
            
        except Exception as e:
            self.menu.show_warning(f"No se pudo obtener información de codificación: {e}")
    
    def _test_basic_chars(self):
        """Prueba caracteres especiales básicos."""
        self.menu.show_info("🎯 CARACTERES ESPECIALES BÁSICOS")
        
        # Crear tabla para mostrar caracteres organizados
        table = Table(title="📝 Caracteres Especiales", box=box.DOUBLE)
        table.add_column("Idioma/Tipo", style="cyan", no_wrap=True)
        table.add_column("Caracteres", style="white")
        
        # Caracteres españoles
        table.add_row("Español", "ñ Ñ á é í ó ú Á É Í Ó Ú ü Ü ¿ ¡")
        
        # Caracteres franceses
        table.add_row("Francés", "àèìòù ÀÈÌÒÙ âêîôû ÂÊÎÔÛ ç Ç œ Œ")
        
        # Caracteres alemanes
        table.add_row("Alemán", "ä ö ü Ä Ö Ü ß")
        
        # Caracteres nórdicos
        table.add_row("Nórdico", "æ Æ ø Ø å Å")
        
        # Caracteres portugueses
        table.add_row("Portugués", "ã õ Ã Õ ç Ç")
        
        # Caracteres italianos
        table.add_row("Italiano", "à è ì ò ù À È Ì Ò Ù")
        
        self.menu.console.print(table)
        self.menu.console.print()
        
        # Mostrar resultado de la prueba
        result_panel = Panel(
            "[green]✅ Si puedes ver correctamente todos los caracteres especiales arriba, "
            "tu configuración UTF-8 está funcionando bien para caracteres básicos.[/green]\n\n"
            "[yellow]⚠️ Si algunos caracteres se ven como cuadros □ o signos de interrogación ?, "
            "necesitas ejecutar la configuración de consola.[/yellow]",
            title="🎯 Resultado de la Prueba",
            border_style="blue"
        )
        self.menu.console.print(result_panel)
    
    def _test_box_chars(self):
        """Prueba símbolos de caja (box drawing characters)."""
        self.menu.show_info("📦 SÍMBOLOS DE CAJA")
        
        # Crear panel con diferentes estilos de cajas
        box_examples = Text()
        
        # Estilo simple
        box_examples.append("Estilo Simple:\n", style="cyan bold")
        box_examples.append("┌─┬─┐\n")
        box_examples.append("│ │ │\n")
        box_examples.append("├─┼─┤\n")
        box_examples.append("│ │ │\n")
        box_examples.append("└─┴─┘\n\n")
        
        # Estilo doble
        box_examples.append("Estilo Doble:\n", style="cyan bold")
        box_examples.append("╔═╦═╗\n")
        box_examples.append("║ ║ ║\n")
        box_examples.append("╠═╬═╣\n")
        box_examples.append("║ ║ ║\n")
        box_examples.append("╚═╩═╝\n\n")
        
        # Estilo redondeado
        box_examples.append("Estilo Redondeado:\n", style="cyan bold")
        box_examples.append("╭───╮\n")
        box_examples.append("│   │\n")
        box_examples.append("├───┤\n")
        box_examples.append("│   │\n")
        box_examples.append("╰───╯\n\n")
        
        # Caracteres individuales
        box_examples.append("Caracteres Individuales:\n", style="cyan bold")
        box_examples.append("┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ─ │\n")
        box_examples.append("╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬ ═ ║\n")
        box_examples.append("╭ ╮ ╰ ╯ ╞ ╡ ╤ ╧ ╪ ╌ ╎\n\n")
        
        # Ejemplo de caja compleja
        box_examples.append("Ejemplo Complejo:\n", style="cyan bold")
        box_examples.append("╔══════════════════════╗\n")
        box_examples.append("║ ┌──────────────────┐ ║\n")
        box_examples.append("║ │ Caja anidada     │ ║\n")
        box_examples.append("║ │ ╭──────────────╮ │ ║\n")
        box_examples.append("║ │ │ Nivel 3      │ │ ║\n")
        box_examples.append("║ │ ╰──────────────╯ │ ║\n")
        box_examples.append("║ └──────────────────┘ ║\n")
        box_examples.append("╚══════════════════════╝\n")
        
        panel = Panel(
            box_examples,
            title="📦 Símbolos de Caja (Box Drawing)",
            border_style="blue"
        )
        self.menu.console.print(panel)
        self.menu.console.print()
        
        # Mostrar resultado
        result_panel = Panel(
            "[green]✅ Si puedes ver correctamente todas las cajas y líneas arriba, "
            "tu terminal soporta bien los caracteres de dibujo.[/green]\n\n"
            "[yellow]⚠️ Si las cajas se ven rotas o con caracteres extraños, "
            "puede que necesites una fuente compatible como Cascadia Code o Consolas.[/yellow]",
            title="🎯 Resultado de la Prueba",
            border_style="blue"
        )
        self.menu.console.print(result_panel)
    
    def _test_emojis(self):
        """Prueba emojis y símbolos Unicode."""
        self.menu.show_info("🎨 EMOJIS Y SÍMBOLOS UNICODE")
        
        # Crear tabla para organizar los símbolos
        table = Table(title="🎨 Emojis y Símbolos", box=box.DOUBLE)
        table.add_column("Categoría", style="cyan", no_wrap=True)
        table.add_column("Símbolos", style="white")
        
        # Emojis de desarrollo
        table.add_row("Desarrollo", "💻 🚀 ⚡ 🔥 ✨ 🎯 📁 📝 🌐 ⚙️")
        
        # Emojis de estado
        table.add_row("Estado", "✅ ❌ ⚠️ 📊 🎉 💡 🔧 🎪 🌟 🏆")
        
        # Símbolos matemáticos
        table.add_row("Matemáticos", "π ∑ ∆ ∞ ± × ÷ √ ∫ ∂")
        
        # Letras griegas
        table.add_row("Griego", "α β γ δ λ μ σ Ω θ φ")
        
        # Flechas
        table.add_row("Flechas", "← ↑ → ↓ ↔ ↕ ⇐ ⇑ ⇒ ⇓")
        
        # Símbolos de moneda
        table.add_row("Monedas", "$ € £ ¥ ¢ ₹ ₽ ₩ ₪ ₫")
        
        # Caracteres de programación
        table.add_row("Programación", "{ } [ ] < > ( ) \" ' `")
        
        # Símbolos técnicos
        table.add_row("Técnicos", "| \\ / ~ # @ & * % ^")
        
        # Símbolos adicionales
        table.add_row("Especiales", "© ® ™ § ¶ † ‡ • ‰ ‱")
        
        # Símbolos de música
        table.add_row("Música", "♪ ♫ ♬ ♭ ♮ ♯ 𝄞 𝄢 𝄡 𝄠")
        
        # Símbolos de juegos
        table.add_row("Juegos", "♠ ♣ ♥ ♦ ♤ ♧ ♡ ♢")
        
        # Símbolos de clima
        table.add_row("Clima", "☀ ☁ ☂ ☃ ❄ ⛅ ⛈ 🌈 ⭐ 🌙")
        
        self.menu.console.print(table)
        self.menu.console.print()
        
        # Mostrar algunos emojis especiales en panel separado
        special_emojis = Text()
        special_emojis.append("Emojis Especiales de Desarrollo:\n", style="cyan bold")
        special_emojis.append("🐍 Python  ")
        special_emojis.append("🟨 JavaScript  ")
        special_emojis.append("⚛️ React  ")
        special_emojis.append("🅰️ Angular\n")
        special_emojis.append("🔗 Node.js  ")
        special_emojis.append("🐳 Docker  ")
        special_emojis.append("☸️ Kubernetes  ")
        special_emojis.append("🔥 Firebase\n")
        special_emojis.append("📱 Mobile  ")
        special_emojis.append("🌐 Web  ")
        special_emojis.append("🖥️ Desktop  ")
        special_emojis.append("☁️ Cloud\n")
        
        emoji_panel = Panel(
            special_emojis,
            title="🚀 Emojis de Tecnología",
            border_style="green"
        )
        self.menu.console.print(emoji_panel)
        self.menu.console.print()
        
        # Mostrar resultado
        result_panel = Panel(
            "[green]✅ Si puedes ver correctamente todos los emojis y símbolos arriba, "
            "tu terminal tiene excelente soporte Unicode.[/green]\n\n"
            "[yellow]⚠️ Si algunos emojis se ven como cuadros o caracteres extraños, "
            "tu fuente o terminal puede tener soporte limitado para Unicode.[/yellow]\n\n"
            "[blue]💡 Para mejor soporte de emojis, usa Windows Terminal con fuente Cascadia Code.[/blue]",
            title="🎯 Resultado de la Prueba",
            border_style="blue"
        )
        self.menu.console.print(result_panel)
    
    def _test_colors(self):
        """Prueba códigos de color ANSI."""
        self.menu.show_info("🌈 PRUEBA DE COLORES ANSI")
        
        # Verificar soporte de colores
        color_support = self._check_color_support()
        
        if color_support:
            self.menu.console.print("[green]✅ Tu terminal soporta colores ANSI[/green]")
        else:
            self.menu.console.print("[yellow]⚠️ Soporte de colores limitado detectado[/yellow]")
        
        self.menu.console.print()
        
        # Colores básicos con Rich
        self.menu.console.print("[bold cyan]Colores Básicos (Rich):[/bold cyan]")
        colors_basic = [
            ("[red]Rojo[/red]", "red"),
            ("[green]Verde[/green]", "green"), 
            ("[yellow]Amarillo[/yellow]", "yellow"),
            ("[blue]Azul[/blue]", "blue"),
            ("[magenta]Magenta[/magenta]", "magenta"),
            ("[cyan]Cian[/cyan]", "cyan"),
            ("[white]Blanco[/white]", "white"),
            ("[black on white]Negro[/black on white]", "black")
        ]
        
        color_line = ""
        for color_text, _ in colors_basic:
            color_line += f"{color_text} "
        
        self.menu.console.print(color_line)
        self.menu.console.print()
        
        # Colores con fondo
        self.menu.console.print("[bold cyan]Colores con Fondo:[/bold cyan]")
        bg_colors = [
            "[black on red] Rojo [/black on red]",
            "[black on green] Verde [/black on green]",
            "[black on yellow] Amarillo [/black on yellow]",
            "[white on blue] Azul [/white on blue]",
            "[white on magenta] Magenta [/white on magenta]",
            "[black on cyan] Cian [/black on cyan]"
        ]
        
        bg_line = ""
        for bg_color in bg_colors:
            bg_line += f"{bg_color} "
        
        self.menu.console.print(bg_line)
        self.menu.console.print()
        
        # Estilos de texto
        self.menu.console.print("[bold cyan]Estilos de Texto:[/bold cyan]")
        styles = [
            "[bold]Negrita[/bold]",
            "[italic]Cursiva[/italic]",
            "[underline]Subrayado[/underline]",
            "[strike]Tachado[/strike]",
            "[dim]Atenuado[/dim]",
            "[blink]Parpadeante[/blink]"
        ]
        
        style_line = ""
        for style in styles:
            style_line += f"{style} "
        
        self.menu.console.print(style_line)
        self.menu.console.print()
        
        # Colores extendidos (256 colores)
        self.menu.console.print("[bold cyan]Paleta de Colores Extendida (muestra):[/bold cyan]")
        
        # Crear una muestra de la paleta de 256 colores
        color_sample = ""
        for i in range(16):
            if i < 8:
                # Colores básicos
                color_sample += f"[color({i})]██[/color({i})]"
            else:
                # Colores brillantes
                color_sample += f"[color({i})]██[/color({i})]"
        
        self.menu.console.print(color_sample)
        
        # Segunda línea con más colores
        color_sample2 = ""
        for i in range(16, 32):
            color_sample2 += f"[color({i})]██[/color({i})]"
        
        self.menu.console.print(color_sample2)
        self.menu.console.print()
        
        # Gradiente de grises
        self.menu.console.print("[bold cyan]Gradiente de Grises:[/bold cyan]")
        gray_gradient = ""
        for i in range(232, 256, 2):  # Colores de gris en la paleta 256
            gray_gradient += f"[color({i})]██[/color({i})]"
        
        self.menu.console.print(gray_gradient)
        self.menu.console.print()
        
        # Mostrar códigos ANSI raw (para referencia)
        ansi_panel = Panel(
            "[bold]Códigos ANSI Raw:[/bold]\n"
            "\\033[91mRojo\\033[0m \\033[92mVerde\\033[0m \\033[93mAmarillo\\033[0m\n"
            "\\033[94mAzul\\033[0m \\033[95mMagenta\\033[0m \\033[96mCian\\033[0m\n\n"
            "[bold]Estilos:[/bold]\n"
            "\\033[1mNegrita\\033[0m \\033[4mSubrayado\\033[0m \\033[7mInvertido\\033[0m",
            title="📋 Referencia de Códigos",
            border_style="yellow"
        )
        self.menu.console.print(ansi_panel)
        self.menu.console.print()
        
        # Resultado de la prueba
        result_panel = Panel(
            "[green]✅ Si puedes ver todos los colores y estilos correctamente, "
            "tu terminal tiene excelente soporte para colores ANSI.[/green]\n\n"
            "[yellow]⚠️ Si algunos colores no se muestran o se ven incorrectos, "
            "tu terminal puede tener soporte limitado de colores.[/yellow]\n\n"
            "[blue]💡 Para mejor soporte de colores, usa Windows Terminal o un terminal moderno.[/blue]",
            title="🎯 Resultado de la Prueba",
            border_style="blue"
        )
        self.menu.console.print(result_panel)
    
    def _check_color_support(self) -> bool:
        """Verifica si el terminal soporta colores."""
        try:
            # Verificar variables de entorno comunes
            term = os.environ.get('TERM', '')
            colorterm = os.environ.get('COLORTERM', '')
            
            # Verificar si estamos en Windows Terminal
            wt_session = os.environ.get('WT_SESSION', '')
            
            # Verificar soporte básico
            if any([
                'color' in term.lower(),
                'xterm' in term.lower(),
                colorterm,
                wt_session,
                platform.system() == "Windows"  # Windows generalmente soporta colores
            ]):
                return True
            
            return False
        except Exception:
            return False
    
    def _diagnostic_encoding(self):
        """Diagnóstico completo de codificación."""
        self.menu.show_info("🔍 DIAGNÓSTICO COMPLETO DE CODIFICACIÓN")
        
        # Crear tabla para información del sistema
        table = Table(title="📋 Información del Sistema", box=box.DOUBLE)
        table.add_column("Propiedad", style="cyan", no_wrap=True)
        table.add_column("Valor", style="white")
        
        try:
            # Información básica de Python
            table.add_row("Python Encoding", sys.getdefaultencoding())
            table.add_row("File System Encoding", sys.getfilesystemencoding())
            table.add_row("Stdout Encoding", getattr(sys.stdout, 'encoding', 'No disponible'))
            table.add_row("Stderr Encoding", getattr(sys.stderr, 'encoding', 'No disponible'))
            
            # Información del sistema operativo
            table.add_row("Sistema Operativo", platform.system())
            table.add_row("Versión OS", platform.version())
            table.add_row("Arquitectura", platform.architecture()[0])
            
            # Variables de entorno relevantes
            locale_vars = ['LANG', 'LC_ALL', 'LC_CTYPE', 'PYTHONIOENCODING']
            for var in locale_vars:
                value = os.environ.get(var, 'No definido')
                table.add_row(f"Env: {var}", value)
            
            self.menu.console.print(table)
            self.menu.console.print()
            
            # Información específica de Windows
            if platform.system() == "Windows":
                self._show_windows_encoding_info()
            
            # Información específica de PowerShell
            self._show_powershell_encoding_info()
            
            # Prueba de escritura de caracteres
            self._test_character_writing()
            
            # Recomendaciones
            self._show_encoding_recommendations()
            
        except Exception as e:
            self.menu.show_error(f"Error en diagnóstico: {e}")
    
    def _show_windows_encoding_info(self):
        """Muestra información específica de Windows."""
        self.menu.console.print("[bold cyan]Información de Windows:[/bold cyan]")
        
        try:
            # Página de códigos actual
            result = subprocess.run(['chcp'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                codepage = result.stdout.strip()
                self.menu.console.print(f"📊 {codepage}")
            
            # Información del registro
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Console") as key:
                    try:
                        codepage_reg = winreg.QueryValueEx(key, "CodePage")[0]
                        self.menu.console.print(f"📋 Registro CodePage: {codepage_reg}")
                    except FileNotFoundError:
                        self.menu.console.print("📋 Registro CodePage: No configurado")
                    
                    try:
                        font_name = winreg.QueryValueEx(key, "FaceName")[0]
                        self.menu.console.print(f"🔤 Fuente del registro: {font_name}")
                    except FileNotFoundError:
                        self.menu.console.print("🔤 Fuente del registro: No configurada")
                        
            except ImportError:
                self.menu.console.print("⚠️ No se puede acceder al registro (winreg no disponible)")
            except Exception as e:
                self.menu.console.print(f"⚠️ Error accediendo al registro: {e}")
                
        except Exception as e:
            self.menu.console.print(f"❌ Error obteniendo información de Windows: {e}")
        
        self.menu.console.print()
    
    def _show_powershell_encoding_info(self):
        """Muestra información de codificación de PowerShell."""
        self.menu.console.print("[bold cyan]Información de PowerShell:[/bold cyan]")
        
        try:
            # OutputEncoding de PowerShell
            ps_commands = [
                "Write-Host 'OutputEncoding:' $OutputEncoding.EncodingName",
                "Write-Host 'Console OutputEncoding:' [Console]::OutputEncoding.EncodingName",
                "Write-Host 'Console InputEncoding:' [Console]::InputEncoding.EncodingName"
            ]
            
            for cmd in ps_commands:
                try:
                    result = subprocess.run(
                        ['powershell', '-Command', cmd],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if result.returncode == 0:
                        output = result.stdout.strip()
                        self.menu.console.print(f"🔧 {output}")
                    else:
                        self.menu.console.print(f"⚠️ Error ejecutando: {cmd}")
                except subprocess.TimeoutExpired:
                    self.menu.console.print(f"⏱️ Timeout ejecutando: {cmd}")
                except Exception as e:
                    self.menu.console.print(f"❌ Error: {e}")
                    
        except Exception as e:
            self.menu.console.print(f"❌ Error obteniendo información de PowerShell: {e}")
        
        self.menu.console.print()
    
    def _test_character_writing(self):
        """Prueba la escritura de caracteres especiales."""
        self.menu.console.print("[bold cyan]Prueba de Escritura de Caracteres:[/bold cyan]")
        
        test_chars = {
            "Español": "ñáéíóú",
            "Emojis": "🚀💻⚡",
            "Símbolos": "←→↑↓",
            "Matemáticos": "πΣΔ∞",
            "Caja": "┌─┐│└┘"
        }
        
        for category, chars in test_chars.items():
            try:
                # Intentar escribir y leer los caracteres
                encoded = chars.encode('utf-8')
                decoded = encoded.decode('utf-8')
                
                if chars == decoded:
                    status = "[green]✅[/green]"
                else:
                    status = "[red]❌[/red]"
                    
                self.menu.console.print(f"{status} {category}: {chars}")
                
            except Exception as e:
                self.menu.console.print(f"[red]❌[/red] {category}: Error - {e}")
        
        self.menu.console.print()
    
    def _show_encoding_recommendations(self):
        """Muestra recomendaciones basadas en el diagnóstico."""
        recommendations = []
        
        # Verificar página de códigos
        if platform.system() == "Windows":
            try:
                result = subprocess.run(['chcp'], capture_output=True, text=True, shell=True)
                if result.returncode == 0 and "65001" not in result.stdout:
                    recommendations.append(
                        "🔧 Ejecuta el módulo de configuración para establecer UTF-8 (65001)"
                    )
            except:
                pass
        
        # Verificar fuente
        try:
            if platform.system() == "Windows":
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Console") as key:
                    try:
                        font_name = winreg.QueryValueEx(key, "FaceName")[0]
                        if font_name not in ["Cascadia Code", "Consolas", "Courier New"]:
                            recommendations.append(
                                "🔤 Considera cambiar a una fuente compatible como Cascadia Code"
                            )
                    except FileNotFoundError:
                        recommendations.append(
                            "🔤 Configura una fuente compatible en el registro"
                        )
        except:
            pass
        
        # Verificar terminal
        if not os.environ.get('WT_SESSION'):
            recommendations.append(
                "💻 Para mejor soporte UTF-8, usa Windows Terminal"
            )
        
        # Mostrar recomendaciones
        if recommendations:
            rec_text = "\n".join(recommendations)
            rec_panel = Panel(
                rec_text,
                title="💡 Recomendaciones",
                border_style="yellow"
            )
            self.menu.console.print(rec_panel)
        else:
            success_panel = Panel(
                "[green]🎉 Tu configuración de codificación parece estar bien configurada![/green]",
                title="✅ Estado",
                border_style="green"
            )
            self.menu.console.print(success_panel)
        
        self.menu.console.print()
    
    def _show_encoding_info(self):
        """Muestra información básica de codificación."""
        self.menu.show_info("💻 INFORMACIÓN DE CODIFICACIÓN")
        
        # Crear tabla simple con información básica
        table = Table(title="📊 Configuración Actual", box=box.SIMPLE)
        table.add_column("Propiedad", style="cyan")
        table.add_column("Valor", style="white")
        
        # Información básica
        table.add_row("Sistema", platform.system())
        table.add_row("Python Encoding", sys.getdefaultencoding())
        
        if platform.system() == "Windows":
            try:
                result = subprocess.run(['chcp'], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    table.add_row("Página de Códigos", result.stdout.strip())
            except:
                table.add_row("Página de Códigos", "No disponible")
        
        # Variables de entorno importantes
        lang = os.environ.get('LANG', 'No definido')
        table.add_row("LANG", lang)
        
        wt_session = os.environ.get('WT_SESSION', 'No')
        table.add_row("Windows Terminal", "Sí" if wt_session else "No")
        
        self.menu.console.print(table)
        self.menu.console.print()
    
    def _run_full_test(self):
        """Ejecuta todas las pruebas de UTF-8."""
        self.menu.show_info("🎯 EJECUTANDO PRUEBA COMPLETA UTF-8")
        self.menu.console.print()
        
        # Ejecutar todas las pruebas en secuencia
        tests = [
            ("📝 Caracteres Básicos", self._test_basic_chars),
            ("📦 Símbolos de Caja", self._test_box_chars),
            ("🎨 Emojis y Símbolos", self._test_emojis),
            ("🌈 Colores ANSI", self._test_colors),
            ("🔍 Diagnóstico", self._diagnostic_encoding)
        ]
        
        for test_name, test_func in tests:
            self.menu.console.print(f"\n[bold blue]═══ {test_name} ═══[/bold blue]")
            try:
                test_func()
            except Exception as e:
                self.menu.show_error(f"Error en {test_name}: {e}")
            
            # Pausa entre pruebas para mejor legibilidad
            self.menu.console.print("\n" + "─" * 50)
        
        # Resumen final
        final_panel = Panel(
            "[bold green]🎉 Prueba completa finalizada![/bold green]\n\n"
            "Si todos los caracteres, símbolos y colores se muestran correctamente,\n"
            "tu configuración UTF-8 está funcionando perfectamente.\n\n"
            "Si hay problemas, revisa las recomendaciones del diagnóstico y\n"
            "considera ejecutar el módulo de configuración de consola.",
            title="🏁 Resumen Final",
            border_style="green"
        )
        self.menu.console.print(final_panel)


def main():
    """Función principal del módulo."""
    module = TestUtf8Module()
    module.main()


if __name__ == "__main__":
    main()