from dataclasses import dataclass
from typing import Protocol


class PlanVisitor(Protocol):
    def visit_plan_basico(self, plan):
        ...

    def visit_plan_complementario(self, plan):
        ...

    def visit_plan_odontologico(self, plan):
        ...


@dataclass
class Plan:
    id: int | None
    nombre: str
    tipo: str
    tarifa_base: float
    cobertura: str

    def aceptar(self, visitor: PlanVisitor):
        raise NotImplementedError


@dataclass
class PlanBasico(Plan):
    def aceptar(self, visitor: PlanVisitor):
        return visitor.visit_plan_basico(self)


@dataclass
class PlanComplementario(Plan):
    servicios_extra: list[str] | None = None

    def aceptar(self, visitor: PlanVisitor):
        return visitor.visit_plan_complementario(self)


@dataclass
class PlanOdontologico(Plan):
    incluye_ortodoncia: bool = False

    def aceptar(self, visitor: PlanVisitor):
        return visitor.visit_plan_odontologico(self)