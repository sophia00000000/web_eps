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

## Roles y casos de uso recomendados

La pagina tiene fines educativos, asi que conviene separar los casos de uso por rol para observar mejor cada patron:

| Rol | Puede hacer | No puede hacer |
| --- | --- | --- |
| Admin | Ver panel general, gestionar afiliaciones, cotizar y auditar planes, revisar autorizaciones, crear usuarios y revisar citas | Procesar atenciones medicas |
| Medico | Procesar citas, urgencias e hospitalizacion, registrar diagnostico, solicitar autorizaciones, ver planes del paciente | Gestionar usuarios y editar coberturas de planes |
| Auxiliar | Registrar solicitudes de autorizacion, consultar estados, agendar citas, ver planes disponibles, asignar paciente a plan | Procesar el paso clinico de la atencion |

- **Admin**: administracion general del sistema. Puede crear o revisar coberturas de planes con Visitor, cotizar todos los planes, auditar planes y servicios, gestionar afiliaciones con State, activar, suspender o cancelar afiliaciones, ver historial de autorizaciones con Chain, crear usuarios y asignar roles, y ver el panel general. No debe procesar atenciones medicas.
- **Medico**: evaluacion clinica. Puede procesar cita, urgencia y hospitalizacion con Template Method, ver citas agendadas, registrar diagnostico y observaciones, solicitar autorizaciones con Chain y consultar planes del paciente en solo lectura.
- **Auxiliar**: soporte operativo. Puede registrar solicitudes de autorizacion, consultar estado de autorizacion y afiliacion, agendar cita para paciente, ver planes disponibles con Visitor, asignar paciente a plan y revisar historial de atenciones.

En esta version, la atencion medica se procesa solo con el medico correspondiente y el campo medico queda fijado al usuario autenticado. El admin puede revisar las citas, pero no ejecutar el paso clinico.

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
- Solicitud pendiente para `Ana Torres` (cirugia menor) — ejemplo de procedimiento que requiere validacion de cobertura y niveles.
- Solicitud pendiente para `Jorge Martinez` (ortopedia) — ejemplo de evaluacion por especialidad.
- Solicitud aprobada para `Sofia Alvarez` (endodoncia) — muestra autorizacion cubierta por plan odontologico.

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

**Plan Basico (id 1)**: cobertura `general`. Soporta consultas generales y examenes de baja complejidad como `Consulta General` y `Examen de Laboratorio`. Procedimientos de alta complejidad suelen quedar fuera y requeriran autorizacion adicional o rechazo.

**Plan Premium (id 2)**: cobertura `amplia`. Soporta `Consulta General`, `Examen de Laboratorio`, `Consulta Especializada`, `Cirugia Menor` y `Ortopedia` en la muestra. Incluye cobertura ampliada y `incluye_ortodoncia = 1`, por lo que varios procedimientos pasan la validacion de cobertura y luego se revisan por nivel de aprobacion.

**Plan Odontologico (id 3)**: cobertura `odontologia`. Esta especializado en servicios dentales; cubre procedimientos odontologicos como `Endodoncia` y tratamientos dentales que el `Plan Basico` no cubre.

## Cómo se evalúan las autorizaciones (resumen del Chain of Responsibility)

1. **Validación de documentos**: el primer paso comprueba que el paciente y su documento existan.
2. **Estado de afiliación**: si la afiliación está `suspendida` o `pendiente`, la solicitud puede ser rechazada o puesta en espera.
3. **Cobertura por plan**: se verifica si el `plan_id` del paciente y la `cobertura` del plan incluyen el `tipo_servicio` solicitado (p. ej. `odontologia` para `Endodoncia`).
4. **Requiere especialidad**: algunos servicios necesitan un especialista; si no se cumple, la autorización puede bajar de nivel o rechazarse.
5. **Aprobación final**: en función del `nivel_complejidad` del servicio se asigna un `nivel_aprobacion` y el resultado final (`aprobada`, `rechazada`, `pendiente`).

En la demo los seeds representan casos concretos para probar cada rama: aprobaciones simples, rechazos por afiliación y solicitudes pendientes que requieren pasos adicionales.

## Servicios por plan (ejemplo)

- **Plan Basico (id 1)**: consultas generales, exámenes de laboratorio y procedimientos de baja complejidad. No cubre procedimientos quirúrgicos importantes ni tratamientos odontológicos especializados.

- **Plan Premium (id 2)**: cubre consultas, exámenes, consultas especializadas y muchos procedimientos (incluye cobertura ampliada para procedimientos de complejidad media y alta). En la muestra soporta `Cirugia Menor` y `Ortopedia` y tiene mayor probabilidad de aprobación según la cadena.

- **Plan Odontologico (id 3)**: especializado en servicios dentales; cubre procedimientos odontológicos como `Endodoncia` y tratamientos dentales que el `Plan Basico` no cubre.

Nota: en este demo la relación entre `plan.cobertura` y `servicio.tipo_servicio` se usa de forma simplificada para decidir cobertura; extiende la lógica en `business/patterns/chain_of_responsibility.py` para reglas reales.

## Significado del `nivel_aprobacion`

El campo `nivel_aprobacion` refleja la severidad y el grado de aprobación que la cadena asigna a una solicitud. Valores típicos en la demo:

- `0` — Pendiente: la solicitud está registrada pero aún no fue procesada/completa.
- `1` — Rechazada / nivel mínimo: la solicitud no cumple requisitos (p. ej. afiliación suspendida o cobertura inexistente).
- `2` — Aprobación parcial / revisión: requiere validación adicional por especialista o autorización de segundo nivel.
- `3` — Aprobación condicional: aprobada con condiciones administrativas (necesita supervisión o documentación complementaria).
- `4` — Aprobación completa: autorizada sin más requisitos.

Ejemplos en los seeds:
- `Ana Torres` — solicitud para `Cirugia Menor`: queda `pendiente` (nivel `0`) para demostrar flujo de evaluación.
- `Jorge Martinez` — solicitud de `Ortopedia`: `pendiente` (nivel `0`) para revisión por especialidad.
- `Sofia Alvarez` — `Endodoncia`: ejemplo aprobado con `nivel_aprobacion = 4` porque su plan odontológico cubre el servicio.

Estos valores alimentan la UI y permiten comparar rutas del Chain of Responsibility en el demo.

## Casos de uso soportados

### 1. Autenticacion de empleados

Permite ingresar al panel con usuario y clave. El sistema muestra el acceso segun el rol.

### 2. Validacion de autorizaciones

El usuario medico puede procesar una solicitud. El admin puede ver el historial, pero no ejecutar el flujo clinico. La cadena valida:

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

El usuario medico puede registrar una atencion como:

- cita programada
- urgencia
- hospitalizacion

El flujo comun se ejecuta con Template Method y cada tipo redefine sus pasos variables. El medico asignado es el usuario autenticado; la fecha y hora se aceptan como dato de registro y no bloquean el procesamiento en el demo.

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
