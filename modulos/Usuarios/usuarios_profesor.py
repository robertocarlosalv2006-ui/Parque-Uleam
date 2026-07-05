import sqlite3
import tkinter as tk
from tkinter import messagebox
# Importamos la función de inserción unificada de database.py
from database import insertar_usuario 

# Base de datos unificada
DB_NAME = "parqueadero_uleam.db"

def titulo_parqueadero_uleam(ventana):
    try:
        logo_uleam = tk.PhotoImage(file="assets/logo_uleam.png")
    except Exception:
        logo_uleam = None

    parqueadero_lbl = tk.Label(
        ventana,
        image=logo_uleam,
        text=" PARQUEADERO ULEAM", 
        bg="red3", 
        fg="white", 
        font=("Times New Roman", 18),  # Fuente ajustada para evitar desbordes visuales
        pady=8,
        compound="left"
    )
    if logo_uleam:
        parqueadero_lbl.image = logo_uleam
    parqueadero_lbl.pack(pady=(0, 10), fill="x")

def menu_registro_buscar_profesor(ventana):
    for borra in ventana.winfo_children():
        borra.destroy()

    ventana.config(bg="gray13")
    titulo_parqueadero_uleam(ventana)

    # Botón Volver desacoplado para prevenir bucles de importación
    btn_regresar = tk.Button(
        ventana, 
        text="Volver", 
        font=("Times New Roman", 10, "bold"),
        bg="forestgreen",
        fg="white",
        command=lambda: regresar_a_usuarios(ventana),
        cursor="hand2"
    )
    btn_regresar.pack(pady=2, anchor="ne", padx=(0, 15))

    # --- FORMULARIO DE REGISTRO ---
    tk.Label(ventana, text="Nombre:", fg="white", bg="gray13", font=("Times New Roman", 11)).pack(pady=1)
    entry_nombre = tk.Entry(ventana, font=("Times New Roman", 10), width=28)
    entry_nombre.pack(pady=1)

    tk.Label(ventana, text="Cédula:", fg="white", bg="gray13", font=("Times New Roman", 11)).pack(pady=1)
    entry_cedula = tk.Entry(ventana, font=("Times New Roman", 10), width=28)
    entry_cedula.pack(pady=1)

    tk.Button(
        ventana, 
        text="Registrar Profesor", 
        font=("Times New Roman", 10, "bold"),
        bg="snow",
        fg="black",
        command=lambda: Registrar_Profesor(entry_nombre, entry_cedula),
        cursor="hand2"
    ).pack(pady=5)

    # --- SECCIÓN DE BÚSQUEDA ---
    tk.Label(ventana, text="Buscar por nombre o cédula:", fg="white", bg="gray13", font=("Times New Roman", 11)).pack(pady=1)
    entry_buscar = tk.Entry(ventana, font=("Times New Roman", 10), width=28)
    entry_buscar.pack(pady=1)

    tk.Button(
        ventana, 
        text="Buscar", 
        font=("Times New Roman", 10, "bold"),
        bg="snow",
        fg="black",
        command=lambda: buscar_Profesor(entry_buscar, resultado_text),
        cursor="hand2"
    ).pack(pady=3)

    resultado_text = tk.Text(ventana, height=3, width=32, font=("Times New Roman", 10))
    resultado_text.pack(pady=2)

def Registrar_Profesor(entry_nombre, entry_cedula):
    nombre = entry_nombre.get().strip()
    cedula = entry_cedula.get().strip()

    if nombre == "" or cedula == "":
        messagebox.showwarning("Campos vacíos", "Debe llenar todos los campos")
        return

    # Inserción real y persistente utilizando SQLite
    id_generado = insertar_usuario(cedula, nombre)
    
    if id_generado is not None:
        messagebox.showinfo("Éxito", "Profesor registrado correctamente en la Base de Datos")
        entry_nombre.delete(0, tk.END)
        entry_cedula.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "La cédula ya se encuentra registrada en el sistema")

def buscar_Profesor(entry_buscar, resultado_text):
    criterio = entry_buscar.get().strip()
    resultado_text.delete("1.0", tk.END)

    if criterio == "":
        resultado_text.insert(tk.END, "Por favor ingrese un término")
        return

    # Consulta real a la tabla unificada de usuarios
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        
        query = "SELECT nombres, cedula FROM usuarios WHERE cedula = ? OR nombres LIKE ?"
        cursor.execute(query, (criterio, f"%{criterio}%"))
        encontrados = cursor.fetchall()
        conexion.close()

        if encontrados:
            for nombres, cedula in encontrados:
                resultado_text.insert(tk.END, f"{nombres} | Cédula: {cedula}\n")
        else:
            resultado_text.insert(tk.END, "Sin resultados en el sistema")
            
    except sqlite3.Error as e:
        messagebox.showerror("Error de Consulta", f"No se pudo buscar en la BD: {e}")

def regresar_a_usuarios(ventana):
    from modulos.Usuarios.usuarios import usuario
    usuario(ventana)
