from dataclasses import dataclass
from datetime import date


@dataclass
class Affiliation:
    id: int | None
    paciente_id: int
    eps_nombre: str
    regimen: str
    estado: str
    fecha_afiliacion: date | None = None
    fecha_cancelacion: date | None = None