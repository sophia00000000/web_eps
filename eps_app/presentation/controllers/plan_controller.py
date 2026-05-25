from flask import Blueprint, render_template, request

from business.services.plan_service import PlanService
from presentation.controllers.auth_controller import login_required, role_required


plan_bp = Blueprint("plan", __name__)
plan_service = PlanService()


@plan_bp.route("/")
@login_required
@role_required("admin")
def index():
    return render_page()


@plan_bp.route("/accion", methods=["POST"])
@login_required
@role_required("admin")
def accion():
    return render_page(request.form.get("accion", "cotizar"))


def render_page(accion_seleccionada: str | None = None):
    cotizaciones = plan_service.cotizar() if accion_seleccionada in (None, "cotizar") else []
    reportes = plan_service.reportar() if accion_seleccionada in (None, "reportar") else []
    auditorias = plan_service.auditar() if accion_seleccionada in (None, "auditar") else []
    return render_template(
        "planes/index.html",
        accion_seleccionada=accion_seleccionada,
        cotizaciones=cotizaciones,
        reportes=reportes,
        auditorias=auditorias,
        db_plans=plan_service.list_db_plans(),
        db_services=plan_service.list_db_services(),
    )