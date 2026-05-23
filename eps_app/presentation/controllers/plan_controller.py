from flask import Blueprint, render_template

from business.services.plan_service import PlanService
from presentation.controllers.auth_controller import login_required, role_required


plan_bp = Blueprint("plan", __name__)
plan_service = PlanService()


@plan_bp.route("/")
@login_required
@role_required("admin")
def index():
    return render_template(
        "planes/index.html",
        cotizaciones=plan_service.cotizar(),
        reportes=plan_service.reportar(),
        auditorias=plan_service.auditar(),
        db_plans=plan_service.list_db_plans(),
        db_services=plan_service.list_db_services(),
    )