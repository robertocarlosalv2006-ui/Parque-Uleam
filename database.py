import sqlite3

def tabla_datos():
    # Asegúrate de usar este mismo nombre de archivo en todo tu proyecto
    conexion = sqlite3.connect("parqueadero_uleam.db")
    cursor = conexion.cursor()

    # ==========================
    # TABLA DE USUARIOS (Estudiantes, Profesores, Invitados)
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cedula TEXT UNIQUE NOT NULL,
        nombres TEXT NOT NULL
    )
    """)  # <-- CORREGIDO: Se eliminó la coma sobrante al final

    # ==========================
    # TABLA DE GUARDIAS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guardias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        clave TEXT NOT NULL
    )
    """)  # <-- CORREGIDO: Se eliminó la coma sobrante al final

    # ==========================
    # TABLA DE VEHICULOS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehiculos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT UNIQUE NOT NULL,
        tipo TEXT NOT NULL,
        propietario INTEGER,
        FOREIGN KEY(propietario) REFERENCES usuarios(id)
    )
    """)

    # ==========================
    # TABLA DE ESPACIOS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS espacios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_espacio INTEGER UNIQUE,
        estado TEXT,
        tipo TEXT
    )
    """)

    # ==========================
    # TABLA DE INGRESOS
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingresos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT,
        espacio INTEGER,
        fecha_ingreso TEXT,
        FOREIGN KEY(espacio) REFERENCES espacios(id)
    )
    """)
    

    # ==========================
    # TABLA DE HISTORIAL
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT,
        fecha_ingreso TEXT,
        fecha_salida TEXT,
        tiempo_total REAL,
        valor_pagado REAL
    )
    """)

    conexion.commit()
    conexion.close()
    print("Base de datos creada correctamente")


# =====================================
# FUNCIONES DE INSERCIÓN
# =====================================

def insertar_usuario(cedula, nombres):
    """Inserta una persona en la tabla usuarios. Retorna el ID generado o None si falla."""
    try:
        conexion = sqlite3.connect("parqueadero_uleam.db")
        cursor = conexion.cursor()
        
        cursor.execute("""
        INSERT INTO usuarios (cedula, nombres)
        VALUES (?, ?)
        """, (cedula, nombres))
        
        conexion.commit()
        id_usuario = cursor.lastrowid # Guardamos el ID por si lo necesitas para la tabla vehículos
        conexion.close()
        return id_usuario
    except sqlite3.IntegrityError:
        return None     


def insertar_guardia(usuario, clave):
    """Inserta un nuevo guardia en la base de datos."""
    try:
        conexion = sqlite3.connect("parqueadero_uleam.db")
        cursor = conexion.cursor()
        
        cursor.execute("""
        INSERT INTO guardias (usuario, clave)
        VALUES (?, ?)
        """, (usuario, clave))
        
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.IntegrityError:
        return False
