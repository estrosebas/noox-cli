# Design Document

## Overview

Este documento describe el diseño para completar la migración de los módulos faltantes de NooxCLI. El diseño mantiene la consistencia con los módulos ya implementados (desarrollo.py y proyectos.py), utilizando el mismo patrón de arquitectura, estilo visual y funcionalidades.

Los módulos a implementar son:
- **sistema.py**: Herramientas de administración del sistema
- **reparar.py**: Reparación de perfil PowerShell  
- **test_utf8.py**: Pruebas de configuración UTF-8
- **config.py**: Configuración de consola UTF-8 (verificar completitud)

## Architecture

### Patrón de Diseño Consistente

Todos los módulos seguirán el mismo patrón arquitectónico establecido:

```python
class ModuleNameModule:
    def __init__(self):
        self.menu = NooxMenu("Module Name - NooxCLI")
        # Configuraciones específicas del módulo
        
    def main(self):
        """Función principal con menú interactivo"""
        while True:
            self.menu.show_banner()
            # Mostrar información contextual
            choices = [...]  # Opciones del menú
            selection = self.menu.show_menu(choices, "Pregunta del menú")
            if not selection or selection == 'exit':
                break
            self._handle_selection(selection)
    
    def _handle_selection(self, selection: str):
        """Dispatcher de funciones"""
        handlers = {...}
        if selection in handlers:
            try:
                handlers[selection]()
            except Exception as e:
                self.menu.show_error(f"Error: {e}")
            self.menu.pause()
```

### Componentes Compartidos

- **NooxMenu**: Framework de menús interactivos con Rich
- **Rich Components**: Tables, Panels, Progress bars, etc.
- **Error Handling**: Manejo consistente de errores y excepciones
- **Cross-platform**: Detección de OS para comandos específicos

## Components and Interfaces

### 1. Sistema Module (sistema.py)

#### Funcionalidades Principales:
- **Información del Sistema**: systeminfo, platform, psutil
- **Gestión de Procesos**: psutil para listar/terminar procesos
- **Monitoreo de Red**: netstat, psutil.net_connections()
- **Espacio en Disco**: shutil.disk_usage(), psutil.disk_partitions()
- **Servicios Windows**: subprocess con sc query
- **Variables de Entorno**: os.environ
- **Limpieza Temporal**: tempfile, shutil para limpiar cache
- **Herramientas Sistema**: taskmgr, regedit
- **Diagnóstico Red**: ipconfig, ping, nslookup

#### Estructura de Menú:
```python
choices = [
    {'name': '💻 Información del sistema', 'value': 'sysinfo'},
    {'name': '⚙️ Procesos en ejecución', 'value': 'processes'},
    {'name': '🌐 Uso de red', 'value': 'network'},
    {'name': '💾 Espacio en disco', 'value': 'disk'},
    {'name': '🔧 Servicios Windows', 'value': 'services'},
    {'name': '📋 Variables de entorno', 'value': 'env_vars'},
    {'name': '🧹 Limpiar temporales', 'value': 'cleanup'},
    {'name': '🛠️ Herramientas sistema', 'value': 'tools'},
    {'name': '🌍 Diagnóstico de red', 'value': 'network_diag'}
]
```

### 2. Reparar Module (reparar.py)

#### Funcionalidades Principales:
- **Backup Perfil**: Crear respaldo con timestamp
- **Generar Perfil**: Crear nuevo Microsoft.PowerShell_profile.ps1
- **Verificar Sintaxis**: Validar PowerShell syntax
- **Configurar UTF-8**: Encoding y CodePage
- **Aliases**: Configurar aliases útiles
- **Oh-My-Posh**: Configuración de tema

#### Estructura de Menú:
```python
choices = [
    {'name': '🔧 Reparar perfil completo', 'value': 'repair_full'},
    {'name': '💾 Solo crear backup', 'value': 'backup_only'},
    {'name': '📝 Regenerar perfil', 'value': 'regenerate'},
    {'name': '✅ Verificar sintaxis', 'value': 'verify'},
    {'name': '🎨 Configurar oh-my-posh', 'value': 'omp_config'},
    {'name': '📊 Ver perfil actual', 'value': 'show_current'}
]
```

### 3. Test UTF-8 Module (test_utf8.py)

#### Funcionalidades Principales:
- **Caracteres Especiales**: ñ, acentos, diéresis
- **Símbolos de Caja**: Box drawing characters
- **Emojis**: Unicode emojis y símbolos
- **Matemáticos**: Símbolos matemáticos y griegos
- **Monedas**: Símbolos de moneda internacional
- **Programación**: Caracteres especiales de código
- **Colores**: Test de códigos ANSI
- **Diagnóstico**: Información de codificación

