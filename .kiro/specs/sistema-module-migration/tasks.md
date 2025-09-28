# Implementation Plan

- [-] 1. Implementar módulo sistema.py completo










  - Crear clase SistemaModule con arquitectura consistente
  - Implementar menú principal con todas las opciones del sistema.bat original

  - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1_

- [x] 1.1 Implementar información del sistema


  - Crear función _get_system_info() usando systeminfo y psutil como fallback
  - Formatear información en tabla Rich con hostname, OS, arquitectura, memoria
  - Manejar errores y permisos insuficientes
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 1.2 Implementar gestión de procesos




  - Crear función _show_processes() usando psutil
  - Mostrar procesos en tabla con PID, nombre, CPU, memoria
  - Implementar paginación para muchos procesos
  - Agregar opción para terminar procesos seleccionados
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 1.3 Implementar monitoreo de red


  - Crear función _show_network() usando netstat y psutil.net_connections()
  - Mostrar conexiones activas con protocolo, direcciones y estado
  - Agregar estadísticas de tráfico de red
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 1.4 Implementar información de disco


  - Crear función _show_disk_usage() usando shutil.disk_usage()
  - Mostrar todas las unidades con tamaño, libre y porcentaje usado
  - Agregar advertencias visuales para poco espacio
  - Mostrar tamaño de archivos temporales
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 1.5 Implementar gestión de servicios Windows






  - Crear función _show_services() usando subprocess con sc query
  - Mostrar todos los servicios y filtrar solo los activos
  - Permitir iniciar/detener servicios si hay permisos
  - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 1.6 Implementar visualización de variables de entorno


  - Crear función _show_env_vars() usando os.environ
  - Formatear variables en tabla ordenada con Rich
  - Implementar búsqueda y filtrado de variables
  - Agregar opción para exportar variables a archivo
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [x] 1.7 Implementar limpieza de archivos temporales


  - Crear función _cleanup_temp_files() usando tempfile y shutil
  - Mostrar tamaño actual de archivos temporales antes de limpiar
  - Eliminar archivos temporales de forma segura
  - Reportar espacio liberado y archivos que no se pudieron eliminar
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 1.8 Implementar herramientas del sistema





  - Crear función _open_system_tools() para abrir taskmgr y regedit
  - Verificar que las herramientas existan antes de ejecutarlas
  - Mostrar advertencias de seguridad para regedit
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 1.9 Implementar diagnóstico de red





  - Crear función _network_diagnostics() para IP local y pública
  - Implementar ping interactivo a servidores
  - Agregar función para flush DNS
  - Mostrar configuración completa de red con ipconfig
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 2. Implementar módulo reparar.py completo




  - Crear clase RepararModule con arquitectura consistente
  - Implementar todas las funcionalidades del reparar-perfil.bat original
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [x] 2.1 Implementar backup de perfil PowerShell


  - Crear función _backup_profile() para respaldar perfil actual
  - Generar nombre de backup con timestamp
  - Verificar que el directorio de PowerShell exista
  - _Requirements: 10.1_

- [x] 2.2 Implementar generación de perfil PowerShell


  - Crear función _generate_profile() con configuración UTF-8 completa
  - Incluir configuración de codificación y chcp 65001
  - Agregar imports de PSReadLine y configuración de predicciones
  - Configurar oh-my-posh en PATH y tema
  - Agregar aliases útiles (dev, sys, proj, config, ll)
  - Crear mensaje de bienvenida personalizado con información del sistema
  - _Requirements: 10.2, 10.3_

- [x] 2.3 Implementar verificación de sintaxis


  - Crear función _verify_syntax() usando PowerShell -NoProfile
  - Validar que el perfil generado no tenga errores de sintaxis
  - Reportar errores específicos si los hay
  - _Requirements: 10.4_

