# EPS App Demo

Aplicacion web de ejemplo para una EPS desarrollada con Flask, SQLite y arquitectura de tres capas. El proyecto implementa cuatro patrones de comportamiento:

- Chain of Responsibility para validacion de autorizaciones.
- State para estados de afiliacion.
- Template Method para atencion de citas medicas.
- Visitor para gestion de planes y servicios.

## Requisitos

- Python 3.14 o compatible con el entorno virtual del proyecto.
- Flask, instalado desde `requirements.txt`.

## Como correr el demo

1. Abrir una terminal en la carpeta `eps_app`.
2. Activar el entorno virtual del workspace.
3. Instalar dependencias.
4. Ejecutar la aplicacion.

```powershell
python -m pip install -r requirements.txt
python app.py
```

5. Abrir en el navegador:

```text
http://127.0.0.1:5000/login
```

## Credenciales de prueba

La aplicacion trabaja con usuarios de empleado:

- `admin` / `admin`
- `medico` / `medico`
- `auxiliar` / `auxiliar`

## Datos de ejemplo cargados

La base de datos SQLite se crea automaticamente y se llena con ejemplos para probar el flujo completo.

### Pacientes

- `Paciente Demo` - documento `1001` - afiliacion activa.
- `Mariana Gomez` - documento `1002` - afiliacion activa.
- `Carlos Perez` - documento `1003` - afiliacion suspendida.
- `Laura Ruiz` - documento `1004` - afiliacion pendiente.
 - `Ana Torres` - documento `1005` - afiliacion activa - asignada a `Plan Basico`.
 - `Jorge Martinez` - documento `1006` - afiliacion activa - asignado a `Plan Premium`.
 - `Sofia Alvarez` - documento `1007` - afiliacion activa - asignada a `Plan Odontologico`.
 - `Miguel Sanchez` - documento `1008` - afiliacion pendiente - asignado a `Plan Premium`.

### Afiliaciones

- Afiliacion activa para `Paciente Demo`.
- Afiliacion activa para `Mariana Gomez`.
- Afiliacion suspendida para `Carlos Perez`.
- Afiliacion pendiente para `Laura Ruiz`.

### Autorizaciones

- Solicitud aprobada para `Paciente Demo`.
- Solicitud aprobada para `Mariana Gomez`.
- Solicitud rechazada para `Carlos Perez` por afiliacion suspendida.
 - Solicitud pendiente para `Ana Torres` (cirugía menor) — ejemplo de procedimiento que requiere validación de cobertura y niveles.
 - Solicitud pendiente para `Jorge Martinez` (ortopedia) — ejemplo de evaluación por especialidad.
 - Solicitud aprobada para `Sofia Alvarez` (endodoncia) — muestra autorización cubierta por plan odontológico.

### Citas

- Cita programada para `Paciente Demo` con `Dra. Lopez`.
- Urgencia atendida para `Mariana Gomez` con `Dr. Vargas`.
- Hospitalizacion programada para `Carlos Perez` con `Dr. Molina`.

### Planes y servicios

- `Plan Basico`.
- `Plan Premium`.
- Servicios cargados: consulta general, triage de urgencias, examen de laboratorio y consulta especializada.

Se añadieron además:
- `Plan Odontologico` (id 3).
- Servicios/procedimientos: `Cirugia Menor`, `Ortopedia`, `Endodoncia`.

## Qué permite cada plan y cómo afectan las autorizaciones

- **Plan Basico (id 1)**: cobertura `general`. Cubre consultas generales y exámenes de baja complejidad. Procedimientos de alta complejidad suelen quedar fuera y requerirán autorización adicional o rechazo.

- **Plan Premium (id 2)**: cobertura `amplia`. Cubre consultas, exámenes y muchos procedimientos; incluye cobertura ampliada y `incluye_ortodoncia = 1` en la muestra. Procedimientos de complejidad alta pueden necesitar aprobaciones de niveles superiores (simulado por la cadena).

- **Plan Odontologico (id 3)**: cobertura `odontologia`. Está especializado en servicios dentales (por ejemplo `Endodoncia`) y permite autorizaciones para procedimientos odontológicos que el `Plan Basico` no cubriría.

## Cómo se evalúan las autorizaciones (resumen del Chain of Responsibility)

1. **Validación de documentos**: el primer paso comprueba que el paciente y su documento existan.
2. **Estado de afiliación**: si la afiliación está `suspendida` o `pendiente`, la solicitud puede ser rechazada o puesta en espera.
3. **Cobertura por plan**: se verifica si el `plan_id` del paciente y la `cobertura` del plan incluyen el `tipo_servicio` solicitado (p. ej. `odontologia` para `Endodoncia`).
4. **Requiere especialidad**: algunos servicios necesitan un especialista; si no se cumple, la autorización puede bajar de nivel o rechazarse.
5. **Aprobación final**: en función del `nivel_complejidad` del servicio se asigna un `nivel_aprobacion` y el resultado final (`aprobada`, `rechazada`, `pendiente`).

En la demo los seeds representan casos concretos para probar cada rama: aprobaciones simples, rechazos por afiliación y solicitudes pendientes que requieren pasos adicionales.

## Casos de uso soportados

### 1. Autenticacion de empleados

Permite ingresar al panel con usuario y clave. El sistema muestra el acceso segun el rol.

### 2. Validacion de autorizaciones

El usuario medico o admin puede procesar una solicitud. La cadena valida:

1. Documentos.
2. Afiliacion.
3. Cobertura.
4. Especialidad.
5. Aprobacion final.

### 3. Gestion de afiliaciones

El usuario admin o auxiliar puede ver las afiliaciones y cambiar su estado a:

- activa
- suspendida
- cancelada

### 4. Atencion de citas medicas

El usuario medico o admin puede registrar una atencion como:

- cita programada
- urgencia
- hospitalizacion

El flujo comun se ejecuta con Template Method y cada tipo redefine sus pasos variables.

### 5. Gestion de planes y servicios

El usuario admin puede revisar planes, cotizaciones, reportes y auditoria usando Visitor.

## Arquitectura de la aplicacion

La aplicacion sigue tres capas:

### Presentacion

- `presentation/controllers/`
- `presentation/templates/`

Aqui viven las rutas Flask, el login y las pantallas HTML.

### Negocio

- `business/services/`
- `business/patterns/`

Aqui esta la logica de negocio y la implementacion de los patrones de comportamiento.

### Datos

- `data/models/`
- `data/daos/`
- `data/database.py`

Aqui se encuentra la conexion SQLite, el esquema de tablas, los modelos y el acceso a datos.

## Rutas principales

- `/login`: acceso de empleados.
- `/dashboard`: panel principal.
- `/autorizaciones/`: gestion de autorizaciones.
- `/afiliaciones/`: gestion de estados de afiliacion.
- `/citas/`: gestion de atenciones medicas.
- `/planes/`: gestion de planes y servicios.

## Notas de uso

- La base de datos `eps.sqlite3` se crea automaticamente al iniciar la app.
- Si quieres reiniciar los datos de prueba, elimina `eps.sqlite3` y vuelve a ejecutar `python app.py`.
- Los formularios del demo ya vienen precargados con ejemplos para facilitar las pruebas manuales.
