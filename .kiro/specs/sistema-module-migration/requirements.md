# Requirements Document

## Introduction

Este documento define los requerimientos para completar la migración de TODOS los módulos faltantes de NooxCLI. Los módulos deben replicar todas las funcionalidades de los archivos .bat originales, proporcionando herramientas completas con una interfaz moderna e interactiva usando Rich y el framework de menús existente.

Los módulos a completar son:
- `sistema.py` (desde sistema.bat)
- `reparar.py` (desde reparar-perfil.bat) 
- `test_utf8.py` (desde test-utf8.bat)
- Verificar y completar `config.py` (desde config-consola.bat)

## Requirements

### Requirement 1

**User Story:** Como desarrollador, quiero acceder a información detallada del sistema, para poder diagnosticar problemas y conocer las especificaciones de mi entorno de trabajo.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Información del sistema" THEN el sistema SHALL mostrar información completa del host, OS, arquitectura y memoria
2. WHEN se muestra la información THEN el sistema SHALL formatear los datos en una tabla legible con Rich
3. IF el comando systeminfo no está disponible THEN el sistema SHALL usar métodos alternativos de Python para obtener información del sistema

### Requirement 2

**User Story:** Como administrador del sistema, quiero ver los procesos en ejecución, para poder monitorear el rendimiento y identificar procesos problemáticos.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Procesos en ejecución" THEN el sistema SHALL mostrar una lista de procesos activos
2. WHEN se muestran los procesos THEN el sistema SHALL incluir PID, nombre, uso de CPU y memoria
3. WHEN hay muchos procesos THEN el sistema SHALL implementar paginación o filtrado
4. IF el usuario lo solicita THEN el sistema SHALL permitir terminar procesos seleccionados

### Requirement 3

**User Story:** Como administrador de red, quiero monitorear el uso de red y conexiones activas, para diagnosticar problemas de conectividad.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Uso de red" THEN el sistema SHALL mostrar conexiones de red activas
2. WHEN se muestran las conexiones THEN el sistema SHALL incluir protocolo, dirección local, dirección remota y estado
3. WHEN se solicite THEN el sistema SHALL mostrar estadísticas de tráfico de red

### Requirement 4

**User Story:** Como administrador del sistema, quiero verificar el espacio disponible en disco, para prevenir problemas de almacenamiento.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Espacio en disco" THEN el sistema SHALL mostrar información de todas las unidades
2. WHEN se muestra el espacio THEN el sistema SHALL incluir tamaño total, espacio libre y porcentaje usado
3. WHEN se detecte poco espacio THEN el sistema SHALL mostrar advertencias visuales
4. WHEN se solicite THEN el sistema SHALL mostrar el tamaño de archivos temporales

### Requirement 5

**User Story:** Como administrador del sistema, quiero gestionar servicios de Windows, para controlar qué servicios están ejecutándose.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Servicios de Windows" THEN el sistema SHALL mostrar opciones para ver servicios
2. WHEN se seleccione "Ver todos" THEN el sistema SHALL listar todos los servicios con su estado
3. WHEN se seleccione "Ver en ejecución" THEN el sistema SHALL filtrar solo servicios activos
4. IF el usuario tiene permisos THEN el sistema SHALL permitir iniciar/detener servicios

### Requirement 6

**User Story:** Como desarrollador, quiero ver las variables de entorno del sistema, para verificar configuraciones y rutas importantes.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Variables de entorno" THEN el sistema SHALL mostrar todas las variables
2. WHEN se muestran las variables THEN el sistema SHALL formatearlas en una tabla ordenada
3. WHEN hay muchas variables THEN el sistema SHALL implementar búsqueda o filtrado
4. WHEN se solicite THEN el sistema SHALL permitir exportar las variables a un archivo

### Requirement 7

