import sqlite3
from pathlib import Path

from flask import current_app, g


def get_connection():
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


def close_connection(_error=None):
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db():
    connection = sqlite3.connect(current_app.config["DATABASE"])
    cursor = connection.cursor()
    # Para el demo recreamos las tablas y cargamos semillas deterministas
    cursor.executescript(
        """
        DROP TABLE IF EXISTS autorizaciones;
        DROP TABLE IF EXISTS citas;
        DROP TABLE IF EXISTS afiliaciones;
        DROP TABLE IF EXISTS pacientes;
        DROP TABLE IF EXISTS servicios;
        DROP TABLE IF EXISTS planes;
        DROP TABLE IF EXISTS usuarios;

        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE planes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            tarifa_base REAL NOT NULL,
            cobertura TEXT NOT NULL,
            incluye_ortodoncia INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            documento TEXT UNIQUE NOT NULL,
            direccion TEXT,
            telefono TEXT,
            email TEXT,
            estado_afiliacion TEXT NOT NULL DEFAULT 'pendiente',
            plan_id INTEGER,
            FOREIGN KEY(plan_id) REFERENCES planes(id)
        );

        CREATE TABLE afiliaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            eps_nombre TEXT NOT NULL,
            regimen TEXT NOT NULL,
            estado TEXT NOT NULL,
            fecha_afiliacion TEXT,
            fecha_cancelacion TEXT,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
        );

        CREATE TABLE servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_servicio TEXT NOT NULL,
            tarifa_base REAL NOT NULL,
            requiere_especialidad TEXT,
            nivel_complejidad INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE autorizaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            servicio_id INTEGER NOT NULL,
            estado TEXT NOT NULL,
            nivel_aprobacion INTEGER NOT NULL DEFAULT 0,
            fecha_solicitud TEXT NOT NULL,
            observaciones TEXT,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id),
            FOREIGN KEY(servicio_id) REFERENCES servicios(id)
        );

        CREATE TABLE citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            medico TEXT NOT NULL,
            fecha TEXT NOT NULL,
            tipo_atencion TEXT NOT NULL,
            estado TEXT NOT NULL,
            diagnostico TEXT,
            factura_total REAL NOT NULL DEFAULT 0,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
        );
        """
    )

    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (id, username, password, rol, activo) VALUES (1, 'admin', 'admin', 'admin', 1)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (id, username, password, rol, activo) VALUES (2, 'medico', 'medico', 'medico', 1)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (id, username, password, rol, activo) VALUES (3, 'auxiliar', 'auxiliar', 'auxiliar', 1)"
    )
    # Planes
    cursor.execute(
        "INSERT OR IGNORE INTO planes (id, nombre, tipo, tarifa_base, cobertura, incluye_ortodoncia) VALUES (1, 'Plan Basico', 'basico', 50000, 'general', 0)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO planes (id, nombre, tipo, tarifa_base, cobertura, incluye_ortodoncia) VALUES (2, 'Plan Premium', 'complementario', 120000, 'amplia', 1)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO planes (id, nombre, tipo, tarifa_base, cobertura, incluye_ortodoncia) VALUES (3, 'Plan Odontologico', 'odontologico', 80000, 'odontologia', 1)"
    )

    # Pacientes de ejemplo (cada uno asignado a un plan para poder evaluar autorizaciones)
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, estado_afiliacion, plan_id) VALUES (1, 'Paciente Demo', '1001', 'activa', 1)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion, plan_id) VALUES (2, 'Mariana Gomez', '1002', '3005551002', 'mariana@example.com', 'activa', 2)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion, plan_id) VALUES (3, 'Carlos Perez', '1003', '3005551003', 'carlos@example.com', 'suspendida', 1)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion, plan_id) VALUES (4, 'Laura Ruiz', '1004', '3005551004', 'laura@example.com', 'pendiente', 2)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion, plan_id) VALUES (5, 'Ana Torres', '1005', '3005551005', 'ana@example.com', 'activa', 1)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion, plan_id) VALUES (6, 'Jorge Martinez', '1006', '3005551006', 'jorge@example.com', 'activa', 2)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion, plan_id) VALUES (7, 'Sofia Alvarez', '1007', '3005551007', 'sofia@example.com', 'activa', 3)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion, plan_id) VALUES (8, 'Miguel Sanchez', '1008', '3005551008', 'miguel@example.com', 'pendiente', 2)"
    )

    # Afiliaciones para los pacientes de ejemplo
    cursor.execute(
        "INSERT OR IGNORE INTO afiliaciones (id, paciente_id, eps_nombre, regimen, estado, fecha_afiliacion) VALUES (1, 1, 'EPS Demo', 'contributivo', 'activa', date('now'))"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO afiliaciones (id, paciente_id, eps_nombre, regimen, estado, fecha_afiliacion) VALUES (2, 2, 'EPS Demo', 'subsidiado', 'activa', date('now', '-15 day'))"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO afiliaciones (id, paciente_id, eps_nombre, regimen, estado, fecha_afiliacion, fecha_cancelacion) VALUES (3, 3, 'EPS Demo', 'contributivo', 'suspendida', date('now', '-30 day'), NULL)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO afiliaciones (id, paciente_id, eps_nombre, regimen, estado, fecha_afiliacion, fecha_cancelacion) VALUES (4, 4, 'EPS Demo', 'subsidiado', 'pendiente', date('now', '-2 day'), NULL)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO afiliaciones (id, paciente_id, eps_nombre, regimen, estado, fecha_afiliacion) VALUES (5, 5, 'EPS Demo', 'contributivo', 'activa', date('now', '-3 day'))"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO afiliaciones (id, paciente_id, eps_nombre, regimen, estado, fecha_afiliacion) VALUES (6, 6, 'EPS Demo', 'contributivo', 'activa', date('now', '-10 day'))"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO afiliaciones (id, paciente_id, eps_nombre, regimen, estado, fecha_afiliacion) VALUES (7, 7, 'EPS Demo', 'subsidiado', 'activa', date('now', '-20 day'))"
    )

    # Servicios / procedimientos
    cursor.execute(
        "INSERT OR IGNORE INTO servicios (id, nombre, tipo_servicio, tarifa_base, requiere_especialidad, nivel_complejidad) VALUES (1, 'Consulta General', 'consulta', 20000, 'medicina general', 1)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO servicios (id, nombre, tipo_servicio, tarifa_base, requiere_especialidad, nivel_complejidad) VALUES (2, 'Triage Urgencias', 'urgencia', 45000, 'urgencias', 3)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO servicios (id, nombre, tipo_servicio, tarifa_base, requiere_especialidad, nivel_complejidad) VALUES (3, 'Examen de Laboratorio', 'examen', 35000, 'laboratorio', 2)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO servicios (id, nombre, tipo_servicio, tarifa_base, requiere_especialidad, nivel_complejidad) VALUES (4, 'Consulta Especializada', 'consulta', 60000, 'medicina interna', 3)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO servicios (id, nombre, tipo_servicio, tarifa_base, requiere_especialidad, nivel_complejidad) VALUES (5, 'Cirugia Menor', 'procedimiento', 200000, 'cirugia general', 4)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO servicios (id, nombre, tipo_servicio, tarifa_base, requiere_especialidad, nivel_complejidad) VALUES (6, 'Ortopedia', 'procedimiento', 150000, 'ortopedia', 4)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO servicios (id, nombre, tipo_servicio, tarifa_base, requiere_especialidad, nivel_complejidad) VALUES (7, 'Endodoncia', 'procedimiento', 90000, 'odontologia', 3)"
    )

    # Autorizaciones de ejemplo para evaluar distintas rutas del Chain of Responsibility
    cursor.execute(
        "INSERT OR IGNORE INTO autorizaciones (id, paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones) VALUES (1, 1, 1, 'aprobada', 4, date('now', '-3 day'), 'Aprobada sin novedades')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO autorizaciones (id, paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones) VALUES (2, 2, 3, 'aprobada', 4, date('now', '-2 day'), 'Cobertura validada')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO autorizaciones (id, paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones) VALUES (3, 3, 4, 'rechazada', 1, date('now', '-1 day'), 'Afiliacion suspendida')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO autorizaciones (id, paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones) VALUES (4, 5, 5, 'pendiente', 0, date('now'), 'Solicitud para cirugia menor')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO autorizaciones (id, paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones) VALUES (5, 6, 6, 'pendiente', 0, date('now', '-1 day'), 'Evaluacion ortopedia')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO autorizaciones (id, paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones) VALUES (6, 7, 7, 'aprobada', 4, date('now', '-5 day'), 'Endodoncia cubierta')"
    )

    # Citas de ejemplo
    cursor.execute(
        "INSERT OR IGNORE INTO citas (id, paciente_id, medico, fecha, tipo_atencion, estado, diagnostico, factura_total) VALUES (1, 1, 'Dra. Lopez', date('now', '+1 day'), 'cita', 'programada', 'Control general', 20000)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO citas (id, paciente_id, medico, fecha, tipo_atencion, estado, diagnostico, factura_total) VALUES (2, 2, 'Dr. Vargas', date('now'), 'urgencia', 'atendida', 'Triage y estabilizacion', 45000)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO citas (id, paciente_id, medico, fecha, tipo_atencion, estado, diagnostico, factura_total) VALUES (3, 3, 'Dr. Molina', date('now', '+2 day'), 'hospitalizacion', 'programada', 'Ingreso para observacion', 150000)"
    )

    connection.commit()
    connection.close()