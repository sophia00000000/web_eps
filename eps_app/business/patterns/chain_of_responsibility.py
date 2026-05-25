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

    def aprobar(self):
        self.estado = "aprobada"

    def rechazar(self, motivo: str):
        self.estado = "rechazada"
        self.observaciones = motivo

    def actualizarEstado(self, estado: str, observaciones: str = ""):
        self.estado = estado
        self.observaciones = observaciones


class Handler:
    def __init__(self):
        self._next: Optional[Handler] = None

    def set_next(self, handler):
        self._next = handler
        return handler

    def setSiguiente(self, handler):
        return self.set_next(handler)

    def process(self, authorization: AuthorizationRequest):
        if self._next:
            return self._next.process(authorization)
        return authorization

    def procesar(self, authorization: AuthorizationRequest):
        return self.process(authorization)


class DocumentValidator(Handler):
    def process(self, authorization: AuthorizationRequest):
        if not authorization.paciente_id:
            authorization.rechazar("Paciente sin identificacion valida")
            return authorization
        return super().process(authorization)


class AffiliationValidator(Handler):
    def __init__(self, affiliation_status: str = "activa"):
        super().__init__()
        self.affiliation_status = affiliation_status

    def process(self, authorization: AuthorizationRequest):
        if self.affiliation_status != "activa":
            authorization.rechazar("Afiliacion no activa")
            return authorization
        authorization.nivel_aprobacion = 1
        return super().process(authorization)


class CoverageValidator(Handler):
    def __init__(self, covered_services: Optional[set[int]] = None):
        super().__init__()
        self.covered_services = covered_services or set()

    def process(self, authorization: AuthorizationRequest):
        if authorization.servicio_id not in self.covered_services:
            authorization.rechazar("Servicio no cubierto")
            return authorization
        authorization.nivel_aprobacion = 2
        return super().process(authorization)


class SpecialistValidator(Handler):
    def __init__(self, required_level: int = 1):
        super().__init__()
        self.required_level = required_level

    def process(self, authorization: AuthorizationRequest):
        if self.required_level > 3:
            authorization.rechazar("Especialidad no valida")
            return authorization
        authorization.nivel_aprobacion = 3
        return super().process(authorization)


class FinalApprovalValidator(Handler):
    def process(self, authorization: AuthorizationRequest):
        authorization.aprobar()
        authorization.nivel_aprobacion = 4
        return authorization


def build_authorization_chain(affiliation_status: str = "activa", covered_services: Optional[set[int]] = None):
    first = DocumentValidator()
    second = first.setSiguiente(AffiliationValidator(affiliation_status))
    third = second.setSiguiente(CoverageValidator(covered_services))
    fourth = third.setSiguiente(SpecialistValidator())
    fourth.setSiguiente(FinalApprovalValidator())
    return first


Autorizacion = AuthorizationRequest
HandlerAutorizacion = Handler
ValidadorDocumentos = DocumentValidator
ValidadorAfiliacion = AffiliationValidator
ValidadorCobertura = CoverageValidator
ValidadorEspecialista = SpecialistValidator
ValidadorAuth = FinalApprovalValidator