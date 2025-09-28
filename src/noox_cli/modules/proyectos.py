"""
Módulo de Proyectos - NooxCLI
Migrado desde proyectos.bat con interfaz interactiva mejorada
Gestión de proyectos web, creación, clonado, backup y deploy
"""

import os
import sys
import subprocess
import shutil
import webbrowser
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..menu import NooxMenu
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.columns import Columns
from rich import box


class ProyectosModule:
    """Módulo de gestión de proyectos web y desarrollo."""
    
    def __init__(self):
        self.menu = NooxMenu("Proyectos - NooxCLI")
        # Directorios configurables
        self.laragon_path = Path("C:/laragonzo/www")
        self.projects_path = self.laragon_path if self.laragon_path.exists() else Path.cwd()
        
    def main(self):
        """Función principal del módulo de proyectos."""
        while True:
            self.menu.show_banner()
            
            # Mostrar directorio de proyectos actual
            self.menu.show_info(f"📁 Directorio de proyectos: {self.projects_path}")
            
            # Verificar y mostrar proyectos disponibles
            if self.projects_path.exists():
                projects = self._get_projects()
                if projects:
                    self.menu.show_info(f"📂 Proyectos encontrados: {len(projects)}")
                else:
                    self.menu.show_warning("⚠️ No hay proyectos en el directorio")
            else:
                self.menu.show_error(f"❌ Directorio no encontrado: {self.projects_path}")
            
            self.menu.console.print()
            
            # Menú principal de proyectos
            choices = [
                {
                    'name': '📂 Ver proyectos',
                    'value': 'list_projects',
                    'description': 'Listar y abrir proyectos existentes'
                },
                {
                    'name': '➕ Crear proyecto nuevo',
                    'value': 'new_project',
                    'description': 'Crear nuevo proyecto con plantilla'
                },
                {
                    'name': '🔄 Clonar repositorio',
                    'value': 'clone_repo',
                    'description': 'Clonar proyecto desde Git'
                },
                {
                    'name': '📁 Abrir directorio',
                    'value': 'open_folder',
                    'description': 'Abrir carpeta de proyectos'
                },
                {
                    'name': '📦 Backup y compresión',
                    'value': 'backup',
                    'description': 'Crear backups de proyectos'
                },
                {
                    'name': '🚀 Deploy y testing',
                    'value': 'deploy',
                    'description': 'Despliegue y pruebas'
                },
                {
                    'name': '🐳 Docker operations',
                    'value': 'docker',
                    'description': 'Operaciones con Docker'
                },
                {
                    'name': '⚙️ Configuración',
                    'value': 'config',
                    'description': 'Configurar directorios y opciones'
                }
            ]
            
            selection = self.menu.show_menu(choices, "📁 ¿Qué quieres hacer con tus proyectos?")
            
            if not selection or selection == 'exit':
                break
            
            self._handle_selection(selection)
    
    def _handle_selection(self, selection: str):
        """Maneja la selección del usuario."""
        handlers = {
            'list_projects': self._list_projects,
            'new_project': self._new_project,
            'clone_repo': self._clone_repo,
            'open_folder': self._open_folder,
            'backup': self._backup_menu,
            'deploy': self._deploy_menu,
            'docker': self._docker_menu,
            'config': self._config_menu
        }
        
        if selection in handlers:
            try:
                handlers[selection]()
            except Exception as e:
                self.menu.show_error(f"Error ejecutando {selection}: {e}")
            self.menu.pause()
    
    def _get_projects(self) -> List[Path]:
        """Obtiene lista de proyectos en el directorio."""
        if not self.projects_path.exists():
            return []
        
        projects = []
        for item in self.projects_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                projects.append(item)
        
        return sorted(projects, key=lambda x: x.name.lower())
    
    def _list_projects(self):
        """Lista y permite abrir proyectos existentes."""
        self.menu.clear_screen()
        
        projects = self._get_projects()
        
        if not projects:
            self.menu.show_warning("⚠️ No hay proyectos en el directorio")
            if self.menu.show_confirmation("¿Quieres crear un nuevo proyecto?"):
                self._new_project()
            return
        
        # Crear opciones para el menú
        project_choices = []
        for i, project in enumerate(projects, 1):
            # Detectar tipo de proyecto
            project_type = self._detect_project_type(project)
            project_choices.append({
                'name': f'🚀 {project.name}',
                'value': str(project),
                'description': f'Tipo: {project_type}'
            })
        
        selection = self.menu.show_menu(project_choices, "📂 Selecciona un proyecto:")
        
        if selection and selection != 'exit':
            self._open_project(Path(selection))
    
    def _detect_project_type(self, project_path: Path) -> str:
        """Detecta el tipo de proyecto basado en archivos existentes."""
        if (project_path / 'package.json').exists():
            return 'Node.js/React'
        elif (project_path / 'requirements.txt').exists():
            return 'Python'
        elif (project_path / 'composer.json').exists():
            return 'PHP/Laravel'
        elif (project_path / 'index.html').exists():
            return 'HTML/Web'
        elif (project_path / 'index.php').exists():
            return 'PHP'
        elif (project_path / '.git').exists():
            return 'Git Repository'
        else:
            return 'Desconocido'
    
    def _open_project(self, project_path: Path):
        """Abre un proyecto con diferentes opciones."""
        self.menu.clear_screen()
        
        self.menu.show_info(f"🚀 Proyecto: {project_path.name}")
        self.menu.show_info(f"📁 Ruta: {project_path}")
        self.menu.show_info(f"🏷️ Tipo: {self._detect_project_type(project_path)}")
        
        actions = [
            {'name': '💻 Abrir en VS Code', 'value': 'vscode'},
            {'name': '⚡ Abrir terminal aquí', 'value': 'terminal'},
            {'name': '🌐 Abrir en navegador', 'value': 'browser'},
            {'name': '📁 Explorar carpeta', 'value': 'explorer'},
            {'name': '📊 Ver información', 'value': 'info'},
            {'name': '⚙️ Ejecutar servidor', 'value': 'server'}
        ]
        
        selection = self.menu.show_menu(actions, "⚙️ ¿Qué quieres hacer?")
        
        if not selection or selection == 'exit':
            return
        
        try:
            if selection == 'vscode':
                if self._open_vscode(project_path):
                    self.menu.show_success("✅ VS Code abierto")
                else:
                    self.menu.show_error("❌ VS Code no está instalado o no se pudo abrir")
                    self.menu.show_info("💡 Instala VS Code desde: https://code.visualstudio.com/")
            
            elif selection == 'terminal':
                if self._open_terminal(project_path):
                    self.menu.show_success("✅ Terminal abierto")
                else:
                    self.menu.show_error("❌ No se pudo abrir el terminal")
            
            elif selection == 'browser':
                # Intentar abrir en localhost
                project_name = project_path.name
                urls = [
                    f"http://localhost/{project_name}",
                    f"http://localhost:3000",
                    f"http://localhost:8000"
                ]
                for url in urls:
                    webbrowser.open(url)
                    self.menu.show_info(f"🌐 Abriendo: {url}")
            
            elif selection == 'explorer':
                if os.name == 'nt':
                    subprocess.run(['explorer', str(project_path)])
                else:
                    subprocess.run(['xdg-open', str(project_path)])
                self.menu.show_success("✅ Explorador abierto")
            
            elif selection == 'info':
                self._show_project_info(project_path)
            
            elif selection == 'server':
                self._run_project_server(project_path)
                
        except Exception as e:
            self.menu.show_error(f"Error ejecutando acción: {e}")
    
    def _show_project_info(self, project_path: Path):
        """Muestra información detallada del proyecto."""
        self.menu.clear_screen()
        
        info_table = Table(title=f"📊 Información: {project_path.name}", box=box.DOUBLE)
        info_table.add_column("Propiedad", style="cyan", no_wrap=True)
        info_table.add_column("Valor", style="white")
        
        # Información básica
        info_table.add_row("📁 Nombre", project_path.name)
        info_table.add_row("💾 Ruta", str(project_path))
        info_table.add_row("🏷️ Tipo", self._detect_project_type(project_path))
        
        # Tamaño del proyecto
        try:
            total_size = sum(f.stat().st_size for f in project_path.rglob('*') if f.is_file())
            size_mb = total_size / (1024 * 1024)
            info_table.add_row("💾 Tamaño", f"{size_mb:.1f} MB")
        except Exception:
            info_table.add_row("💾 Tamaño", "No calculable")
        
        # Fecha de modificación
        try:
            mod_time = datetime.fromtimestamp(project_path.stat().st_mtime)
            info_table.add_row("📅 Última modificación", mod_time.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception:
            info_table.add_row("📅 Última modificación", "No disponible")
        
        # Archivos principales
        main_files = ['index.html', 'index.php', 'package.json', 'requirements.txt', 'composer.json', 'README.md']
        found_files = []
        for file_name in main_files:
            if (project_path / file_name).exists():
                found_files.append(file_name)
        
        if found_files:
            info_table.add_row("📄 Archivos principales", ', '.join(found_files))
        
        self.menu.console.print(info_table)
    
    def _run_project_server(self, project_path: Path):
        """Ejecuta servidor de desarrollo apropiado para el proyecto."""
        self.menu.clear_screen()
        
        project_type = self._detect_project_type(project_path)
        
        servers = [
            {'name': '🐍 Python HTTP Server (puerto 8000)', 'value': 'python'},
            {'name': '🌐 PHP Server (puerto 8080)', 'value': 'php'},
            {'name': '📦 npm start (Node.js)', 'value': 'npm'},
            {'name': '⚛️ yarn start (React)', 'value': 'yarn'}
        ]
        
        selection = self.menu.show_menu(servers, f"🚀 Servidor para {project_path.name}:")
        
        if not selection or selection == 'exit':
            return
        
        # Cambiar al directorio del proyecto
        original_dir = Path.cwd()
        os.chdir(project_path)
        
        try:
            if selection == 'python':
                self.menu.show_info("🐍 Iniciando servidor Python...")
                self.menu.show_info(f"🌐 Accede a: http://localhost:8000")
                subprocess.run([sys.executable, '-m', 'http.server', '8000'])
            
            elif selection == 'php':
                if self._command_exists('php'):
                    self.menu.show_info("🌐 Iniciando servidor PHP...")
                    self.menu.show_info(f"🌐 Accede a: http://localhost:8080")
                    subprocess.run(['php', '-S', 'localhost:8080'])
                else:
                    self.menu.show_error("❌ PHP no está instalado")
            
            elif selection == 'npm':
                if (project_path / 'package.json').exists():
                    self.menu.show_info("📦 Ejecutando npm start...")
                    subprocess.run(['npm', 'start'])
                else:
                    self.menu.show_error("❌ No se encontró package.json")
            
            elif selection == 'yarn':
                if (project_path / 'package.json').exists():
                    self.menu.show_info("⚛️ Ejecutando yarn start...")
                    subprocess.run(['yarn', 'start'])
                else:
                    self.menu.show_error("❌ No se encontró package.json")
                    
        except KeyboardInterrupt:
            self.menu.show_info("\n🛑 Servidor detenido")
        except Exception as e:
            self.menu.show_error(f"Error ejecutando servidor: {e}")
        finally:
            os.chdir(original_dir)
    
    def _new_project(self):
        """Crea un nuevo proyecto con plantillas."""
        self.menu.clear_screen()
        
        # Solicitar nombre del proyecto
        project_name = self.menu.show_input("🏷️ Nombre del proyecto:")
        
        if not project_name:
            self.menu.show_warning("⚠️ Nombre requerido")
            return
        
        project_path = self.projects_path / project_name
        
        if project_path.exists():
            self.menu.show_error(f"❌ Ya existe un proyecto llamado '{project_name}'")
            return
        
        # Tipos de proyecto
        project_types = [
            {'name': '🌐 Proyecto Web (HTML/CSS/JS)', 'value': 'web'},
            {'name': '🐍 Proyecto Python (Flask)', 'value': 'python'},
            {'name': '📦 Proyecto Node.js (Express)', 'value': 'node'},
            {'name': '⚛️ Proyecto React + TypeScript', 'value': 'react'},
            {'name': '🐘 Proyecto PHP', 'value': 'php'},
            {'name': '📁 Proyecto vacío', 'value': 'empty'}
        ]
        
        project_type = self.menu.show_menu(project_types, f"🏷️ Tipo de proyecto para '{project_name}':")
        
        if not project_type or project_type == 'exit':
            return
        
        try:
            # Crear directorio del proyecto
            project_path.mkdir(parents=True, exist_ok=True)
            os.chdir(project_path)
            
            # Crear estructura según el tipo
            if project_type == 'web':
                self._create_web_project(project_name)
            elif project_type == 'python':
                self._create_python_project(project_name)
            elif project_type == 'node':
                self._create_node_project(project_name)
            elif project_type == 'react':
                self._create_react_project(project_name)
            elif project_type == 'php':
                self._create_php_project(project_name)
            elif project_type == 'empty':
                self._create_empty_project(project_name)
            
            # Inicializar Git
            if self._command_exists('git'):
                subprocess.run(['git', 'init'], capture_output=True)
                subprocess.run(['git', 'add', '.'], capture_output=True)
                subprocess.run(['git', 'commit', '-m', f'Initial commit for {project_name}'], capture_output=True)
            
            self.menu.show_success(f"✅ Proyecto '{project_name}' creado exitosamente!")
            
            # Preguntar si abrir el proyecto
            if self.menu.show_confirmation("¿Quieres abrir el proyecto ahora?"):
                if self._command_exists('code'):
                    subprocess.run(['code', '.'])
                else:
                    webbrowser.open(f"http://localhost/{project_name}")
                    
        except Exception as e:
            self.menu.show_error(f"Error creando proyecto: {e}")
        finally:
            os.chdir(self.projects_path)
    
    def _create_web_project(self, name: str):
        """Crea proyecto web básico."""
        # index.html
        html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>🚀 {name}</h1>
        <p>Proyecto web creado con NooxCLI</p>
    </header>
    
    <main>
        <section>
            <h2>🎉 ¡Bienvenido!</h2>
            <p>Tu proyecto web está listo para desarrollar.</p>
        </section>
    </main>
    
    <script src="script.js"></script>
</body>
</html>'''
        
        # style.css
        css_content = '''/* Estilos para el proyecto */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

header {
    text-align: center;
    background: rgba(255, 255, 255, 0.1);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}

h1 {
    color: white;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

header p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.1rem;
}

main {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

h2 {
    color: #333;
    margin-bottom: 1rem;
    font-size: 1.8rem;
}'''
        
        # script.js
        js_content = f'''// JavaScript para {name}
console.log("🚀 Proyecto {name} iniciado correctamente!");

// Función de bienvenida
function init() {{
    console.log("✨ Proyecto listo para desarrollo");
    
    // Agregar funcionalidad aquí
}}

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", init);'''
        
        # Escribir archivos
        Path('index.html').write_text(html_content, encoding='utf-8')
        Path('style.css').write_text(css_content, encoding='utf-8')
        Path('script.js').write_text(js_content, encoding='utf-8')
        Path('README.md').write_text(f'# {name}\n\nProyecto web creado con NooxCLI\n', encoding='utf-8')
    
    def _create_python_project(self, name: str):
        """Crea proyecto Python con Flask."""
        # Crear estructura
        Path('app.py').write_text(f'''from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', project_name='{name}')

@app.route('/api/test')
def api_test():
    return {{'message': 'API funcionando', 'project': '{name}'}}

if __name__ == '__main__':
    app.run(debug=True)''', encoding='utf-8')
        
        Path('requirements.txt').write_text('flask\nrequests\n', encoding='utf-8')
        
        # Crear carpeta templates
        Path('templates').mkdir(exist_ok=True)
        Path('templates/index.html').write_text(f'''<!DOCTYPE html>
<html>
<head>
    <title>{{{{ project_name }}}}</title>
</head>
<body>
    <h1>🐍 {{{{ project_name }}}}</h1>
    <p>Proyecto Flask creado con NooxCLI</p>
</body>
</html>''', encoding='utf-8')
        
        Path('README.md').write_text(f'# {name}\n\nProyecto Python Flask\n\n## Instalar dependencias\n```\npip install -r requirements.txt\n```\n\n## Ejecutar\n```\npython app.py\n```', encoding='utf-8')
    
    def _create_node_project(self, name: str):
        """Crea proyecto Node.js con Express."""
        # package.json
        package_json = f'''{{
    "name": "{name.lower().replace(' ', '-')}",
    "version": "1.0.0",
    "description": "Proyecto Node.js creado con NooxCLI",
    "main": "index.js",
    "scripts": {{
        "start": "node index.js",
        "dev": "nodemon index.js"
    }},
    "dependencies": {{
        "express": "^4.18.2"
    }},
    "devDependencies": {{
        "nodemon": "^2.0.22"
    }}
}}'''
        
        # index.js
        index_js = f'''const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.static('public'));
app.use(express.json());

// Rutas
app.get('/', (req, res) => {{
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
}});

app.get('/api/test', (req, res) => {{
    res.json({{
        message: 'API funcionando',
        project: '{name}',
        timestamp: new Date().toISOString()
    }});
}});

app.listen(PORT, () => {{
    console.log(`🚀 Servidor ejecutándose en http://localhost:${{PORT}}`);
}});'''
        
        # Crear archivos
        Path('package.json').write_text(package_json, encoding='utf-8')
        Path('index.js').write_text(index_js, encoding='utf-8')
        Path('README.md').write_text(f'# {name}\n\nProyecto Node.js + Express\n\n## Instalar\n```\nnpm install\n```\n\n## Ejecutar\n```\nnpm start\n```', encoding='utf-8')
        
        # Carpeta public
        Path('public').mkdir(exist_ok=True)
        Path('public/index.html').write_text(f'''<!DOCTYPE html>
<html>
<head>
    <title>{name}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>📦 {name}</h1>
    <p>Proyecto Node.js + Express</p>
</body>
</html>''', encoding='utf-8')
    
    def _create_react_project(self, name: str):
        """Crea proyecto React con TypeScript usando create-react-app."""
        if self._command_exists('npx'):
            self.menu.show_info("📦 Creando proyecto React...")
            subprocess.run(['npx', 'create-react-app', '.', '--template', 'typescript'], check=True)
        else:
            # Fallback: crear estructura básica
            self.menu.show_warning("npx no disponible, creando estructura básica...")
            self._create_web_project(name)
    
    def _create_php_project(self, name: str):
        """Crea proyecto PHP básico."""
        # index.php
        php_content = f'''<?php
// {name} - Proyecto PHP
$project_name = "{name}";
$created_at = date('Y-m-d H:i:s');
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title><?= $project_name ?></title>
</head>
<body>
    <h1>🐘 <?= $project_name ?></h1>
    <p>Proyecto PHP creado con NooxCLI</p>
    <p>Creado el: <?= $created_at ?></p>
    
    <?php
    // Código PHP aquí
    echo "<p>✨ PHP funcionando correctamente!</p>";
    ?>
</body>
</html>'''
        
        Path('index.php').write_text(php_content, encoding='utf-8')
        Path('README.md').write_text(f'# {name}\n\nProyecto PHP\n\n## Acceder\nhttp://localhost/{name}', encoding='utf-8')
    
    def _create_empty_project(self, name: str):
        """Crea proyecto vacío con README."""
        Path('README.md').write_text(f'# {name}\n\nProyecto creado con NooxCLI\n\nCreado el: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', encoding='utf-8')
    
    def _clone_repo(self):
        """Clona un repositorio Git."""
        self.menu.clear_screen()
        
        if not self._command_exists('git'):
            self.menu.show_error("❌ Git no está instalado")
            return
        
        repo_url = self.menu.show_input("🔗 URL del repositorio:")
        
        if not repo_url:
            self.menu.show_warning("⚠️ URL requerida")
            return
        
        folder_name = self.menu.show_input("📁 Nombre de carpeta (opcional):", "")
        
        try:
            os.chdir(self.projects_path)
            
            if folder_name:
                self.menu.show_info(f"🔄 Clonando en '{folder_name}'...")
                subprocess.run(['git', 'clone', repo_url, folder_name], check=True)
            else:
                self.menu.show_info("🔄 Clonando repositorio...")
                subprocess.run(['git', 'clone', repo_url], check=True)
            
            self.menu.show_success("✅ Repositorio clonado exitosamente!")
            
        except subprocess.CalledProcessError as e:
            self.menu.show_error(f"Error clonando repositorio: {e}")
    
    def _open_folder(self):
        """Abre la carpeta de proyectos en el explorador."""
        try:
            if os.name == 'nt':
                subprocess.run(['explorer', str(self.projects_path)])
            else:
                subprocess.run(['xdg-open', str(self.projects_path)])
            self.menu.show_success("✅ Carpeta de proyectos abierta")
        except Exception as e:
            self.menu.show_error(f"Error abriendo carpeta: {e}")
    
    def _backup_menu(self):
        """Menú de backup y compresión."""
        self.menu.clear_screen()
        
        backup_options = [
            {'name': '📦 Crear backup de proyecto', 'value': 'backup_single'},
            {'name': '🗜️ Comprimir proyecto', 'value': 'compress'},
            {'name': '📦 Backup de todos los proyectos', 'value': 'backup_all'}
        ]
        
        selection = self.menu.show_menu(backup_options, "📦 Opciones de backup:")
        
        if selection == 'backup_single':
            self._backup_single_project()
        elif selection == 'compress':
            self._compress_project()
        elif selection == 'backup_all':
            self._backup_all_projects()
    
    def _backup_single_project(self):
        """Crea backup de un proyecto específico."""
        projects = self._get_projects()
        if not projects:
            self.menu.show_warning("⚠️ No hay proyectos para respaldar")
            return
        
        project_choices = [{'name': p.name, 'value': str(p)} for p in projects]
        selection = self.menu.show_menu(project_choices, "📁 Proyecto a respaldar:")
        
        if selection and selection != 'exit':
            project_path = Path(selection)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{project_path.name}_{timestamp}.zip"
            backup_path = self.projects_path / backup_name
            
            try:
                self.menu.show_info(f"📦 Creando backup: {backup_name}")
                shutil.make_archive(str(backup_path.with_suffix('')), 'zip', str(project_path))
                self.menu.show_success(f"✅ Backup creado: {backup_name}")
            except Exception as e:
                self.menu.show_error(f"Error creando backup: {e}")
    
    def _compress_project(self):
        """Comprime un proyecto."""
        projects = self._get_projects()
        if not projects:
            self.menu.show_warning("⚠️ No hay proyectos para comprimir")
            return
        
        project_choices = [{'name': p.name, 'value': str(p)} for p in projects]
        selection = self.menu.show_menu(project_choices, "🗆 Proyecto a comprimir:")
        
        if selection and selection != 'exit':
            project_path = Path(selection)
            zip_path = project_path.with_suffix('.zip')
            
            try:
                self.menu.show_info(f"🗜️ Comprimiendo: {project_path.name}")
                shutil.make_archive(str(project_path), 'zip', str(project_path))
                self.menu.show_success(f"✅ Proyecto comprimido: {zip_path.name}")
            except Exception as e:
                self.menu.show_error(f"Error comprimiendo: {e}")
    
    def _backup_all_projects(self):
        """Crea backup de todos los proyectos."""
        projects = self._get_projects()
        if not projects:
            self.menu.show_warning("⚠️ No hay proyectos para respaldar")
            return
        
        if not self.menu.show_confirmation(f"¿Crear backup de {len(projects)} proyecto(s)?"):
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.projects_path / f"backup_all_{timestamp}"
        backup_dir.mkdir()
        
        try:
            for project in projects:
                self.menu.show_info(f"📦 Respaldando: {project.name}")
                backup_path = backup_dir / f"{project.name}.zip"
                shutil.make_archive(str(backup_path.with_suffix('')), 'zip', str(project))
            
            self.menu.show_success(f"✅ Backup completo creado en: {backup_dir.name}")
        except Exception as e:
            self.menu.show_error(f"Error en backup masivo: {e}")
    
    def _deploy_menu(self):
        """Menú de deploy y testing."""
        self.menu.clear_screen()
        
        deploy_options = [
            {'name': '🚀 Deploy via Git', 'value': 'git'},
            {'name': '🧪 Test del proyecto', 'value': 'test'},
            {'name': '🛠️ Build de producción', 'value': 'build'}
        ]
        
        selection = self.menu.show_menu(deploy_options, "🚀 Deploy y Testing:")
        
        if selection == 'git':
            self._deploy_git()
        elif selection == 'test':
            self._run_tests()
        elif selection == 'build':
            self._build_production()
    
    def _deploy_git(self):
        """Deploy via Git."""
        if not self._command_exists('git'):
            self.menu.show_error("❌ Git no instalado")
            return
        
        commit_msg = self.menu.show_input("💬 Mensaje del commit:", "Deploy update")
        
        if commit_msg:
            try:
                subprocess.run(['git', 'add', '.'], check=True)
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                subprocess.run(['git', 'push', 'origin', 'main'], check=True)
                self.menu.show_success("✅ Deploy completado!")
            except subprocess.CalledProcessError as e:
                self.menu.show_error(f"Error en deploy: {e}")
    
    def _run_tests(self):
        """Ejecuta tests del proyecto."""
        test_runners = [
            {'name': '🧪 Jest (JavaScript)', 'value': 'jest'},
            {'name': '🐍 pytest (Python)', 'value': 'pytest'},
            {'name': '📦 npm test', 'value': 'npm'}
        ]
        
        selection = self.menu.show_menu(test_runners, "🧪 Ejecutar tests:")
        
        try:
            if selection == 'jest' and self._command_exists('npm'):
                subprocess.run(['npm', 'test'])
            elif selection == 'pytest' and self._command_exists('pytest'):
                subprocess.run(['pytest'])
            elif selection == 'npm' and self._command_exists('npm'):
                subprocess.run(['npm', 'test'])
        except Exception as e:
            self.menu.show_error(f"Error ejecutando tests: {e}")
    
    def _build_production(self):
        """Build de producción."""
        build_options = [
            {'name': '📦 npm run build', 'value': 'npm'},
            {'name': '🐍 Python setup.py build', 'value': 'python'}
        ]
        
        selection = self.menu.show_menu(build_options, "🛠️ Tipo de build:")
        
        try:
            if selection == 'npm' and self._command_exists('npm'):
                subprocess.run(['npm', 'run', 'build'])
                self.menu.show_success("✅ Build completado!")
            elif selection == 'python':
                subprocess.run([sys.executable, 'setup.py', 'build'])
                self.menu.show_success("✅ Build Python completado!")
        except Exception as e:
            self.menu.show_error(f"Error en build: {e}")
    
    def _docker_menu(self):
        """Menú de operaciones Docker."""
        self.menu.clear_screen()
        
        if not self._command_exists('docker'):
            self.menu.show_error("❌ Docker no está instalado")
            return
        
        docker_options = [
            {'name': '🛠️ Docker build', 'value': 'build'},
            {'name': '🚀 Docker run', 'value': 'run'},
            {'name': '🐳 Docker compose up', 'value': 'compose'},
            {'name': '📄 Ver containers', 'value': 'ps'}
        ]
        
        selection = self.menu.show_menu(docker_options, "🐳 Operaciones Docker:")
        
        try:
            if selection == 'build':
                tag = self.menu.show_input("🏷️ Tag de la imagen:", "my-app")
                subprocess.run(['docker', 'build', '-t', tag, '.'])
                self.menu.show_success(f"✅ Imagen '{tag}' creada")
            
            elif selection == 'run':
                image = self.menu.show_input("🖼️ Imagen a ejecutar:", "my-app")
                subprocess.run(['docker', 'run', '-p', '8080:80', image])
            
            elif selection == 'compose':
                subprocess.run(['docker-compose', 'up', '-d'])
                self.menu.show_success("✅ Docker Compose iniciado")
            
            elif selection == 'ps':
                result = subprocess.run(['docker', 'ps', '-a'], capture_output=True, text=True)
                self.menu.console.print(result.stdout)
                
        except Exception as e:
            self.menu.show_error(f"Error Docker: {e}")
    
    def _config_menu(self):
        """Menú de configuración."""
        self.menu.clear_screen()
        
        config_options = [
            {'name': f'📁 Cambiar directorio de proyectos (actual: {self.projects_path})', 'value': 'change_dir'},
            {'name': '📊 Ver configuración actual', 'value': 'show_config'}
        ]
        
        selection = self.menu.show_menu(config_options, "⚙️ Configuración:")
        
        if selection == 'change_dir':
            new_dir = self.menu.show_input("📁 Nueva ruta de proyectos:", str(self.projects_path))
            if new_dir and Path(new_dir).exists():
                self.projects_path = Path(new_dir)
                self.menu.show_success("✅ Directorio actualizado")
            else:
                self.menu.show_error("❌ Directorio no válido")
        
        elif selection == 'show_config':
            config_table = Table(title="⚙️ Configuración Actual", box=box.SIMPLE)
            config_table.add_column("Propiedad", style="cyan")
            config_table.add_column("Valor", style="white")
            
            config_table.add_row("Directorio de proyectos", str(self.projects_path))
            config_table.add_row("Proyectos encontrados", str(len(self._get_projects())))
            config_table.add_row("Git disponible", "✅" if self._command_exists('git') else "❌")
            config_table.add_row("Docker disponible", "✅" if self._command_exists('docker') else "❌")
            config_table.add_row("Node.js disponible", "✅" if self._command_exists('npm') else "❌")
            
            self.menu.console.print(config_table)
    
    def _command_exists(self, command: str) -> bool:
        """Verifica si un comando existe en el sistema."""
        try:
            subprocess.run([command, '--version'], capture_output=True, check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            # Para VS Code, intentar variaciones del comando
            if command == 'code':
                # Probar code.cmd que es lo que realmente funciona
                try:
                    subprocess.run(['code.cmd', '--version'], capture_output=True, check=True, timeout=5)
                    return True
                except:
                    return self._check_vscode_installation()
            return False
    
    def _check_vscode_installation(self) -> bool:
        """Verifica si VS Code está instalado en ubicaciones comunes."""
        # Rutas comunes donde se instala VS Code
        common_paths = [
            # Tu ubicación específica
            r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd".format(os.environ.get('USERNAME', '')),
            r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.environ.get('USERNAME', '')),
            # Instalaciones del sistema
            r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
            # Comandos en PATH
            "code.cmd",
            "code"
        ]
        
        for path in common_paths:
            try:
                if os.path.exists(path):
                    return True
                # Intentar ejecutar el comando
                subprocess.run([path, '--version'], capture_output=True, check=True, timeout=5)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        # Verificar en PATH del sistema (no solo del usuario)
        try:
            # Obtener PATH completo del sistema
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
                system_path = winreg.QueryValueEx(key, "Path")[0]
                if "Microsoft VS Code" in system_path:
                    return True
        except Exception:
            pass
        
        return False
    
    def _open_vscode(self, project_path: Path) -> bool:
        """Abre VS Code con mejor detección de rutas."""
        # Lista de rutas a probar en orden de preferencia
        vscode_commands = [
            # Comando que sabemos que funciona en tu sistema
            'code.cmd',
            # Comando directo (si está en PATH)
            'code',
            # Tu ubicación específica - comando code
            rf"C:\Users\{os.environ.get('USERNAME', '')}\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
            # Tu ubicación específica - ejecutable directo
            rf"C:\Users\{os.environ.get('USERNAME', '')}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            # Instalaciones del sistema
            r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
        ]
        
        for vscode_cmd in vscode_commands:
            try:
                # Si es solo 'code', intentar como comando
                if vscode_cmd == 'code':
                    subprocess.run([vscode_cmd, str(project_path)], check=True, timeout=10)
                    return True
                
                # Para rutas específicas, verificar que exista primero
                if os.path.exists(vscode_cmd):
                    # Usar Popen para no bloquear
                    subprocess.Popen([vscode_cmd, str(project_path)])
                    return True
                    
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
            except Exception as e:
                # Log del error pero continuar con la siguiente opción
                continue
        
        return False
    
    def _open_terminal(self, project_path: Path) -> bool:
        """Abre terminal en el directorio del proyecto con manejo mejorado de errores."""
        try:
            if os.name == 'nt':
                # Intentar Windows Terminal primero (más moderno)
                if os.environ.get('WT_SESSION'):
                    try:
                        subprocess.Popen([
                            'wt', '-d', str(project_path)
                        ])
                        return True
                    except FileNotFoundError:
                        pass
                
                # Intentar PowerShell 7 primero (pwsh)
                try:
                    subprocess.Popen([
                        'pwsh', '-NoExit', '-Command', 
                        f"Set-Location '{project_path}'; Write-Host 'Directorio: {project_path}' -ForegroundColor Green"
                    ])
                    return True
                except FileNotFoundError:
                    # Fallback a PowerShell 5.1 si pwsh no está disponible
                    try:
                        subprocess.Popen([
                            'powershell', '-NoExit', '-Command', 
                            f"Set-Location '{project_path}'; Write-Host 'Directorio: {project_path}' -ForegroundColor Green"
                        ])
                        return True
                    except Exception:
                        # Último recurso: cmd
                        subprocess.Popen([
                            'cmd', '/k', f'cd /d "{project_path}"'
                        ])
                        return True
            else:
                # Linux/Mac
                terminals = ['gnome-terminal', 'xterm', 'konsole']
                for terminal in terminals:
                    try:
                        subprocess.Popen([terminal, '--working-directory', str(project_path)])
                        return True
                    except FileNotFoundError:
                        continue
            
            return False
            
        except Exception as e:
            self.menu.show_error(f"Error abriendo terminal: {e}")
            return False


def main():
    """Función principal del módulo."""
    proyectos_module = ProyectosModule()
    proyectos_module.main()


if __name__ == "__main__":
    main()
