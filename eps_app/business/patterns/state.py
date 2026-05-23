from abc import ABC, abstractmethod
from datetime import date


class EstadoAfiliacion(ABC):
    @abstractmethod
    def activar(self, contexto):
        raise NotImplementedError

    @abstractmethod
    def suspender(self, contexto):
        raise NotImplementedError

    @abstractmethod
    def cancelar(self, contexto):
        raise NotImplementedError

    @abstractmethod
    def validar_servicios(self) -> bool:
        raise NotImplementedError


class AfiliacionPendiente(EstadoAfiliacion):
    def activar(self, contexto):
        contexto.set_estado(AfiliacionActiva())

    def suspender(self, contexto):
        contexto.set_estado(AfiliacionSuspendida())

    def cancelar(self, contexto):
        contexto.fecha_cancelacion = date.today()
        contexto.set_estado(AfiliacionCancelada())

    def validar_servicios(self) -> bool:
        return False


class AfiliacionActiva(EstadoAfiliacion):
    def activar(self, contexto):
        contexto.set_estado(self)

    def suspender(self, contexto):
        contexto.set_estado(AfiliacionSuspendida())

    def cancelar(self, contexto):
        contexto.fecha_cancelacion = date.today()
        contexto.set_estado(AfiliacionCancelada())

    def validar_servicios(self) -> bool:
        return True


class AfiliacionSuspendida(EstadoAfiliacion):
    def activar(self, contexto):
        contexto.set_estado(AfiliacionActiva())

    def suspender(self, contexto):
        contexto.set_estado(self)

    def cancelar(self, contexto):
        contexto.fecha_cancelacion = date.today()
        contexto.set_estado(AfiliacionCancelada())

    def validar_servicios(self) -> bool:
        return False


class AfiliacionCancelada(EstadoAfiliacion):
    def activar(self, contexto):
        contexto.set_estado(AfiliacionActiva())

    def suspender(self, contexto):
        contexto.set_estado(AfiliacionSuspendida())

    def cancelar(self, contexto):
        contexto.fecha_cancelacion = date.today()
        contexto.set_estado(self)

    def validar_servicios(self) -> bool:
        return False


class AfiliacionContexto:
    def __init__(self, estado=None):
        self.estado = estado or AfiliacionPendiente()
        self.fecha_cancelacion = None

    def set_estado(self, estado):
        self.estado = estado

    def activar(self):
        self.estado.activar(self)

    def suspender(self):
        self.estado.suspender(self)

    def cancelar(self):
        self.estado.cancelar(self)

    def validar_servicios(self) -> bool:
        return self.estado.validar_servicios()