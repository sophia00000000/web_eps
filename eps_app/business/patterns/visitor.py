from dataclasses import dataclass
from datetime import date

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
    reviewer: str = "Auditor Demo"

    def _base_result(self, plan_name: str, audited: bool, issues: list[str] | None = None):
        return {
            "plan": plan_name,
            "auditoria": audited,
            "revisado_por": self.reviewer,
            "fecha_revision": date.today().isoformat(),
            "issues": issues or [],
            "observaciones": ("; ".join(issues) if issues else "Sin observaciones relevantes"),
        }

    def visit_plan_basico(self, plan: PlanBasico):
        issues = ["Cobertura limitada a consultas básicas", "Revisar exclusiones de laboratorio"]
        return self._base_result(plan.nombre, True, issues)

    def visit_plan_complementario(self, plan: PlanComplementario):
        # Complementario suele tener buena cobertura; solo observación menor
        issues = ["Verificar actualización de prima para servicios nuevos"]
        return self._base_result(plan.nombre, True, issues)

    def visit_plan_odontologico(self, plan: PlanOdontologico):
        issues = ["Cobertura de ortodoncia requiere estudio previo"]
        return self._base_result(plan.nombre, True, issues)