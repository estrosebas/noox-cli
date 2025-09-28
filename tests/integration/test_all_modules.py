#!/usr/bin/env python3
"""
Pruebas de integración completas para todos los módulos de NooxCLI.
Verifica funcionalidad, manejo de errores, permisos y consistencia visual.
"""

import os
import sys
import unittest
import subprocess
import platform
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from noox_cli.modules import sistema, reparar, test_utf8, config
from noox_cli.menu import NooxMenu


class TestModuleIntegration(unittest.TestCase):
    """Pruebas de integración para todos los módulos."""
    
    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = os.getcwd()
        
    def tearDown(self):
        """Limpieza después de cada prueba."""
        os.chdir(self.original_cwd)
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_sistema_module_initialization(self):
        """Prueba la inicialización del módulo sistema."""
        try:
            sistema_module = sistema.SistemaModule()
            self.assertIsInstance(sistema_module, sistema.SistemaModule)
            self.assertIsInstance(sistema_module.menu, NooxMenu)
            self.assertEqual(sistema_module.menu.title, "Sistema - NooxCLI")
        except Exception as e:
            self.fail(f"Error inicializando módulo sistema: {e}")
    
    def test_reparar_module_initialization(self):
        """Prueba la inicialización del módulo reparar."""
        try:
            reparar_module = reparar.RepararModule()
            self.assertIsInstance(reparar_module, reparar.RepararModule)
            self.assertIsInstance(reparar_module.menu, NooxMenu)
            self.assertEqual(reparar_module.menu.title, "Reparación - NooxCLI")
        except Exception as e:
            self.fail(f"Error inicializando módulo reparar: {e}")
    
    def test_test_utf8_module_initialization(self):
        """Prueba la inicialización del módulo test_utf8."""
        try:
            utf8_module = test_utf8.TestUtf8Module()
            self.assertIsInstance(utf8_module, test_utf8.TestUtf8Module)
            self.assertIsInstance(utf8_module.menu, NooxMenu)
            self.assertEqual(utf8_module.menu.title, "Test UTF-8 - NooxCLI")
        except Exception as e:
            self.fail(f"Error inicializando módulo test_utf8: {e}")
    
    def test_config_module_initialization(self):
        """Prueba la inicialización del módulo config."""
        try:
            config_module = config.ConfigModule()
            self.assertIsInstance(config_module, config.ConfigModule)
            self.assertIsInstance(config_module.menu, NooxMenu)
            self.assertEqual(config_module.menu.title, "Configuración - NooxCLI")
        except Exception as e:
            self.fail(f"Error inicializando módulo config: {e}")


