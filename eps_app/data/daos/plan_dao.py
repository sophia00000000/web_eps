from data.database import get_connection


class PlanDAO:
    def list_all(self):
        connection = get_connection()
        return connection.execute("SELECT * FROM planes").fetchall()

    def list_services(self):
        connection = get_connection()
        return connection.execute("SELECT * FROM servicios").fetchall()