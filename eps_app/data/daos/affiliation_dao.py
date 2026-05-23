from data.database import get_connection
from data.models.affiliation import Affiliation


class AffiliationDAO:
    def list_all(self):
        connection = get_connection()
        rows = connection.execute(
            """
            SELECT a.*, p.nombre AS paciente_nombre, p.documento AS paciente_documento
            FROM afiliaciones a
            JOIN pacientes p ON p.id = a.paciente_id
            ORDER BY a.id DESC
            """
        ).fetchall()
        return [
            (lambda affiliation: (
                setattr(affiliation, "paciente_nombre", row["paciente_nombre"]),
                setattr(affiliation, "paciente_documento", row["paciente_documento"]),
                affiliation,
            )[2])(
            Affiliation(
                row["id"],
                row["paciente_id"],
                row["eps_nombre"],
                row["regimen"],
                row["estado"],
                row["fecha_afiliacion"],
                row["fecha_cancelacion"],
            )
            )
            for row in rows
        ]

    def find_by_id(self, affiliation_id: int):
        connection = get_connection()
        row = connection.execute("SELECT * FROM afiliaciones WHERE id = ?", (affiliation_id,)).fetchone()
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
        return affiliation

    def update_state(self, affiliation_id: int, estado: str, fecha_cancelacion=None):
        connection = get_connection()
        connection.execute(
            "UPDATE afiliaciones SET estado = ?, fecha_cancelacion = COALESCE(?, fecha_cancelacion) WHERE id = ?",
            (estado, fecha_cancelacion, affiliation_id),
        )
        connection.execute(
            "UPDATE pacientes SET estado_afiliacion = ? WHERE id = (SELECT paciente_id FROM afiliaciones WHERE id = ?)",
            (estado, affiliation_id),
        )
        connection.commit()