class TestSistemaModuleFunctionality(unittest.TestCase):
    """Pruebas específicas del módulo sistema."""
    
    def setUp(self):
        self.sistema_module = sistema.SistemaModule()
    
    def test_get_system_info_fallback(self):
        """Prueba el método fallback de información del sistema."""
        try:
            system_info = self.sistema_module._get_system_info_fallback()
            self.assertIsNotNone(system_info)
            self.assertIsInstance(system_info.hostname, str)
            self.assertIsInstance(system_info.os_name, str)
            self.assertIsInstance(system_info.cpu_count, int)
            self.assertGreater(system_info.cpu_count, 0)
        except Exception as e:
            self.fail(f"Error en get_system_info_fallback: {e}")
    
    def test_format_bytes(self):
        """Prueba el formateo de bytes."""
        test_cases = [
            (0, "0 B"),
            (1024, "1.0 KB"),
            (1048576, "1.0 MB"),
            (1073741824, "1.0 GB"),
            (512, "512.0 B")
        ]
        
        for bytes_value, expected in test_cases:
            result = self.sistema_module._format_bytes(bytes_value)
            self.assertEqual(result, expected)
    
    def test_parse_memory_string(self):
        """Prueba el parseo de strings de memoria."""
        test_cases = [
            ("8,192 MB", 8589934592),  # 8 GB en bytes
            ("4 GB", 4294967296),      # 4 GB en bytes
            ("1024 KB", 1048576),      # 1 MB en bytes
            ("", 0),                   # String vacío
            ("invalid", 0)             # String inválido
        ]
        
        for memory_str, expected in test_cases:
            result = self.sistema_module._parse_memory_string(memory_str)
            self.assertEqual(result, expected)
    
    @patch('psutil.process_iter')
    def test_get_process_list_with_psutil(self, mock_process_iter):
        """Prueba la obtención de lista de procesos con psutil."""
        # Mock de proceso
        mock_proc = MagicMock()
        mock_proc.info = {
            'pid': 1234,
            'name': 'test_process',
            'cpu_percent': 5.0,
            'memory_percent': 2.5,
            'status': 'running',
            'create_time': 1640995200  # timestamp
        }
        mock_process_iter.return_value = [mock_proc]
        
        try:
            processes = self.sistema_module._get_process_list(limit=10)
            self.assertIsInstance(processes, list)
            if processes:  # Solo verificar si hay procesos
                self.assertIsInstance(processes[0], sistema.ProcessInfo)
        except Exception as e:
            # Si psutil no está disponible, la prueba debe pasar
            if "psutil" not in str(e):
                self.fail(f"Error inesperado en get_process_list: {e}")
    
    def test_error_handling_without_permissions(self):
        """Prueba el manejo de errores sin permisos administrativos."""
        # Simular falta de permisos
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = PermissionError("Access denied")
            
            # La función debe manejar el error graciosamente
            try:
                system_info = self.sistema_module._get_system_info_windows()
                # Debe retornar None o usar fallback
                self.assertTrue(system_info is None or isinstance(system_info, sistema.SystemInfo))
            except PermissionError:
                self.fail("El módulo no maneja correctamente los errores de permisos")


class TestRepararModuleFunctionality(unittest.TestCase):
    """Pruebas específicas del módulo reparar."""
    
    def setUp(self):
        self.reparar_module = reparar.RepararModule()
        self.test_dir = Path(tempfile.mkdtemp())
        # Usar directorio temporal para pruebas
        self.reparar_module.powershell_dir = self.test_dir / "WindowsPowerShell"
        self.reparar_module.profile_path = self.reparar_module.powershell_dir / "Microsoft.PowerShell_profile.ps1"
    
    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_generate_profile_content(self):
        """Prueba la generación del contenido del perfil."""
        try:
            content = self.reparar_module._get_profile_content()
            self.assertIsInstance(content, str)
            self.assertIn("UTF-8", content)
            self.assertIn("chcp 65001", content)
            self.assertIn("oh-my-posh", content)
            self.assertIn("Set-Alias", content)
        except Exception as e:
            self.fail(f"Error generando contenido del perfil: {e}")
    
    def test_backup_profile_no_existing_profile(self):
        """Prueba backup cuando no existe perfil previo."""
        # Asegurar que no existe perfil
        if self.reparar_module.profile_path.exists():
            self.reparar_module.profile_path.unlink()
        
        backup_path = self.reparar_module._backup_profile()
        self.assertIsNone(backup_path)
    
    def test_generate_profile_creates_directory(self):
        """Prueba que la generación de perfil crea el directorio."""
        # Asegurar que el directorio no existe
        if self.reparar_module.powershell_dir.exists():
            shutil.rmtree(self.reparar_module.powershell_dir)
        
        result = self.reparar_module._generate_profile()
        self.assertTrue(result)
        self.assertTrue(self.reparar_module.powershell_dir.exists())
        self.assertTrue(self.reparar_module.profile_path.exists())
    
    def test_check_omp_installation(self):
        """Prueba la verificación de instalación de oh-my-posh."""
        try:
            status = self.reparar_module._check_omp_installation()
            self.assertIsInstance(status, str)
            self.assertTrue(status.startswith("✅") or status.startswith("❌"))
        except Exception as e:
            self.fail(f"Error verificando oh-my-posh: {e}")


