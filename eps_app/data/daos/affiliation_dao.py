from data.database import get_connection
from data.models.affiliation import Affiliation


class AffiliationDAO:
    def list_all(self):
        connection = get_connection()
        rows = connection.execute(
            """
            SELECT a.*, p.nombre AS paciente_nombre, p.documento AS paciente_documento, pl.nombre AS plan_nombre
            FROM afiliaciones a
            JOIN pacientes p ON p.id = a.paciente_id
            LEFT JOIN planes pl ON pl.id = p.plan_id
            ORDER BY a.id DESC
            """
        ).fetchall()
        affiliations = []
        for row in rows:
            affiliation = Affiliation(
                row["id"],
                row["paciente_id"],
                row["eps_nombre"],
                row["regimen"],
                row["estado"],
                row["fecha_afiliacion"],
                row["fecha_cancelacion"],
            )
            affiliation.paciente_nombre = row["paciente_nombre"]
            affiliation.paciente_documento = row["paciente_documento"]
            affiliation.plan_nombre = row["plan_nombre"]
            affiliation.estado_anterior = row["estado_anterior"]
            affiliation.motivo_modificacion = row["motivo_modificacion"]
            affiliation.fecha_modificacion = row["fecha_modificacion"]
            affiliations.append(affiliation)
        return affiliations

    def find_by_id(self, affiliation_id: int):
        connection = get_connection()
        row = connection.execute("SELECT a.*, p.nombre AS paciente_nombre, p.documento AS paciente_documento, pl.nombre AS plan_nombre FROM afiliaciones a JOIN pacientes p ON p.id = a.paciente_id LEFT JOIN planes pl ON pl.id = p.plan_id WHERE a.id = ?", (affiliation_id,)).fetchone()
        if not row:
            return None
        affiliation = Affiliation(
            row["id"],
            row["paciente_id"],
            row["eps_nombre"],
            row["regimen"],
            row["estado"],
            row["fecha_afiliacion"],
            row["fecha_cancelacion"],
        )
        affiliation.paciente_nombre = row["paciente_nombre"]
        affiliation.paciente_documento = row["paciente_documento"]
        affiliation.plan_nombre = row["plan_nombre"]
        affiliation.estado_anterior = row["estado_anterior"]
        affiliation.motivo_modificacion = row["motivo_modificacion"]
        affiliation.fecha_modificacion = row["fecha_modificacion"]
        return affiliation

    def update_state(self, affiliation_id: int, estado: str, fecha_cancelacion=None, motivo_modificacion: str | None = None):
        connection = get_connection()
        connection.execute(
            """
            UPDATE afiliaciones
            SET estado = ?,
                estado_anterior = (SELECT estado FROM afiliaciones WHERE id = ?),
                fecha_cancelacion = COALESCE(?, fecha_cancelacion),
                motivo_modificacion = ?,
                fecha_modificacion = date('now')
            WHERE id = ?
            """,
            (estado, affiliation_id, fecha_cancelacion, motivo_modificacion, affiliation_id),
        )
        connection.execute(
            "UPDATE pacientes SET estado_afiliacion = ? WHERE id = (SELECT paciente_id FROM afiliaciones WHERE id = ?)",
            (estado, affiliation_id),
        )
        connection.commit()