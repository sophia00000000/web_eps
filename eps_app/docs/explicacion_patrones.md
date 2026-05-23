# Analisis y diseno de patrones de comportamiento

## Vista general
La aplicacion EPS se organizo en tres capas:
- Presentacion: controladores Flask y plantillas HTML.
- Negocio: servicios y patrones de comportamiento.
- Datos: SQLite, DAOs y modelos.

La aplicacion trabaja con autenticacion de empleados y permisos por rol:
- `admin`: acceso total.
- `medico`: autorizaciones y citas.
- `auxiliar`: afiliaciones.

## 1. Template Method
Define el esqueleto comun de la atencion medica en `AtencionMedicaTemplate`.
Las clases `CitaMedica`, `UrgenciaMedica` y `HospitalizacionMedica` solo cambian los pasos variables.

Flujo aplicado:
1. Registrar paciente.
2. Validar afiliacion.
3. Asignar medico.
4. Ejecutar la atencion especifica.
5. Generar diagnostico.
6. Generar factura.

La operacion principal se concentra en `procesar_atencion()`, que queda como esqueleto fijo del algoritmo.

## 2. State
`AfiliacionContexto` delega el comportamiento a `AfiliacionPendiente`, `AfiliacionActiva`, `AfiliacionSuspendida` y `AfiliacionCancelada`.
Cada estado decide si la afiliacion permite servicios y cuando cambia al siguiente estado.

Flujo aplicado:
1. Se crea la afiliacion en estado inicial.
2. El contexto cambia con `activar()`, `suspender()` o `cancelar()`.
3. El estado decide si se habilitan o bloquean servicios.
4. Si se cancela, se registra `fecha_cancelacion` en el contexto y en la base de datos.

## 3. Chain of Responsibility
La autorizacion pasa por `DocumentValidator`, `AffiliationValidator`, `CoverageValidator`, `SpecialistValidator` y `FinalApprovalValidator`.
Cada validador decide si continua o rechaza la solicitud.

Flujo aplicado:
1. El paciente solicita la autorizacion.
2. Se valida documento.
3. Se valida afiliacion.
4. Se valida cobertura.
5. Se valida especialidad.
6. Se aprueba o rechaza y se guarda el resultado.

## 4. Visitor
`PlanBasico`, `PlanComplementario` y `PlanOdontologico` aceptan visitantes que calculan cotizacion, generan reportes y hacen auditoria.

Flujo aplicado:
1. El objeto plan mantiene su estructura.
2. El visitante ejecuta la operacion segun el tipo concreto.
3. Se reutiliza la misma logica para varias operaciones sin modificar las clases de plan.

## Rutas principales
- `/login`: ingreso de empleados.
- `/dashboard`: panel principal.
- `/autorizaciones/`: solicitud y listado de autorizaciones.
- `/afiliaciones/`: listado y cambio de estado de afiliaciones.
- `/citas/`: procesamiento de atenciones medicas con Template Method.
- `/planes/`: cotizacion, reporte y auditoria con Visitor.

## Credenciales de prueba
- Usuario: `admin` / Clave: `admin`
- Usuario: `medico` / Clave: `medico`
- Usuario: `auxiliar` / Clave: `auxiliar`

## Ejecucion
1. Instalar dependencias con `pip install -r requirements.txt`.
2. Ejecutar `python app.py` desde la carpeta `eps_app/`.
3. Abrir `http://127.0.0.1:5000/login`.