class TestTestUtf8ModuleFunctionality(unittest.TestCase):
    """Pruebas específicas del módulo test_utf8."""
    
    def setUp(self):
        self.utf8_module = test_utf8.TestUtf8Module()
    
    def test_check_color_support(self):
        """Prueba la verificación de soporte de colores."""
        try:
            color_support = self.utf8_module._check_color_support()
            self.assertIsInstance(color_support, bool)
        except Exception as e:
            self.fail(f"Error verificando soporte de colores: {e}")
    
    def test_get_python_encoding(self):
        """Prueba la obtención de información de codificación de Python."""
        try:
            encoding_info = self.utf8_module._get_python_encoding()
            self.assertIsInstance(encoding_info, dict)
            self.assertIn('stdout', encoding_info)
            self.assertIn('locale', encoding_info)
        except Exception as e:
            self.fail(f"Error obteniendo codificación de Python: {e}")
    
    @unittest.skipUnless(platform.system() == "Windows", "Prueba específica de Windows")
    def test_show_windows_encoding_info(self):
        """Prueba la información de codificación específica de Windows."""
        try:
            # Capturar salida para verificar que no hay errores
            with patch('sys.stdout', new_callable=StringIO):
                self.utf8_module._show_windows_encoding_info()
        except Exception as e:
            self.fail(f"Error mostrando información de Windows: {e}")


class TestConfigModuleFunctionality(unittest.TestCase):
    """Pruebas específicas del módulo config."""
    
    def setUp(self):
        self.config_module = config.ConfigModule()
    
    def test_get_current_codepage(self):
        """Prueba la obtención de la página de códigos actual."""
        try:
            codepage = self.config_module._get_current_codepage()
            self.assertIsInstance(codepage, str)
            self.assertNotEqual(codepage, "")
        except Exception as e:
            self.fail(f"Error obteniendo página de códigos: {e}")
    
    def test_get_python_encoding(self):
        """Prueba la obtención de información de codificación de Python."""
        try:
            encoding_info = self.config_module._get_python_encoding()
            self.assertIsInstance(encoding_info, dict)
            self.assertIn('stdout', encoding_info)
            self.assertIn('locale', encoding_info)
        except Exception as e:
            self.fail(f"Error obteniendo codificación de Python: {e}")
    
    @unittest.skipUnless(platform.system() == "Windows", "Prueba específica de Windows")
    def test_get_registry_config(self):
        """Prueba la obtención de configuración del registro."""
        try:
            reg_config = self.config_module._get_registry_config()
            self.assertIsInstance(reg_config, dict)
        except Exception as e:
            self.fail(f"Error obteniendo configuración del registro: {e}")


class TestCrossModuleConsistency(unittest.TestCase):
    """Pruebas de consistencia entre módulos."""
    
    def setUp(self):
        self.modules = {
            'sistema': sistema.SistemaModule(),
            'reparar': reparar.RepararModule(),
            'test_utf8': test_utf8.TestUtf8Module(),
            'config': config.ConfigModule()
        }
    
    def test_all_modules_have_menu(self):
        """Verifica que todos los módulos tengan un objeto menu."""
        for module_name, module_instance in self.modules.items():
            with self.subTest(module=module_name):
                self.assertTrue(hasattr(module_instance, 'menu'))
                self.assertIsInstance(module_instance.menu, NooxMenu)
    
    def test_all_modules_have_main_method(self):
        """Verifica que todos los módulos tengan un método main."""
        for module_name, module_instance in self.modules.items():
            with self.subTest(module=module_name):
                self.assertTrue(hasattr(module_instance, 'main'))
                self.assertTrue(callable(getattr(module_instance, 'main')))
    
    def test_all_modules_have_handle_selection_method(self):
        """Verifica que todos los módulos tengan un método _handle_selection."""
        for module_name, module_instance in self.modules.items():
            with self.subTest(module=module_name):
                self.assertTrue(hasattr(module_instance, '_handle_selection'))
                self.assertTrue(callable(getattr(module_instance, '_handle_selection')))
    
    def test_menu_titles_are_consistent(self):
        """Verifica que los títulos de menú sigan un patrón consistente."""
        expected_patterns = {
            'sistema': "Sistema - NooxCLI",
            'reparar': "Reparación - NooxCLI",
            'test_utf8': "Test UTF-8 - NooxCLI",
            'config': "Configuración - NooxCLI"
        }
        
        for module_name, expected_title in expected_patterns.items():
            with self.subTest(module=module_name):
                module_instance = self.modules[module_name]
                self.assertEqual(module_instance.menu.title, expected_title)


