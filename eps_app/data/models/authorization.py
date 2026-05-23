from dataclasses import dataclass
from datetime import date


@dataclass
class Authorization:
    id: int | None
    paciente_id: int
    servicio_id: int
    estado: str
    nivel_aprobacion: int
    fecha_solicitud: date
    observaciones: str = ""