# Casos de uso por rol para probar la EPS App

Este documento resume pruebas manuales por rol para validar el comportamiento de la aplicacion educativa.
La base de datos ya incluye datos de ejemplo para ejecutar los casos sin crear registros nuevos.

## Credenciales de prueba

- `admin` / `admin`
- `medico` / `medico`
- `auxiliar` / `auxiliar`

## Datos iniciales relevantes

### Pacientes y plan asociado

- `Paciente Demo` - documento `1001` - plan `Plan Basico`
- `Mariana Gomez` - documento `1002` - plan `Plan Premium`
- `Carlos Perez` - documento `1003` - plan `Plan Basico`
- `Laura Ruiz` - documento `1004` - plan `Plan Premium`
- `Ana Torres` - documento `1005` - plan `Plan Basico`
- `Jorge Martinez` - documento `1006` - plan `Plan Premium`
- `Sofia Alvarez` - documento `1007` - plan `Plan Odontologico`
- `Miguel Sanchez` - documento `1008` - plan `Plan Premium`

### Planes y servicios soportados

- `Plan Basico`: `Consulta General`, `Examen de Laboratorio`
- `Plan Premium`: `Consulta General`, `Examen de Laboratorio`, `Consulta Especializada`, `Cirugia Menor`, `Ortopedia`
- `Plan Odontologico`: `Endodoncia` y otros servicios odontologicos

### Autorizaciones de ejemplo ya cargadas

- `Paciente Demo` + `Consulta General` -> aprobada
- `Mariana Gomez` + `Examen de Laboratorio` -> aprobada
- `Carlos Perez` + `Consulta Especializada` -> rechazada por afiliacion suspendida
- `Ana Torres` + `Cirugia Menor` -> pendiente
- `Jorge Martinez` + `Ortopedia` -> pendiente
- `Sofia Alvarez` + `Endodoncia` -> aprobada

## Casos de uso por rol

### 1. Admin

| Caso | Datos de entrada | Resultado esperado |
| --- | --- | --- |
| Ver panel general | Ingresar con `admin / admin` y abrir `/dashboard` | Se muestra el panel general con accesos visibles a autorizaciones, afiliaciones, citas y planes segun permisos del menu |
| Gestionar afiliacion | Abrir `/afiliaciones/` y usar `Ana Torres` o `Carlos Perez` | Puede activar, suspender o cancelar una afiliacion y el estado cambia en la tabla |
| Revisar historial de autorizaciones | Abrir `/autorizaciones/` | Ve el historial completo, pero no debe usar la pantalla como flujo clinico principal |
| Cotizar planes con Visitor | Abrir `/planes/` | Debe ver las cotizaciones de `Plan Basico`, `Plan Premium` y `Plan Odontologico` |
| Auditar planes y servicios | Abrir `/planes/` | Debe ver los reportes y auditorias generados por Visitor |
| Crear usuarios y roles | Usar la gestion administrativa disponible en la app | Debe poder registrar empleados y asignar roles de manera conceptual dentro del proyecto educativo |
| Intentar procesar atencion medica | Abrir `/citas/` | Solo debe poder revisar el historial; no debe ejecutar el boton de procesar atencion |

### 2. Medico

| Caso | Datos de entrada | Resultado esperado |
| --- | --- | --- |
| Procesar cita programada | Ingresar con `medico / medico`, abrir `/citas/`, elegir `Paciente Demo` y tipo `cita` | Se registra la atencion con `Template Method`, el medico queda fijado al usuario autenticado y se crea el diagnostico de cita |
| Procesar urgencia | Elegir `Mariana Gomez` y tipo `urgencia` | Se registra una urgencia y se genera la factura/diagnostico del flujo de urgencia |
| Procesar hospitalizacion | Elegir `Carlos Perez` y tipo `hospitalizacion` | Se registra la hospitalizacion con el flujo comun y el diagnostico correspondiente |
| Solicitar autorizacion | Abrir `/autorizaciones/` y usar `Mariana Gomez` con `Examen de Laboratorio` o `Sofia Alvarez` con `Endodoncia` | La solicitud pasa por la cadena de validacion y se aprueba o rechaza segun cobertura, afiliacion y especialidad |
| Ver planes del paciente | Abrir `/planes/` | Puede revisar planes y servicios en modo de lectura |
| Ver citas agendadas | Abrir `/citas/` | Debe ver el listado de atenciones registradas |

### 3. Auxiliar

| Caso | Datos de entrada | Resultado esperado |
| --- | --- | --- |
| Registrar solicitud de autorizacion | Ingresar con `auxiliar / auxiliar`, abrir `/autorizaciones/`, seleccionar `Ana Torres` y `Cirugia Menor` | Se registra la solicitud y el resultado esperado es `pendiente` por revision adicional |
| Consultar estado de autorizacion | Abrir `/autorizaciones/` y revisar historial | Debe ver autorizaciones aprobadas, rechazadas y pendientes con su nivel de aprobacion |
| Consultar estado de afiliacion | Abrir `/afiliaciones/` | Debe ver estados `activa`, `pendiente` y `suspendida` |
| Agendar cita para paciente | Abrir `/citas/` si el menu lo muestra segun permiso de la interfaz | Debe poder preparar el registro de cita, pero el procesamiento clinico queda al medico |
| Ver planes disponibles | Abrir `/planes/` si la interfaz del rol lo permite | Debe poder consultar los planes y sus coberturas de forma de lectura |
| Asignar paciente a plan | Usar los datos de `Ana Torres`, `Jorge Martinez` o `Miguel Sanchez` | Debe quedar visible el plan asociado al paciente en el sistema y en las vistas que muestran afiliaciones |
| Ver historial de atenciones | Revisar `/citas/` | Debe consultar el historial, pero sin ejecutar el paso clinico del Template Method |

## Resultado esperado por patron

- **Chain of Responsibility**: las solicitudes de autorizacion deben terminar en `aprobada`, `rechazada` o `pendiente` segun documento, afiliacion, cobertura, especialidad y aprobacion final.
- **State**: las afiliaciones deben cambiar entre `activa`, `suspendida` y `cancelada`.
- **Template Method**: la atencion medica debe seguir el mismo flujo general, cambiando solo el tipo de atencion.
- **Visitor**: los planes deben poder cotizarse, auditarse y reportarse sin cambiar la estructura del objeto plan.

## Recomendacion de prueba rapida

1. Entrar como `admin` y validar `afiliaciones` y `planes`.
2. Entrar como `medico` y procesar una `cita` y una `urgencia`.
3. Entrar como `auxiliar` y revisar el historial de autorizaciones.
4. Comparar los resultados con la tabla anterior.

## Observaciones

- La app es educativa, por lo que la fecha y hora de la atencion no bloquean el flujo clinico.
- El medico corresponde al usuario autenticado.
- El admin puede revisar la informacion, pero no ejecutar el paso clinico.
