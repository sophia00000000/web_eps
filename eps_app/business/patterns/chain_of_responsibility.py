from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class AuthorizationRequest:
    paciente_id: int
    servicio_id: int
    estado: str = "pendiente"
    nivel_aprobacion: int = 0
    fecha_solicitud: date = date.today()
    observaciones: str = ""


class Handler:
    def __init__(self):
        self._next: Optional[Handler] = None

    def set_next(self, handler):
        self._next = handler
        return handler

    def process(self, authorization: AuthorizationRequest):
        if self._next:
            return self._next.process(authorization)
        return authorization


class DocumentValidator(Handler):
    def process(self, authorization: AuthorizationRequest):
        if not authorization.paciente_id:
            authorization.estado = "rechazada"
            authorization.observaciones = "Paciente sin identificacion valida"
            return authorization
        return super().process(authorization)


class AffiliationValidator(Handler):
    def __init__(self, affiliation_status: str = "activa"):
        super().__init__()
        self.affiliation_status = affiliation_status

    def process(self, authorization: AuthorizationRequest):
        if self.affiliation_status != "activa":
            authorization.estado = "rechazada"
            authorization.observaciones = "Afiliacion no activa"
            return authorization
        authorization.nivel_aprobacion = 1
        return super().process(authorization)


class CoverageValidator(Handler):
    def __init__(self, covered_services: Optional[set[int]] = None):
        super().__init__()
        self.covered_services = covered_services or set()

    def process(self, authorization: AuthorizationRequest):
        if authorization.servicio_id not in self.covered_services:
            authorization.estado = "rechazada"
            authorization.observaciones = "Servicio no cubierto"
            return authorization
        authorization.nivel_aprobacion = 2
        return super().process(authorization)


class SpecialistValidator(Handler):
    def __init__(self, required_level: int = 1):
        super().__init__()
        self.required_level = required_level

    def process(self, authorization: AuthorizationRequest):
        if self.required_level > 3:
            authorization.estado = "rechazada"
            authorization.observaciones = "Especialidad no valida"
            return authorization
        authorization.nivel_aprobacion = 3
        return super().process(authorization)


class FinalApprovalValidator(Handler):
    def process(self, authorization: AuthorizationRequest):
        authorization.estado = "aprobada"
        authorization.nivel_aprobacion = 4
        return authorization


def build_authorization_chain(affiliation_status: str = "activa", covered_services: Optional[set[int]] = None):
    first = DocumentValidator()
    second = first.set_next(AffiliationValidator(affiliation_status))
    third = second.set_next(CoverageValidator(covered_services))
    fourth = third.set_next(SpecialistValidator())
    fourth.set_next(FinalApprovalValidator())
    return first