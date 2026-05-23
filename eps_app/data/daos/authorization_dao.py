from data.database import get_connection


class AuthorizationDAO:
    def list_all(self):
        connection = get_connection()
        return connection.execute(
            """
            SELECT a.*, p.nombre AS paciente_nombre, s.nombre AS servicio_nombre
            FROM autorizaciones a
            JOIN pacientes p ON p.id = a.paciente_id
            JOIN servicios s ON s.id = a.servicio_id
            ORDER BY a.id DESC
            """
        ).fetchall()

    def create(self, paciente_id: int, servicio_id: int, estado: str, nivel_aprobacion: int, fecha_solicitud: str, observaciones: str):
        connection = get_connection()
        cursor = connection.execute(
            """
            INSERT INTO autorizaciones (paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones),
        )
        connection.commit()
        return cursor.lastrowid