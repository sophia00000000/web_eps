from flask import Blueprint, redirect, render_template, request, session, url_for

from business.services.appointment_service import AppointmentService
from presentation.controllers.auth_controller import login_required, role_required


appointment_bp = Blueprint("appointment", __name__)
appointment_service = AppointmentService()


@appointment_bp.route("/")
@login_required
@role_required("medico", "admin")
def index():
    appointments = appointment_service.list_appointments()
    return render_template(
        "citas/index.html",
        appointments=appointments,
        patients=appointment_service.list_patients(),
        medico_actual=session.get("username"),
        puede_procesar=session.get("rol") == "medico",
    )


@appointment_bp.route("/procesar", methods=["POST"])
@login_required
@role_required("medico")
def procesar():
    appointment_service.process_and_store(
        int(request.form["paciente_id"]),
        session.get("username", request.form["medico"]),
        request.form["fecha"],
        request.form["tipo_atencion"],
    )
    return redirect(url_for("appointment.index"))