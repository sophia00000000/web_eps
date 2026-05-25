from flask import Blueprint, redirect, render_template, request, session, url_for

from business.services.authorization_service import AuthorizationService
from presentation.controllers.auth_controller import login_required, role_required


authorization_bp = Blueprint("authorization", __name__)
authorization_service = AuthorizationService()


@authorization_bp.route("/")
@login_required
@role_required("admin", "medico", "auxiliar")
def index():
    authorizations = authorization_service.list_authorizations()
    return render_template(
        "autorizaciones/index.html",
        authorizations=authorizations,
        patients=authorization_service.list_patients(),
        services=authorization_service.list_services(),
        coverage_description_for_plan=authorization_service.coverage_description_for_plan,
    )


@authorization_bp.route("/procesar", methods=["POST"])
@login_required
@role_required("admin", "medico", "auxiliar")
def procesar():
    authorization_service.process_request(
        int(request.form["paciente_id"]),
        int(request.form["servicio_id"]),
        request.form.get("afiliacion_estado", "activa"),
        session.get("rol"),
    )
    return redirect(url_for("authorization.index"))