- [x] 2.4 Implementar configuración oh-my-posh


  - Crear función _configure_omp() para configurar oh-my-posh
  - Verificar instalación de oh-my-posh
  - Configurar tema por defecto (avit.omp.json)
  - Agregar oh-my-posh al PATH del perfil
  - _Requirements: 10.3_

- [x] 3. Implementar módulo test_utf8.py completo





  - Crear clase TestUtf8Module con arquitectura consistente
  - Implementar todas las pruebas del test-utf8.bat original
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [x] 3.1 Implementar test de caracteres especiales básicos


  - Crear función _test_basic_chars() con ñ, acentos, diéresis
  - Mostrar caracteres en formato organizado y legible
  - Incluir caracteres de diferentes idiomas (francés, alemán, etc.)
  - _Requirements: 11.1, 11.2_

- [x] 3.2 Implementar test de símbolos de caja


  - Crear función _test_box_chars() con box drawing characters
  - Mostrar diferentes estilos de cajas (simple, doble, redondeada)
  - Crear ejemplos visuales de cajas completas
  - _Requirements: 11.2_

- [x] 3.3 Implementar test de emojis y símbolos Unicode


  - Crear función _test_emojis() con emojis comunes de desarrollo
  - Incluir símbolos matemáticos, técnicos y de moneda
  - Mostrar caracteres de programación especiales
  - _Requirements: 11.2_

- [x] 3.4 Implementar test de colores ANSI


  - Crear función _test_colors() con códigos de color ANSI
  - Mostrar paleta de colores básicos y extendidos
  - Verificar soporte de colores en la terminal actual
  - _Requirements: 11.2_

- [x] 3.5 Implementar diagnóstico de codificación


  - Crear función _diagnostic_encoding() para mostrar configuración actual
  - Mostrar página de códigos activa con chcp
  - Verificar OutputEncoding de PowerShell y Console
  - Mostrar configuración del registro de Windows
  - Sugerir ejecutar config-consola si hay problemas
  - _Requirements: 11.3, 11.4_

- [x] 4. Verificar y completar módulo config.py




  - Revisar implementación actual del módulo config.py
  - Comparar con funcionalidades del config-consola.bat original
  - Implementar funcionalidades faltantes si las hay
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 4.1 Verificar configuración completa UTF-8


  - Revisar si _apply_full_config() está implementada correctamente
  - Verificar configuración de página de códigos UTF-8 (65001)
  - Verificar configuración de fuente de consola en registro
  - Verificar configuración de PowerShell OutputEncoding
  - _Requirements: 12.1, 12.2_

- [x] 4.2 Verificar configuración de fuentes


  - Revisar si _configure_font() permite seleccionar fuentes
  - Verificar soporte para Cascadia Code, Consolas, JetBrains Mono
  - Verificar modificación correcta del registro HKCU\Console
  - _Requirements: 12.2_

- [x] 4.3 Verificar restauración de configuración


  - Revisar si _restore_config() elimina configuraciones personalizadas
  - Verificar restauración de página de códigos predeterminada
  - Verificar limpieza de configuraciones de fuente del registro
  - _Requirements: 12.4_

- [x] 4.4 Verificar visualización de configuración actual


  - Revisar si _show_current_config() muestra toda la información
  - Verificar que muestre página de códigos, fuente, y codificación
  - Verificar formato de tabla Rich consistente con otros módulos
  - _Requirements: 12.5_

- [x] 5. Integrar todos los módulos en el menú principal





  - Verificar que todos los módulos estén importados correctamente en main.py
  - Actualizar el menú principal para incluir todos los módulos completados
  - Verificar que las funciones main() de cada módulo funcionen correctamente
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [x] 6. Realizar pruebas de integración completas




  - Probar cada módulo individualmente en diferentes sistemas operativos
  - Verificar manejo de errores y permisos insuficientes
  - Probar funcionalidades que requieren permisos administrativos
  - Verificar consistencia visual y de UX entre todos los módulos
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_