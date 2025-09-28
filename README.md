# NooxCLI 🚀

Una herramienta CLI moderna desarrollada en Python para gestión de desarrollo, sistema y proyectos. Migrado desde PowerShell con interfaz interactiva mejorada usando menús navegables con flechas.

## Características ✨

- **Interfaz Interactiva**: Menús navegables con flechas del teclado
- **Multi-plataforma**: Compatible con Windows y Linux
- **Diseño Modular**: Organizado en módulos especializados
- **UTF-8 Support**: Soporte completo para caracteres especiales
- **Tema Personalizable**: Colores y estilos configurables

## Módulos Disponibles 📋

- **Desarrollo**: Herramientas para entorno de desarrollo
- **Sistema**: Scripts y utilidades del sistema
- **Proyectos**: Gestión de proyectos Laragon
- **Configuración**: Configuración de consola y UTF-8
- **Ayuda**: Sistema de ayuda interactivo
- **Reparaciones**: Utilidades de reparación

## Instalación 🔧

### Desde el repositorio
```bash
git clone https://github.com/tu-usuario/noox-cli.git
cd noox-cli
pip install -r requirements.txt
pip install -e .
```

### Uso
```bash
noox
```

## Desarrollo 🛠️

### Estructura del proyecto
```
noox-cli/
├── src/
│   └── noox_cli/
│       ├── main.py          # Punto de entrada principal
│       ├── menu.py          # Sistema de menús
│       ├── utils/           # Utilidades compartidas
│       └── modules/         # Módulos individuales
│           ├── ayuda.py
│           ├── desarrollo.py
│           ├── sistema.py
│           ├── proyectos.py
│           ├── config.py
│           └── reparar.py
├── tests/                   # Pruebas unitarias
├── docs/                    # Documentación
└── requirements.txt         # Dependencias
```

## Licencia 📄

MIT License - Ver archivo LICENSE para detalles.
