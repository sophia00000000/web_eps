from abc import ABC, abstractmethod
from datetime import date
from typing import final


class AtencionMedicaTemplate(ABC):
    @final
    def procesar_atencion(self, paciente, medico):
        self.registrar_paciente(paciente)
        self.validar_afiliacion(paciente)
        self.asignar_medico(medico)
        self.realizar_atencion()
        self.generar_diagnostico()
        return self.generar_factura()

    def registrar_paciente(self, paciente):
        return paciente

    def validar_afiliacion(self, paciente):
        return paciente

    def asignar_medico(self, medico):
        return medico

    @abstractmethod
    def realizar_atencion(self):
        raise NotImplementedError

    @abstractmethod
    def generar_diagnostico(self):
        raise NotImplementedError

    def generar_factura(self):
        return {"fecha": date.today().isoformat(), "total": 0.0}


class CitaMedica(AtencionMedicaTemplate):
    def realizar_atencion(self):
        return "Consulta programada"

    def generar_diagnostico(self):
        return "Diagnostico de cita"


class UrgenciaMedica(AtencionMedicaTemplate):
    def clasificar_triage(self):
        return "prioridad inmediata"

    def realizar_atencion(self):
        return self.clasificar_triage()

    def generar_diagnostico(self):
        return "Diagnostico de urgencia"


class HospitalizacionMedica(AtencionMedicaTemplate):
    def asignar_habitacion(self):
        return "Habitacion asignada"

    def realizar_atencion(self):
        return self.asignar_habitacion()

    def generar_diagnostico(self):
        return "Diagnostico de hospitalizacion"