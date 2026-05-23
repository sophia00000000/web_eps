from datetime import date

from business.patterns.state import AfiliacionActiva, AfiliacionCancelada, AfiliacionContexto, AfiliacionPendiente, AfiliacionSuspendida
from data.daos.affiliation_dao import AffiliationDAO


class AffiliationService:
    def __init__(self):
        self.affiliation_dao = AffiliationDAO()

    def create_context(self, estado_actual: str = "pendiente"):
        if estado_actual == "activa":
            return AfiliacionContexto(AfiliacionActiva())
        if estado_actual == "suspendida":
            return AfiliacionContexto(AfiliacionSuspendida())
        if estado_actual == "cancelada":
            return AfiliacionContexto(AfiliacionCancelada())
        return AfiliacionContexto(AfiliacionPendiente())

    def list_affiliations(self):
        return self.affiliation_dao.list_all()

    def change_state(self, affiliation_id: int, action: str):
        affiliation = self.affiliation_dao.find_by_id(affiliation_id)
        if not affiliation:
            return None
        context = self.create_context(affiliation.estado)
        if action == "activar":
            context.activar()
        elif action == "suspender":
            context.suspender()
        elif action == "cancelar":
            context.cancelar()
        else:
            return context
        self.affiliation_dao.update_state(
            affiliation_id,
            context.estado.__class__.__name__.replace("Afiliacion", "").lower(),
            context.fecha_cancelacion.isoformat() if context.fecha_cancelacion else None,
        )
        return context

    def activar(self, contexto: AfiliacionContexto):
        contexto.activar()
        return contexto

    def cancelar(self, contexto: AfiliacionContexto):
        contexto.cancelar()
        return contexto