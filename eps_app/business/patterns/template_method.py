from abc import ABC, abstractmethod
from datetime import date
from typing import final


class AtencionMedicaTemplate(ABC):
    @final
    def procesarAtencion(self, paciente, medico):
        self.registrarPaciente(paciente)
        self.validarAfiliacion(paciente)
        self.asignarMedico(medico)
        self.realizarAtencion()
        self.generarDiagnostico()
        return self.generarFactura()

    def procesar_atencion(self, paciente, medico):
        return self.procesarAtencion(paciente, medico)

    def registrarPaciente(self, paciente):
        return paciente

    def registrar_paciente(self, paciente):
        return self.registrarPaciente(paciente)

    def validarAfiliacion(self, paciente):
        return paciente

    def validar_afiliacion(self, paciente):
        return self.validarAfiliacion(paciente)

    def asignarMedico(self, medico):
        return medico

    def asignar_medico(self, medico):
        return self.asignarMedico(medico)

    @abstractmethod
    def realizarAtencion(self):
        raise NotImplementedError

    def realizar_atencion(self):
        return self.realizarAtencion()

    @abstractmethod
    def generarDiagnostico(self):
        raise NotImplementedError

    def generar_diagnostico(self):
        return self.generarDiagnostico()

    def generarFactura(self):
        return {"fecha": date.today().isoformat(), "total": 0.0}

    def generar_factura(self):
        return self.generarFactura()


class CitaMedica(AtencionMedicaTemplate):
    def realizarAtencion(self):
        return "Consulta programada"

    def generarDiagnostico(self):
        return "Diagnostico de cita"


class UrgenciaMedica(AtencionMedicaTemplate):
    def clasificar_triage(self):
        return "prioridad inmediata"

    def realizarAtencion(self):
        return self.clasificar_triage()

    def generarDiagnostico(self):
        return "Diagnostico de urgencia"


class HospitalizacionMedica(AtencionMedicaTemplate):
    def asignar_habitacion(self):
        return "Habitacion asignada"

    def realizarAtencion(self):
        return self.asignar_habitacion()

    def generarDiagnostico(self):
        return "Diagnostico de hospitalizacion"