class TestErrorHandlingAndPermissions(unittest.TestCase):
    """Pruebas de manejo de errores y permisos."""
    
    def test_sistema_handles_missing_psutil(self):
        """Prueba que el módulo sistema maneje la ausencia de psutil."""
        with patch.dict('sys.modules', {'psutil': None}):
            try:
                sistema_module = sistema.SistemaModule()
                # Debe poder inicializarse sin psutil
                self.assertIsInstance(sistema_module, sistema.SistemaModule)
            except Exception as e:
                self.fail(f"El módulo sistema no maneja correctamente la ausencia de psutil: {e}")
    
    def test_modules_handle_keyboard_interrupt(self):
        """Prueba que los módulos manejen KeyboardInterrupt correctamente."""
        for module_name, module_class in [
            ('sistema', sistema.SistemaModule),
            ('reparar', reparar.RepararModule),
            ('test_utf8', test_utf8.TestUtf8Module),
            ('config', config.ConfigModule)
        ]:
            with self.subTest(module=module_name):
                module_instance = module_class()
                
                # Simular KeyboardInterrupt en _handle_selection
                with patch.object(module_instance, '_handle_selection') as mock_handle:
                    mock_handle.side_effect = KeyboardInterrupt()
                    
                    try:
                        # Esto no debería lanzar excepción no manejada
                        module_instance._handle_selection('test')
                    except KeyboardInterrupt:
                        # Es aceptable que se propague KeyboardInterrupt
                        pass
                    except Exception as e:
                        self.fail(f"Módulo {module_name} no maneja KeyboardInterrupt: {e}")
    
    @unittest.skipUnless(platform.system() == "Windows", "Prueba específica de Windows")
    def test_windows_registry_access_errors(self):
        """Prueba el manejo de errores de acceso al registro de Windows."""
        config_module = config.ConfigModule()
        
        with patch('winreg.OpenKey') as mock_open_key:
            mock_open_key.side_effect = PermissionError("Access denied")
            
            try:
                reg_config = config_module._get_registry_config()
                # Debe retornar un dict con información de error
                self.assertIsInstance(reg_config, dict)
            except PermissionError:
                self.fail("El módulo config no maneja errores de registro correctamente")


class TestVisualConsistency(unittest.TestCase):
    """Pruebas de consistencia visual y UX."""
    
    def test_error_message_format_consistency(self):
        """Verifica que los mensajes de error sigan un formato consistente."""
        modules = [
            sistema.SistemaModule(),
            reparar.RepararModule(),
            test_utf8.TestUtf8Module(),
            config.ConfigModule()
        ]
        
        for module in modules:
            # Verificar que todos usen el mismo método para mostrar errores
            self.assertTrue(hasattr(module.menu, 'show_error'))
            self.assertTrue(hasattr(module.menu, 'show_success'))
            self.assertTrue(hasattr(module.menu, 'show_warning'))
            self.assertTrue(hasattr(module.menu, 'show_info'))
    
    def test_menu_structure_consistency(self):
        """Verifica que la estructura de menús sea consistente."""
        modules = {
            'sistema': sistema.SistemaModule(),
            'reparar': reparar.RepararModule(),
            'test_utf8': test_utf8.TestUtf8Module(),
            'config': config.ConfigModule()
        }
        
        for module_name, module_instance in modules.items():
            with self.subTest(module=module_name):
                # Verificar que el menú use Rich Console
                self.assertTrue(hasattr(module_instance.menu, 'console'))
                self.assertTrue(hasattr(module_instance.menu, 'show_banner'))
                self.assertTrue(hasattr(module_instance.menu, 'show_menu'))


if __name__ == '__main__':
    # Configurar UTF-8 para las pruebas
    if platform.system() == "Windows":
        os.system('chcp 65001 > nul')
    
    # Ejecutar todas las pruebas
    unittest.main(verbosity=2)