from business.patterns.visitor import VisitorAuditoria, VisitorCotizacion, VisitorReporte
from data.daos.plan_dao import PlanDAO
from data.models.plan import PlanBasico, PlanComplementario, PlanOdontologico


class PlanService:
    def __init__(self):
        self.plan_dao = PlanDAO()

    def all_plans(self):
        return [
            PlanBasico(1, "Plan Basico", "basico", 50000, "general"),
            PlanComplementario(2, "Plan Complementario", "complementario", 90000, "amplia"),
            PlanOdontologico(3, "Plan Odontologico", "odontologico", 70000, "odontologia"),
        ]

    def list_db_plans(self):
        return self.plan_dao.list_all()

    def list_db_services(self):
        return self.plan_dao.list_services()

    def cotizar(self):
        visitor = VisitorCotizacion()
        return [plan.accept(visitor) for plan in self.all_plans()]

    def reportar(self):
        visitor = VisitorReporte()
        return [plan.accept(visitor) for plan in self.all_plans()]

    def auditar(self):
        visitor = VisitorAuditoria()
        return [plan.accept(visitor) for plan in self.all_plans()]