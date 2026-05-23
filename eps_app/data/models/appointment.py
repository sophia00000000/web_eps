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