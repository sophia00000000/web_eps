from flask import Blueprint, redirect, render_template, request, session, url_for

from business.services.appointment_service import AppointmentService
from presentation.controllers.auth_controller import login_required, role_required


appointment_bp = Blueprint("appointment", __name__)
appointment_service = AppointmentService()


@appointment_bp.route("/")
@login_required
@role_required("medico", "admin", "auxiliar")
def index():
    appointments = appointment_service.list_appointments()
    scheduled_appointments = []
    if session.get("rol") == "medico":
        scheduled_appointments = appointment_service.list_scheduled_for_medico(session.get("username"))
    return render_template(
        "citas/index.html",
        appointments=appointments,
        patients=appointment_service.list_patients(),
        medicos=appointment_service.list_medicos(),
        medico_actual=session.get("username"),
        puede_procesar=session.get("rol") == "medico",
        puede_agendar=session.get("rol") in ("auxiliar", "admin"),
        scheduled_appointments=scheduled_appointments,
    )


@appointment_bp.route("/agendar", methods=["POST"])
@login_required
@role_required("auxiliar", "admin")
def agendar():
    appointment_service.schedule_appointment(
        int(request.form["paciente_id"]),
        request.form["medico"],
        request.form["fecha"],
        request.form.get("tipo_atencion", "cita"),
    )
    return redirect(url_for("appointment.index"))


@appointment_bp.route("/procesar", methods=["POST"])
@login_required
@role_required("medico")
def procesar():
    medico = session.get("username", request.form["medico"])
    tipo = request.form["tipo_atencion"]
    cita_id = request.form.get("cita_id")
    fecha = request.form.get("fecha") or request.form.get("fecha_directa")
    motivo = request.form.get("motivo_consulta")
    observaciones = request.form.get("observaciones")
    triage = request.form.get("triage")
    signos = request.form.get("signos_vitales")
    intervenciones = request.form.get("intervenciones")
    habitacion = request.form.get("habitacion")
    fecha_ingreso = request.form.get("fecha_ingreso")
    fecha_alta = request.form.get("fecha_alta")

    if tipo == "cita":
        cita = appointment_service.appointment_dao.find_by_id(int(cita_id)) if cita_id else None
        if cita is None:
            return redirect(url_for("appointment.index"))
        paciente_id = cita.paciente_id
        fecha = cita.fecha
    else:
        paciente_id = int(request.form["paciente_id"])

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
        cita_id=int(cita_id) if cita_id else None,
    )
    return redirect(url_for("appointment.index"))