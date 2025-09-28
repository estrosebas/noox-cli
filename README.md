# NooxCLI 🚀

> **Una herramienta CLI moderna desarrollada en Python para gestión de desarrollo, sistema y proyectos**

Migrado desde PowerShell con interfaz interactiva mejorada usando menús navegables con flechas. NooxCLI combina la potencia de los scripts de automatización con una experiencia de usuario moderna y intuitiva.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ✨ Características

- 🎯 **Interfaz Interactiva**: Menús navegables con flechas del teclado usando InquirerPy
- 🌍 **Multi-plataforma**: Compatible con Windows, Linux y macOS
- 🔧 **Diseño Modular**: Organizado en módulos especializados para fácil mantenimiento
- 🌐 **UTF-8 Completo**: Soporte total para caracteres especiales y emojis
- 🎨 **Diseño Moderno**: Colores y estilos atractivos usando Rich
- ⚡ **Rendimiento**: Rápido y eficiente, construido en Python moderno
- 📱 **Portabilidad**: Scripts originales .bat preservados para compatibilidad

## 📋 Módulos Disponibles

| Módulo | Estado | Descripción |
|--------|--------|--------------|
| 🛠️ **Desarrollo** | 🚧 | Herramientas para entorno de desarrollo (Git, NPM, Python, VS Code) |
| ⚙️ **Sistema** | 🚧 | Scripts y utilidades del sistema (procesos, red, limpieza) |
| 📁 **Proyectos** | 🚧 | Gestión de proyectos Laragon (crear, clonar, deploy) |
| 🔧 **Configuración** | ✅ | Configuración de consola y UTF-8 (completo) |
| ❓ **Ayuda** | ✅ | Sistema de ayuda interactivo (completo) |
| 🔨 **Reparación** | 🚧 | Utilidades de reparación de perfil |
| 🧪 **Test UTF-8** | 🚧 | Pruebas de codificación y caracteres especiales |

## 🚀 Instalación Rápida

### Método 1: Script Automático (Recomendado)

**Windows:**
```cmd
git clone https://github.com/tu-usuario/noox-cli.git
cd noox-cli
install.bat
```

**Linux/macOS:**
```bash
git clone https://github.com/tu-usuario/noox-cli.git
cd noox-cli
chmod +x install.sh
./install.sh
```

### Método 2: Instalación Manual

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/noox-cli.git
cd noox-cli

# Instalar dependencias
pip install -r requirements.txt

# Instalar en modo desarrollo
pip install -e .
```

## 🎮 Uso

### Ejecutar NooxCLI
```bash
# Método principal (recomendado)
python -m noox_cli.main

# Si el comando noox está en PATH
noox
```

### Navegación
- **↑↓**: Navegar por el menú
- **Enter**: Seleccionar opción
- **Ctrl+C**: Salir en cualquier momento

### Ejemplos de Uso

1. **Configurar UTF-8 completo:**
   - Ejecuta NooxCLI → Configuración → Configuración Completa

2. **Ver ayuda de módulos:**
   - Ejecuta NooxCLI → Ayuda → Selecciona el módulo

3. **Probar caracteres UTF-8:**
   - Ejecuta NooxCLI → Configuración → Probar UTF-8

## 🛠️ Desarrollo

### Estructura del Proyecto

```
noox-cli/
├── 📁 src/noox_cli/           # Código fuente principal
│   ├── main.py                # Punto de entrada
│   ├── menu.py                # Sistema de menús base
│   ├── 📁 modules/            # Módulos funcionales
│   │   ├── ayuda.py          # ✅ Sistema de ayuda
│   │   ├── config.py         # ✅ Configuración UTF-8
│   │   ├── desarrollo.py     # 🚧 Herramientas dev
│   │   ├── sistema.py        # 🚧 Utilidades sistema
│   │   ├── proyectos.py      # 🚧 Gestión proyectos
│   │   ├── reparar.py        # 🚧 Reparaciones
│   │   └── test_utf8.py      # 🚧 Tests UTF-8
│   └── 📁 utils/             # Utilidades compartidas
├── 📁 tests/                 # Pruebas unitarias (futuro)
├── 📁 docs/                  # Documentación (futuro)
├── *.bat                     # Scripts originales preservados
├── requirements.txt          # Dependencias Python
├── setup.py                 # Configuración del paquete
└── install.{bat,sh}         # Scripts de instalación
```

### Tecnologías Utilizadas

- **[InquirerPy](https://github.com/kazhala/InquirerPy)**: Menús interactivos elegantes
- **[Rich](https://github.com/Textualize/rich)**: Formateo y colores de terminal
- **[Colorama](https://github.com/tartley/colorama)**: Compatibilidad de colores en Windows
- **[psutil](https://github.com/giampaolo/psutil)**: Información del sistema
- **[windows-curses](https://github.com/zephyrproject-rtos/windows-curses)**: Soporte curses en Windows

### Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 🔄 Migración desde PowerShell

**Estado actual de migración:**
- ✅ **Estructura base**: Completa
- ✅ **Sistema de menús**: Completo
- ✅ **Módulo Ayuda**: 100% migrado
- ✅ **Módulo Configuración**: 100% migrado
- 🚧 **Otros módulos**: En progreso

**Scripts originales preservados en la raíz del proyecto para referencia.**

## 🐛 Resolución de Problemas

### Problemas Comunes

**Error: ModuleNotFoundError**
```bash
# Asegúrate de instalar en modo desarrollo
pip install -e .
```

**Problemas de codificación UTF-8**
```bash
# Ejecuta el módulo de configuración
python -m noox_cli.main
# Luego: Configuración → Configuración Completa
```

**Comando 'noox' no encontrado**
```bash
# Usa el método alternativo
python -m noox_cli.main
```

## 📋 TODO / Roadmap

- [ ] 🛠️ Completar migración módulo Desarrollo
- [ ] ⚙️ Completar migración módulo Sistema  
- [ ] 📁 Completar migración módulo Proyectos
- [ ] 🔨 Completar migración módulo Reparación
- [ ] 🧪 Completar migración módulo Test UTF-8
- [ ] 🧪 Agregar pruebas unitarias
- [ ] 📚 Documentación completa
- [ ] 🐳 Soporte Docker
- [ ] 📦 Distribución en PyPI
- [ ] 🌍 Internacionalización (i18n)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🤝 Contribuidores

- **Sebastian** - *Desarrollo inicial y migración* - [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Gracias a la comunidad de Python por las excelentes librerías
- Inspirado en herramientas CLI modernas como `click` y `typer`
- Diseño basado en mejores prácticas de UX para terminales

---

**¿Encuentras útil NooxCLI? ¡Dale una ⭐ al repositorio!**