#### Estructura de Menú:
```python
choices = [
    {'name': '🎯 Test completo UTF-8', 'value': 'full_test'},
    {'name': '📝 Solo caracteres básicos', 'value': 'basic_chars'},
    {'name': '📦 Símbolos de caja', 'value': 'box_chars'},
    {'name': '🎨 Emojis y símbolos', 'value': 'emojis'},
    {'name': '🌈 Test de colores', 'value': 'colors'},
    {'name': '🔍 Diagnóstico completo', 'value': 'diagnostic'},
    {'name': '💻 Info codificación', 'value': 'encoding_info'}
]
```

### 4. Config Module (config.py)

Verificar si ya está completo o necesita implementación adicional basada en config-consola.bat.

## Data Models

### SystemInfo
```python
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
```

### ProcessInfo
```python
@dataclass
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    status: str
    create_time: datetime
```

### DiskInfo
```python
@dataclass
class DiskInfo:
    device: str
    mountpoint: str
    fstype: str
    total: int
    used: int
    free: int
    percent: float
```

### NetworkConnection
```python
@dataclass
class NetworkConnection:
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    status: str
    protocol: str
```

## Error Handling

### Estrategia Consistente
- **Try-Catch Blocks**: Envolver operaciones críticas
- **User-Friendly Messages**: Mensajes claros para el usuario
- **Fallback Methods**: Métodos alternativos cuando falle el principal
- **Permission Handling**: Detectar y manejar permisos insuficientes

### Ejemplos de Manejo:
```python
def _get_system_info(self):
    try:
        # Método principal con systeminfo
        result = subprocess.run(['systeminfo'], capture_output=True, text=True, check=True)
        return self._parse_systeminfo(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback con platform y psutil
        return self._get_system_info_fallback()
    except Exception as e:
        self.menu.show_error(f"Error obteniendo información del sistema: {e}")
        return None
```

## Testing Strategy

### Pruebas por Módulo

#### Sistema Module:
- Test de información del sistema en diferentes OS
- Test de listado de procesos
- Test de información de red
- Test de espacio en disco
- Test de limpieza de temporales

#### Reparar Module:
- Test de creación de backup
- Test de generación de perfil
- Test de verificación de sintaxis
- Test de configuración UTF-8

#### Test UTF-8 Module:
- Test de renderizado de caracteres especiales
- Test de detección de problemas de codificación
- Test de diagnóstico de configuración

### Estrategia de Testing:
1. **Unit Tests**: Funciones individuales
2. **Integration Tests**: Interacción con sistema operativo
3. **Manual Tests**: Verificación visual de caracteres UTF-8
4. **Cross-platform Tests**: Windows, Linux, macOS

## Visual Design Consistency

### Colores y Estilos (siguiendo desarrollo.py y proyectos.py):
- **Success**: `[green]✅[/green]`
- **Error**: `[red]❌[/red]`
- **Warning**: `[yellow]⚠️[/yellow]`
- **Info**: `[cyan]ℹ️[/cyan]`
- **Progress**: `[blue]🔄[/blue]`

### Iconos Consistentes:
- 💻 Sistema/Computadora
- ⚙️ Configuración/Procesos
- 🌐 Red/Internet
- 💾 Almacenamiento/Disco
- 🔧 Herramientas/Reparación
- 📊 Información/Estadísticas
- 🧹 Limpieza
- 🎯 Test/Prueba
- 📝 Archivos/Texto

### Tablas Rich:
```python
table = Table(title="📊 Título", box=box.DOUBLE)
table.add_column("Columna", style="cyan", no_wrap=True)
table.add_column("Valor", style="white")
```

## Platform Compatibility

### Windows Specific:
- Registry operations (winreg)
- Windows services (sc command)
- PowerShell profile paths
- CMD/PowerShell detection

### Cross-platform:
- psutil para información del sistema
- pathlib para rutas
- subprocess para comandos
- platform para detección de OS

### Fallback Strategies:
- Si falla comando Windows → usar psutil
- Si no hay permisos admin → mostrar alternativas
- Si falta herramienta → sugerir instalación

## Security Considerations

### Permisos Administrativos:
- Detectar cuando se requieren permisos elevados
- Informar claramente al usuario
- Proporcionar alternativas sin permisos admin

### Operaciones Seguras:
- Validar rutas antes de operaciones de archivo
- Sanitizar inputs de usuario
- Backup antes de modificaciones críticas
- Verificar sintaxis antes de aplicar cambios

### Registry Operations:
- Solo modificar claves de usuario (HKCU)
- Crear backup de valores antes de cambiar
- Validar valores antes de escribir