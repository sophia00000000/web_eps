from datetime import date

from business.patterns.chain_of_responsibility import AuthorizationRequest, build_authorization_chain
from data.database import get_connection
from data.daos.authorization_dao import AuthorizationDAO


class AuthorizationService:
    def __init__(self):
        self.authorization_dao = AuthorizationDAO()

    def list_authorizations(self):
        return self.authorization_dao.list_all()

    def list_patients(self):
        connection = get_connection()
        return connection.execute("SELECT id, nombre, documento FROM pacientes ORDER BY nombre").fetchall()

    def list_services(self):
        connection = get_connection()
        return connection.execute("SELECT id, nombre, tipo_servicio FROM servicios ORDER BY nombre").fetchall()

    def process_request(self, paciente_id: int, servicio_id: int, affiliation_status: str = "activa"):
        request = AuthorizationRequest(paciente_id=paciente_id, servicio_id=servicio_id, fecha_solicitud=date.today())
        chain = build_authorization_chain(affiliation_status)
        result = chain.process(request)
        self.authorization_dao.create(
            paciente_id=result.paciente_id,
            servicio_id=result.servicio_id,
            estado=result.estado,
            nivel_aprobacion=result.nivel_aprobacion,
            fecha_solicitud=result.fecha_solicitud.isoformat(),
            observaciones=result.observaciones,
        )
        return result