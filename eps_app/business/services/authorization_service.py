from datetime import date

from business.patterns.chain_of_responsibility import AuthorizationRequest, build_authorization_chain
from data.database import get_connection
from data.daos.authorization_dao import AuthorizationDAO


class AuthorizationService:
    def __init__(self):
        self.authorization_dao = AuthorizationDAO()

    def coverage_description_for_plan(self, plan_tipo: str) -> str:
        if plan_tipo == "basico":
            return "cubre consulta general y triage de urgencias"
        if plan_tipo == "complementario":
            return "cubre consulta general, urgencias y procedimientos ampliados"
        if plan_tipo == "odontologico":
            return "cubre endodoncia y procedimientos odontológicos"
        return "cobertura no definida"

    def _covered_services_for_patient(self, paciente_id: int) -> set[int]:
        connection = get_connection()
        row = connection.execute(
            """
            SELECT p.plan_id, pl.tipo
            FROM pacientes p
            JOIN planes pl ON pl.id = p.plan_id
            WHERE p.id = ?
            """,
            (paciente_id,),
        ).fetchone()
        if row is None:
            return set()

        plan_tipo = row["tipo"]
        if plan_tipo == "basico":
            return {1, 2}
        if plan_tipo == "complementario":
            return {1, 2, 3, 4, 5, 6}
        if plan_tipo == "odontologico":
            return {7}
        return set()

    def list_authorizations(self):
        return self.authorization_dao.list_all()

    def list_patients(self):
        connection = get_connection()
        return connection.execute(
            """
            SELECT p.id, p.nombre, p.documento, pl.nombre AS plan_nombre, pl.tipo AS plan_tipo
            FROM pacientes p
            LEFT JOIN planes pl ON p.plan_id = pl.id
            ORDER BY p.nombre
            """
        ).fetchall()

    def list_services(self):
        connection = get_connection()
        return connection.execute("SELECT id, nombre, tipo_servicio FROM servicios ORDER BY nombre").fetchall()

    def process_request(self, paciente_id: int, servicio_id: int, affiliation_status: str = "activa", user_role: str | None = None):
        request = AuthorizationRequest(paciente_id=paciente_id, servicio_id=servicio_id, fecha_solicitud=date.today())

        if user_role == "auxiliar":
            self.authorization_dao.create(
                paciente_id=request.paciente_id,
                servicio_id=request.servicio_id,
                estado="pendiente",
                nivel_aprobacion=0,
                fecha_solicitud=request.fecha_solicitud.isoformat(),
                observaciones="Pendiente por revision adicional",
            )
            request.estado = "pendiente"
            request.nivel_aprobacion = 0
            request.observaciones = "Pendiente por revision adicional"
            return request

        covered_services = self._covered_services_for_patient(paciente_id)
        chain = build_authorization_chain(affiliation_status, covered_services)
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