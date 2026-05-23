from business.patterns.template_method import CitaMedica, HospitalizacionMedica, UrgenciaMedica
from data.database import get_connection
from data.daos.appointment_dao import AppointmentDAO


class AppointmentService:
    def __init__(self):
        self.appointment_dao = AppointmentDAO()

    def get_strategy(self, tipo_atencion: str):
        if tipo_atencion == "urgencia":
            return UrgenciaMedica()
        if tipo_atencion == "hospitalizacion":
            return HospitalizacionMedica()
        return CitaMedica()

    def list_appointments(self):
        return self.appointment_dao.list_all()

    def list_patients(self):
        connection = get_connection()
        return connection.execute("SELECT id, nombre, documento FROM pacientes ORDER BY nombre").fetchall()

    def list_medicos(self):
        connection = get_connection()
        return connection.execute(
            "SELECT id, username, rol FROM usuarios WHERE rol IN ('medico', 'admin') AND activo = 1 ORDER BY username"
        ).fetchall()

    def process_and_store(self, paciente_id: int, medico: str, fecha: str, tipo_atencion: str):
        strategy = self.get_strategy(tipo_atencion)
        factura = strategy.procesar_atencion(f"Paciente {paciente_id}", medico)
        diagnostico = strategy.generar_diagnostico()
        appointment_id = self.appointment_dao.create(
            paciente_id=paciente_id,
            medico=medico,
            fecha=fecha,
            tipo_atencion=tipo_atencion,
            estado="atendida",
            diagnostico=diagnostico,
            factura_total=float(factura["total"]),
        )
        return appointment_id, diagnostico, factura