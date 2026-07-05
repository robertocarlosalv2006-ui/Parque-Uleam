from tkinter import *
from tkinter import messagebox

# Matriz del estacionamiento (5 filas x 15 columnas)
FILAS = 5
COLUMNAS = 15

# Estructura de datos en memoria (Asegura persistencia temporal interactiva)
estacionamiento = [[None for i in range(COLUMNAS)] for j in range(FILAS)]
letras = "ABCDE"

# Variables globales
botones = []
nombre = None
placa = None
marca = None
hora = None
observaciones = None

# Variables para controlar el puesto seleccionado actualmente para retirar
fila_seleccionada = None
columna_seleccionada = None

def vehiculos(ventana):
    global nombre, placa, marca, hora, observaciones, botones
    global fila_seleccionada, columna_seleccionada
    
    # Reiniciar selecciones al entrar
    fila_seleccionada = None
    columna_seleccionada = None

    # 1. Limpiar por completo la interfaz previa
    for borra in ventana.winfo_children():
        borra.destroy()

    # 2. Configurar ventana (Dimensiones óptimas para el mapa)
    ventana.geometry("1100x650")
    ventana.config(bg="gray13")

    # 3. Inicializar las variables de Tkinter
    nombre = StringVar(ventana)
    placa = StringVar(ventana)
    marca = StringVar(ventana)
    hora = StringVar(ventana)
    observaciones = StringVar(ventana)

    # Botón Volver
    btn_volver = Button(
        ventana, 
        text="Volver al Menú", 
        font=("Arial", 11, "bold"),
        bg="forestgreen",
        fg="white",
        command=lambda: regresar_al_menu(ventana),
        cursor="hand2"
    )
    btn_volver.place(x=950, y=20)

    # --- FORMULARIO DE INGRESO ---
    Label(ventana, text="Nombre Propietario:", font=("Arial", 11), bg="gray13", fg="white").place(x=20, y=20)
    Entry(ventana, textvariable=nombre, width=30, font=("Arial", 11)).place(x=180, y=20)

    Label(ventana, text="Placa Vehículo:", font=("Arial", 11), bg="gray13", fg="white").place(x=20, y=55)
    Entry(ventana, textvariable=placa, width=30, font=("Arial", 11)).place(x=180, y=55)

    Label(ventana, text="Marca del Vehículo:", font=("Arial", 11), bg="gray13", fg="white").place(x=470, y=20)
    Entry(ventana, textvariable=marca, width=30, font=("Arial", 11)).place(x=630, y=20)

    Label(ventana, text="Hora de Ingreso:", font=("Arial", 11), bg="gray13", fg="white").place(x=470, y=55)
    Entry(ventana, textvariable=hora, width=30, font=("Arial", 11)).place(x=630, y=55)

    Label(ventana, text="Observaciones:", font=("Arial", 11), bg="gray13", fg="white").place(x=20, y=95)
    Entry(ventana, textvariable=observaciones, width=86, font=("Arial", 11)).place(x=180, y=95)

    # --- BOTÓN PARA RETIRAR VEHÍCULO ---
    global btn_retirar
    btn_retirar = Button(
        ventana,
        text="Retirar Vehículo",
        font=("Arial", 11, "bold"),
        bg="firebrick",
        fg="white",
        state=DISABLED,
        command=lambda: enviar_a_salidas(ventana), 
        cursor="hand2"
    )
    btn_retirar.place(x=950, y=90, width=130, height=35)

    Label(
        ventana,
        text="MAPA DE ESPACIOS (Celeste: Libre | Rojo: Ocupado)",
        font=("Arial", 12, "bold"),
        bg="gray13",
        fg="yellow"
    ).place(x=20, y=145)

    # --- RENDERIZADO DEL MAPA ---
    frame_mapa = Frame(ventana, bg="gray25", bd=2, relief=SUNKEN)
    frame_mapa.place(x=20, y=180, width=1060, height=440)

    botones = [] 

    for i in range(FILAS):
        fila_botones = []
        for j in range(COLUMNAS):
            puesto = f"{letras[i]}-{j+1}"
            
            if estacionamiento[i][j] is not None:
                txt_boton = f"{puesto}\n{estacionamiento[i][j]['placa']}"
                bg_color = "red"
                fg_color = "white"
            else:
                txt_boton = puesto
                bg_color = "sky blue"
                fg_color = "black"

            boton = Button(
                frame_mapa,
                text=txt_boton,
                width=8,
                height=3,
                bg=bg_color,
                fg=fg_color,
                font=("Arial", 9, "bold"),
                command=lambda f=i, c=j: click_puesto(f, c)
            )
            boton.grid(row=i, column=j, padx=4, pady=8)
            fila_botones.append(boton)
            
        botones.append(fila_botones)

