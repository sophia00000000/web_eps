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

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            documento TEXT UNIQUE NOT NULL,
            direccion TEXT,
            telefono TEXT,
            email TEXT,
            estado_afiliacion TEXT NOT NULL DEFAULT 'pendiente'
        );

        CREATE TABLE IF NOT EXISTS afiliaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            eps_nombre TEXT NOT NULL,
            regimen TEXT NOT NULL,
            estado TEXT NOT NULL,
            fecha_afiliacion TEXT,
            fecha_cancelacion TEXT,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
        );

        CREATE TABLE IF NOT EXISTS planes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            tarifa_base REAL NOT NULL,
            cobertura TEXT NOT NULL,
            incluye_ortodoncia INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo_servicio TEXT NOT NULL,
            tarifa_base REAL NOT NULL,
            requiere_especialidad TEXT,
            nivel_complejidad INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS autorizaciones (
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

        CREATE TABLE IF NOT EXISTS citas (
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
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, estado_afiliacion) VALUES (1, 'Paciente Demo', '1001', 'activa')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion) VALUES (2, 'Mariana Gomez', '1002', '3005551002', 'mariana@example.com', 'activa')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion) VALUES (3, 'Carlos Perez', '1003', '3005551003', 'carlos@example.com', 'suspendida')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO pacientes (id, nombre, documento, telefono, email, estado_afiliacion) VALUES (4, 'Laura Ruiz', '1004', '3005551004', 'laura@example.com', 'pendiente')"
    )
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
        "INSERT OR IGNORE INTO planes (id, nombre, tipo, tarifa_base, cobertura, incluye_ortodoncia) VALUES (1, 'Plan Basico', 'basico', 50000, 'general', 0)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO planes (id, nombre, tipo, tarifa_base, cobertura, incluye_ortodoncia) VALUES (2, 'Plan Premium', 'complementario', 120000, 'amplia', 1)"
    )
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
        "INSERT OR IGNORE INTO autorizaciones (id, paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones) VALUES (1, 1, 1, 'aprobada', 4, date('now', '-3 day'), 'Aprobada sin novedades')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO autorizaciones (id, paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones) VALUES (2, 2, 3, 'aprobada', 4, date('now', '-2 day'), 'Cobertura validada')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO autorizaciones (id, paciente_id, servicio_id, estado, nivel_aprobacion, fecha_solicitud, observaciones) VALUES (3, 3, 4, 'rechazada', 1, date('now', '-1 day'), 'Afiliacion suspendida')"
    )
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