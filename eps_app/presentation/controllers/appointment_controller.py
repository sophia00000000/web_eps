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
    paciente_id = int(request.form["paciente_id"])
    medico = session.get("username", request.form["medico"])
    fecha = request.form["fecha"]
    tipo = request.form["tipo_atencion"]
    motivo = request.form.get("motivo_consulta")
    observaciones = request.form.get("observaciones")
    triage = request.form.get("triage")
    signos = request.form.get("signos_vitales")
    intervenciones = request.form.get("intervenciones")
    habitacion = request.form.get("habitacion")
    fecha_ingreso = request.form.get("fecha_ingreso")
    fecha_alta = request.form.get("fecha_alta")

    appointment_service.process_and_store(
        paciente_id,
        medico,
        fecha,
        tipo,
        motivo_consulta=motivo,
        observaciones=observaciones,
        triage=triage,
        signos_vitales=signos,
        intervenciones=intervenciones,
        habitacion=habitacion,
        fecha_ingreso=fecha_ingreso,
        fecha_alta=fecha_alta,
    )
    return redirect(url_for("appointment.index"))