def click_puesto(fila, column):
    global fila_seleccionada, columna_seleccionada
    puesto = f"{letras[fila]}-{column+1}"

    if estacionamiento[fila][column] is None:
        btn_retirar.config(state=DISABLED)
        ocupar_puesto(fila, column)
    else:
        fila_seleccionada = fila
        columna_seleccionada = column
        datos = estacionamiento[fila][column]
        
        btn_retirar.config(state=NORMAL)
        messagebox.showinfo(
            "Puesto Seleccionado", 
            f"Puesto: {puesto}\n"
            f"Vehículo: {datos['marca']} ({datos['placa']})\n"
            f"Propietario: {datos['nombre']}\n\n"
            "Presione el botón 'Retirar Vehículo' arriba a la derecha para calcular pago."
        )

def ocupar_puesto(fila, columna):
    if (nombre.get().strip() == "" or placa.get().strip() == "" or
        marca.get().strip() == "" or hora.get().strip() == ""):
        messagebox.showwarning(
            "Aviso",
            "Complete todos los campos obligatorios antes de seleccionar un puesto libre."
        )
        return

    estacionamiento[fila][columna] = {
        "nombre": nombre.get(),
        "placa": placa.get(),
        "marca": marca.get(),
        "hora": hora.get(),
        "observaciones": observaciones.get()
    }

    puesto = f"{letras[fila]}-{columna+1}"
    botones[fila][columna].config(
        text=f"{puesto}\n{placa.get()}",
        bg="red",
        fg="white"
    )

    messagebox.showinfo("Registro Exitoso", f"Vehículo asignado al puesto: {puesto}")

    nombre.set("")
    placa.set("")
    marca.set("")
    hora.set("")
    observaciones.set("")

def enviar_a_salidas(ventana):
    global fila_seleccionada, columna_seleccionada
    
    if fila_seleccionada is None or columna_seleccionada is None:
        return

    datos_vehiculo = estacionamiento[fila_seleccionada][columna_seleccionada]
    puesto_texto = f"{letras[fila_seleccionada]}-{columna_seleccionada+1}"

    # Importación dinámica local del módulo salidas
    try:
        from modulos.salidas import salidas
        salidas(ventana, datos_vehiculo, puesto_texto, fila_seleccionada, columna_seleccionada)
    except ModuleNotFoundError:
        messagebox.showerror("Error", "No se encontró el módulo de cobros/salidas.py")

def liberar_puesto_desde_salidas(fila, columna):
    """Permite que el módulo de salidas limpie la celda y restaure el botón a celeste."""
    global botones
    estacionamiento[fila][columna] = None
    puesto = f"{letras[fila]}-{columna+1}"
    
    if botones:
        botones[fila][columna].config(
            text=puesto,
            bg="sky blue",
            fg="black"
        )

def regresar_al_menu(ventana):
    """Restaura dimensiones originales y regresa al menú de control del guardia."""
    ventana.geometry("600x550")  # Restauramos proporciones cómodas para menús estándar
    from modulos.guardia import menu_guardia
    menu_guardia(ventana)

def regresar_a_vehiculos(ventana):
    """Redirecciona de forma segura al mapa de parqueo rompiendo el bloqueo de hilos circulares."""
    ventana.geometry("1100x650")
    
    for borra in ventana.winfo_children():
        borra.destroy()
        
    # Bloque try/except corregido y cerrado sintácticamente de forma robusta
    try:
        modulo = __import__('modulos.Vehiculos.vehiculos', fromlist=['vehiculos'])
    except ModuleNotFoundError:
        try:
            modulo = __import__('modulos.vehiculos.vehiculos', fromlist=['vehiculos'])
        except ModuleNotFoundError:
            try:
                modulo = __import__('modulos.vehiculos', fromlist=['vehiculos'])
            except ModuleNotFoundError:
                messagebox.showerror("Error estructural", "No se pudo resolver la ruta de importación de vehiculos")
                return
        
    # Forzar la ejecución limpia del mapa para evadir bloqueos de callbacks concurrentes
    ventana.after(1, lambda: modulo.vehiculos(ventana))
