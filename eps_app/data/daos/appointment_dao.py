from data.database import get_connection
from data.models.appointment import Appointment


class AppointmentDAO:
    def list_all(self):
        connection = get_connection()
        rows = connection.execute(
            """
            SELECT c.*, p.nombre AS paciente_nombre, p.documento AS paciente_documento
            FROM citas c
            JOIN pacientes p ON p.id = c.paciente_id
            ORDER BY c.fecha DESC, c.id DESC
            """
        ).fetchall()
        return [
            (lambda appointment: (
                setattr(appointment, "paciente_nombre", row["paciente_nombre"]),
                setattr(appointment, "paciente_documento", row["paciente_documento"]),
                appointment,
            )[2])(
            Appointment(
                row["id"],
                row["paciente_id"],
                row["medico"],
                row["fecha"],
                row["tipo_atencion"],
                row["estado"],
                row["diagnostico"],
                row["factura_total"],
                row["motivo_consulta"],
                row["observaciones"],
                row["triage"],
                row["signos_vitales"],
                row["intervenciones"],
                row["habitacion"],
                row["fecha_ingreso"],
                row["fecha_alta"],
            )
            )
            for row in rows
        ]

    def find_by_id(self, appointment_id: int):
        connection = get_connection()
        row = connection.execute(
            """
            SELECT c.*, p.nombre AS paciente_nombre, p.documento AS paciente_documento
            FROM citas c
            JOIN pacientes p ON p.id = c.paciente_id
            WHERE c.id = ?
            """,
            (appointment_id,),
        ).fetchone()
        if not row:
            return None
        appointment = Appointment(
            row["id"],
            row["paciente_id"],
            row["medico"],
            row["fecha"],
            row["tipo_atencion"],
            row["estado"],
            row["diagnostico"],
            row["factura_total"],
            row["motivo_consulta"],
            row["observaciones"],
            row["triage"],
            row["signos_vitales"],
            row["intervenciones"],
            row["habitacion"],
            row["fecha_ingreso"],
            row["fecha_alta"],
        )
        setattr(appointment, "paciente_nombre", row["paciente_nombre"])
        setattr(appointment, "paciente_documento", row["paciente_documento"])
        return appointment

    def list_scheduled_for_medico(self, medico_username: str):
        connection = get_connection()
        rows = connection.execute(
            """
            SELECT c.*, p.nombre AS paciente_nombre, p.documento AS paciente_documento
            FROM citas c
            JOIN pacientes p ON p.id = c.paciente_id
            WHERE c.medico = ? AND c.estado = 'programada' AND c.tipo_atencion = 'cita'
            ORDER BY c.fecha ASC, c.id ASC
            """,
            (medico_username,),
        ).fetchall()
        result = []
        for row in rows:
            appointment = Appointment(
                row["id"],
                row["paciente_id"],
                row["medico"],
                row["fecha"],
                row["tipo_atencion"],
                row["estado"],
                row["diagnostico"],
                row["factura_total"],
                row["motivo_consulta"],
                row["observaciones"],
                row["triage"],
                row["signos_vitales"],
                row["intervenciones"],
                row["habitacion"],
                row["fecha_ingreso"],
                row["fecha_alta"],
            )
            setattr(appointment, "paciente_nombre", row["paciente_nombre"])
            setattr(appointment, "paciente_documento", row["paciente_documento"])
            result.append(appointment)
        return result

    def update_to_attended(self, appointment_id: int, diagnostico: str, factura_total: float, motivo_consulta: str | None = None, observaciones: str | None = None, triage: str | None = None, signos_vitales: str | None = None, intervenciones: str | None = None, habitacion: str | None = None, fecha_ingreso: str | None = None, fecha_alta: str | None = None):
        connection = get_connection()
        connection.execute(
            """
            UPDATE citas
            SET estado = 'atendida', diagnostico = ?, factura_total = ?, motivo_consulta = COALESCE(?, motivo_consulta), observaciones = COALESCE(?, observaciones), triage = COALESCE(?, triage), signos_vitales = COALESCE(?, signos_vitales), intervenciones = COALESCE(?, intervenciones), habitacion = COALESCE(?, habitacion), fecha_ingreso = COALESCE(?, fecha_ingreso), fecha_alta = COALESCE(?, fecha_alta)
            WHERE id = ?
            """,
            (diagnostico, factura_total, motivo_consulta, observaciones, triage, signos_vitales, intervenciones, habitacion, fecha_ingreso, fecha_alta, appointment_id),
        )
        connection.commit()
    

    def create(self, paciente_id: int, medico: str, fecha: str, tipo_atencion: str, estado: str, diagnostico: str, factura_total: float, motivo_consulta: str | None = None, observaciones: str | None = None, triage: str | None = None, signos_vitales: str | None = None, intervenciones: str | None = None, habitacion: str | None = None, fecha_ingreso: str | None = None, fecha_alta: str | None = None):
        connection = get_connection()
        cursor = connection.execute(
            """
            INSERT INTO citas (paciente_id, medico, fecha, tipo_atencion, estado, motivo_consulta, diagnostico, observaciones, triage, signos_vitales, intervenciones, habitacion, fecha_ingreso, fecha_alta, factura_total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (paciente_id, medico, fecha, tipo_atencion, estado, motivo_consulta, diagnostico, observaciones, triage, signos_vitales, intervenciones, habitacion, fecha_ingreso, fecha_alta, factura_total),
        )
        connection.commit()
        return cursor.lastrowid