import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3

# --- CONFIGURACIÓN DE TARIFAS DEL PARQUEADERO ---
TARIFA_POR_MINUTO = 0.02  # Equivale a $1.20 la hora
VALOR_MINIMO = 0.50       # Cobro mínimo por ingresar al establecimiento
DB_NAME = "parqueadero_uleam.db"

entry_placa = None
entry_cedula = None

def salidas(ventana, datos_vehiculo=None, puesto_texto="", fila=None, columna=None):
    """
    Controla la pantalla de cobros y salidas.
    Calcula el tiempo transcurrido y el valor a pagar si se viene desde el mapa.
    """
    global entry_placa, entry_cedula

    # 1. Limpiar por completo la interfaz previa
    for borra in ventana.winfo_children():
        borra.destroy()

    # 2. Configurar las dimensiones para la pantalla de cobros y desglose
    ventana.geometry("700x550")
    ventana.config(bg="gray13")

    # Título Superior
    titulo = tk.Label(
        ventana,
        text="SALIDA - LIQUIDACIÓN Y RETIRO",
        bg="red3",
        fg="white",
        font=("Times New Roman", 20, "bold"),
        pady=10
    )
    titulo.pack(fill="x")

    # Botón Volver al mapa de vehículos
    btn_regresar = tk.Button(
        ventana,
        text="Volver al Mapa",
        font=("Arial", 10, "bold"),
        bg="forestgreen",
        fg="white",
        command=lambda: regresar_a_vehiculos(ventana),
        cursor="hand2"
    )
    btn_regresar.pack(pady=5, anchor="ne", padx=(0, 20))

    # Frame principal de datos del vehículo
    frame = tk.Frame(ventana, bg="gray13")
    frame.pack(pady=10)

    # Campo Placa
    tk.Label(frame, text="Placa del Vehículo:", bg="gray13", fg="white", font=("Times New Roman", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_placa = tk.Entry(frame, width=30, font=("Arial", 11))
    entry_placa.grid(row=0, column=1, pady=10)

    # Campo Propietario
    tk.Label(frame, text="Propietario / Cédula:", bg="gray13", fg="white", font=("Times New Roman", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_cedula = tk.Entry(frame, width=30, font=("Arial", 11))
    entry_cedula.grid(row=1, column=1, pady=10)

    # --- AUTOCOMPLETADO Y CÁLCULO DE PAGO ---
    if datos_vehiculo is not None:
        entry_placa.insert(0, datos_vehiculo["placa"])
        entry_cedula.insert(0, f"{datos_vehiculo['nombre']} ({datos_vehiculo['marca']})")
        
        entry_placa.config(state="readonly")
        entry_cedula.config(state="readonly")

        # 1. Obtener horas de ingreso y salida real del reloj del sistema
        hora_ingreso_str = datos_vehiculo["hora"]
        hora_salida_obj = datetime.now()
        hora_salida_str = hora_salida_obj.strftime("%H:%M")

        # 2. Calcular los minutos transcurridos
        minutos_totales = calcular_minutos(hora_ingreso_str, hora_salida_str)
        
        # 3. Calcular el valor monetario a pagar
        valor_pagar = max(minutos_totales * TARIFA_POR_MINUTO, VALOR_MINIMO)

        # Contenedor visual del desglose financiero de cobro
        frame_cobro = tk.Frame(ventana, bg="gray25", bd=2, relief=tk.GROOVE)
        frame_cobro.pack(pady=10, padx=50, fill="x")

        # Fila 1: Tiempos del reporte
        tk.Label(
            frame_cobro, 
            text=f"Puesto: {puesto_texto}  |  Ingreso: {hora_ingreso_str}  |  Salida Actual: {hora_salida_str}", 
            bg="gray25", fg="white", font=("Arial", 11)
        ).pack(pady=5)

        # Fila 2: Minutos registrados en total
        tk.Label(
            frame_cobro, 
            text=f"Tiempo Total: {minutos_totales} minutos", 
            bg="gray25", fg="lightblue", font=("Arial", 11, "bold")
        ).pack(pady=2)

        # Fila 3: RECUADRO DE PAGO DE DINERO REAL
        tk.Label(
            frame_cobro, 
            text=f"TOTAL A PAGAR: ${valor_pagar:.2f}", 
            bg="gray25", fg="springgreen", font=("Arial", 16, "bold")
        ).pack(pady=8)

        # Botón para confirmar cobro en efectivo y liberar espacio
        btn_retirar = tk.Button(
            ventana,
            text="Procesar Pago y Liberar Espacio",
            font=("Arial", 12, "bold"),
            bg="firebrick",
            fg="white",
            command=lambda: ejecutar_retiro_parqueo(ventana, fila, columna, puesto_texto, hora_ingreso_str, hora_salida_str, minutos_totales, valor_pagar),
            cursor="hand2"
        )
        btn_retirar.pack(pady=15)
        
    else:
        btn_buscar = tk.Button(
            ventana, text="Buscar Vehículo", font=("Arial", 12, "bold"), bg="snow", fg="black", command=lambda: buscar_vehiculo(ventana), cursor="hand2"
        )
        btn_buscar.pack(pady=20)


def calcular_minutos(hora_ingreso, hora_salida):
    try:
        t_ingreso = datetime.strptime(hora_ingreso, "%H:%M")
        t_salida = datetime.strptime(hora_salida, "%H:%M")
        
        diferencia = t_salida - t_ingreso
        minutos = int(diferencia.total_seconds() / 60)
        
        if minutos < 0:
            return 1
        return minutos
    except Exception:
        return 30


def ejecutar_retiro_parqueo(ventana, fila, columna, puesto_texto, ingreso, salida, minutos, total):
    placa_txt = entry_placa.get().strip()
    confirmar = messagebox.askyesno(
        "Confirmar Transacción",
        f"¿Se ha recibido el pago de ${total:.2f} en efectivo?\nPresione SÍ para finalizar el retiro."
    )
    
    if confirmar:
        try:
            conexion = sqlite3.connect(DB_NAME)
            cursor = conexion.cursor()
            
            # 1. Insertamos en salidas e historial financiero
            cursor.execute("""
            INSERT INTO salidas (placa, fecha_salida, tiempo_total, valor_pagado)
            VALUES (?, ?, ?, ?)
            """, (placa_txt, f"Hoy {salida}", float(minutos), float(total)))
            
            cursor.execute("""
            INSERT INTO historial (placa, fecha_ingreso, fecha_salida, tiempo_total, valor_pagado)
            VALUES (?, ?, ?, ?, ?)
            """, (placa_txt, ingreso, salida, float(minutos), float(total)))
            
            # 2. CORREGIDO: Eliminar el vehículo de la tabla de ingresos para liberar el parqueadero de forma real y permanente
            cursor.execute("DELETE FROM ingresos WHERE placa = ? AND espacio = ?", (placa_txt, puesto_texto))
            
            conexion.commit()
            conexion.close()
        except Exception as e:
            print(f"Error al impactar la base de datos: {e}")

        # CORREGIDO: Ruta en minúsculas alineada a tu árbol original del proyecto
        try:
            from modulos.vehiculos import liberar_puesto_desde_salidas
            liberar_puesto_desde_salidas(fila, columna)
        except ModuleNotFoundError:
            print("Alerta: No se pudo limpiar la matriz temporal.")
        
        messagebox.showinfo("Éxito", f"¡Puesto {puesto_texto} Liberado!\nTransacción guardada exitosamente.")
        regresar_a_vehiculos(ventana)


def buscar_vehiculo(ventana):
    """Busca vehículos registrados en la tabla ingresos que no se han despachado."""
    placa_buscada = entry_placa.get().strip()

    if placa_buscada == "":
        messagebox.showwarning("Error", "Ingrese una placa para realizar la búsqueda manual.")
        return

    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("SELECT espacio, fecha_ingreso FROM ingresos WHERE placa = ?", (placa_buscada,))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            puesto, h_ingreso = resultado
            # Convertimos al formato esperado para autocompletar la pantalla
            datos_ficticios = {
                "placa": placa_buscada,
                "nombre": "Propietario Registrado",
                "marca": "Vehículo",
                "hora": h_ingreso
            }
            # Refrescamos la pantalla simulando el clic en el botón del mapa
            salidas(ventana, datos_ficticios, puesto, fila=0, columna=0)
        else:
            messagebox.showerror("Sin Resultados", "No se encontró ningún vehículo activo con esa placa.")
    except sqlite3.Error as e:
        messagebox.showerror("Error BD", f"No se pudo consultar la tabla de ingresos: {e}")


def regresar_a_vehiculos(ventana):
    """Redirecciona a la vista del mapa de puestos redimensionando la ventana."""
    ventana.geometry("1100x650")
    # CORREGIDO: Ruta en minúsculas unificada para romper el ciclo sin crasheos
    __import__('modulos.vehiculos', fromlist=['vehiculos']).vehiculos(ventana)