**User Story:** Como administrador del sistema, quiero limpiar archivos temporales, para liberar espacio en disco y mejorar el rendimiento.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Limpiar archivos temporales" THEN el sistema SHALL mostrar el tamaño actual de archivos temporales
2. WHEN se confirme la limpieza THEN el sistema SHALL eliminar archivos temporales de forma segura
3. WHEN se complete la limpieza THEN el sistema SHALL mostrar el espacio liberado
4. IF hay archivos en uso THEN el sistema SHALL omitirlos y reportar cuáles no se pudieron eliminar

### Requirement 8

**User Story:** Como administrador del sistema, quiero acceso rápido a herramientas del sistema, para realizar tareas administrativas comunes.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Administrador de tareas" THEN el sistema SHALL abrir el Task Manager
2. WHEN el usuario selecciona "Editor del registro" THEN el sistema SHALL abrir regedit con advertencias de seguridad
3. WHEN se abran herramientas externas THEN el sistema SHALL verificar que existan antes de ejecutarlas

### Requirement 9

**User Story:** Como administrador de red, quiero herramientas de diagnóstico de red, para resolver problemas de conectividad.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Información de IP/Red" THEN el sistema SHALL mostrar configuración de red completa
2. WHEN se muestre la IP THEN el sistema SHALL incluir tanto IP local como IP pública
3. WHEN el usuario selecciona "Ping a servidor" THEN el sistema SHALL permitir hacer ping interactivo
4. WHEN el usuario selecciona "Flush DNS" THEN el sistema SHALL limpiar la cache DNS y confirmar la acción

### Requirement 10

**User Story:** Como desarrollador, quiero reparar mi perfil de PowerShell cuando esté corrupto, para restaurar mi entorno de desarrollo personalizado.

#### Acceptance Criteria

1. WHEN el usuario selecciona "Reparar perfil PowerShell" THEN el sistema SHALL crear un backup del perfil actual
2. WHEN se repare el perfil THEN el sistema SHALL generar un nuevo perfil con configuración UTF-8 correcta
3. WHEN se genere el perfil THEN el sistema SHALL incluir aliases útiles y configuración de oh-my-posh
4. WHEN se complete la reparación THEN el sistema SHALL verificar la sintaxis del nuevo perfil

### Requirement 11

**User Story:** Como usuario, quiero probar si mi configuración UTF-8 funciona correctamente, para verificar que puedo ver caracteres especiales.

#### Acceptance Criteria

1. WHEN el usuario ejecute el test UTF-8 THEN el sistema SHALL mostrar caracteres especiales, emojis y símbolos
2. WHEN se muestren los caracteres THEN el sistema SHALL incluir ñ, acentos, símbolos de caja y emojis
3. WHEN se solicite diagnóstico THEN el sistema SHALL mostrar información de codificación actual
4. WHEN se detecten problemas THEN el sistema SHALL sugerir ejecutar la configuración de consola

### Requirement 12

**User Story:** Como usuario, quiero configurar mi consola para UTF-8, para poder ver correctamente caracteres especiales en todos mis scripts.

#### Acceptance Criteria

1. WHEN el usuario seleccione configuración completa THEN el sistema SHALL aplicar página de códigos UTF-8
2. WHEN se configure la consola THEN el sistema SHALL establecer fuente apropiada para UTF-8
3. WHEN se apliquen cambios THEN el sistema SHALL modificar el registro de Windows correctamente
4. WHEN se solicite THEN el sistema SHALL permitir restaurar configuración predeterminada
5. WHEN se solicite THEN el sistema SHALL mostrar configuración actual del sistema

### Requirement 13

**User Story:** Como usuario del sistema, quiero una interfaz consistente con el resto de NooxCLI, para tener una experiencia de usuario uniforme.

#### Acceptance Criteria

1. WHEN se use cualquier módulo THEN el sistema SHALL usar el framework NooxMenu existente
2. WHEN se muestren datos THEN el sistema SHALL usar Rich para formateo visual
3. WHEN ocurran errores THEN el sistema SHALL manejarlos de forma consistente con otros módulos
4. WHEN se complete una acción THEN el sistema SHALL mostrar confirmación visual apropiada
5. WHEN se requieran permisos administrativos THEN el sistema SHALL informar claramente al usuario