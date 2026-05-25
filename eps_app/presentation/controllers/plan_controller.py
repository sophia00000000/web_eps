from flask import Blueprint, render_template, request

from business.services.plan_service import PlanService
from presentation.controllers.auth_controller import login_required, role_required


plan_bp = Blueprint("plan", __name__)
plan_service = PlanService()


@plan_bp.route("/")
@login_required
@role_required("admin", "auxiliar")
def index():
    return render_page()


@plan_bp.route("/accion", methods=["POST"])
@login_required
@role_required("admin")
def accion():
    return render_page(request.form.get("accion", "cotizar"))


def render_page(accion_seleccionada: str | None = None):
    resultado_titulo = None
    resultado_descripcion = None
    resultado_items = []

    if accion_seleccionada == "cotizar":
        resultado_titulo = "Cotización de planes"
        resultado_descripcion = "Visitor calcula el valor estimado de cada plan."
        resultado_items = plan_service.cotizar()
    elif accion_seleccionada == "reportar":
        resultado_titulo = "Reporte de planes"
        resultado_descripcion = "Visitor genera un texto descriptivo por cada plan."
        resultado_items = plan_service.reportar()
    elif accion_seleccionada == "auditar":
        resultado_titulo = "Auditoría de planes"
        resultado_descripcion = "Visitor marca cada plan como revisado para la demo educativa."
        resultado_items = plan_service.auditar()

    return render_template(
        "planes/index.html",
        accion_seleccionada=accion_seleccionada,
        resultado_titulo=resultado_titulo,
        resultado_descripcion=resultado_descripcion,
        resultado_items=resultado_items,
        db_plans=plan_service.list_db_plans(),
        db_services=plan_service.list_db_services(),
    )