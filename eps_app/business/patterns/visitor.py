from dataclasses import dataclass

from data.models.plan import PlanBasico, PlanComplementario, PlanOdontologico


@dataclass
class VisitorCotizacion:
    factor: float = 1.2

    def visit_plan_basico(self, plan: PlanBasico):
        return {"plan": plan.nombre, "valor": plan.tarifa_base * self.factor}

    def visit_plan_complementario(self, plan: PlanComplementario):
        return {"plan": plan.nombre, "valor": plan.tarifa_base * 1.4}

    def visit_plan_odontologico(self, plan: PlanOdontologico):
        return {"plan": plan.nombre, "valor": plan.tarifa_base * 1.6}


@dataclass
class VisitorReporte:
    def visit_plan_basico(self, plan: PlanBasico):
        return f"Reporte de {plan.nombre}"

    def visit_plan_complementario(self, plan: PlanComplementario):
        return f"Reporte de {plan.nombre} con servicios extra"

    def visit_plan_odontologico(self, plan: PlanOdontologico):
        return f"Reporte de {plan.nombre} con ortodoncia"


@dataclass
class VisitorAuditoria:
    def visit_plan_basico(self, plan: PlanBasico):
        return {"plan": plan.nombre, "auditoria": True}

    def visit_plan_complementario(self, plan: PlanComplementario):
        return {"plan": plan.nombre, "auditoria": True}

    def visit_plan_odontologico(self, plan: PlanOdontologico):
        return {"plan": plan.nombre, "auditoria": True}