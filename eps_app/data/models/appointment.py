from dataclasses import dataclass


@dataclass
class Appointment:
    id: int | None
    paciente_id: int
    medico: str
    fecha: str
    tipo_atencion: str
    estado: str
    diagnostico: str | None = None
    factura_total: float = 0.0
    motivo_consulta: str | None = None
    observaciones: str | None = None
    triage: str | None = None
    signos_vitales: str | None = None
    intervenciones: str | None = None
    habitacion: str | None = None
    fecha_ingreso: str | None = None
    fecha_alta: str | None = None
    