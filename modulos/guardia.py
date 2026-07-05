import sqlite3
import tkinter as tk
from tkinter import messagebox
# Importamos la función de inserción que ya habías creado en database
from database import insertar_guardia 

# IMPORTANTE: Asegúrate de que estas rutas de importación sean correctas en tu PC
from modulos.Usuarios.usuarios import usuario
from modulos.vehiculos import vehiculos

# Base de datos unificada (La misma que main.py)
DB_NAME = "parqueadero_uleam.db"

def titulo_parqueadero_uleam(ventana):
    try:
        logo_uleam = tk.PhotoImage(file="assets/logo_uleam.png")
    except Exception:
        # Evita que el programa se caiga si no encuentra la imagen del logo
        logo_uleam = None

    parqueadero_lbl = tk.Label(
        ventana,
        image=logo_uleam,
        text=" PARQUEADERO ULEAM", 
        bg="red3", 
        fg="white", 
        font=("Times New Roman", 24),  # Reducido de 60 para que quepa en la pantalla
        pady=10,
        compound="left"
    )
    if logo_uleam:
        parqueadero_lbl.image = logo_uleam
    parqueadero_lbl.pack(pady=(0, 20), fill="x")


def login_guardia(ventana):
   
    for borra in ventana.winfo_children():
        borra.destroy()


    titulo_parqueadero_uleam(ventana)
    
    btn_login = tk.Button(
        ventana, 
        text="LOGIN GUARDIA",
        font=("Times New Roman", 18), # Reducido de 40
        bg="forestgreen", 
        fg="white",
        command=lambda: login(ventana), 
        padx=10,
        cursor="hand2"
    )
    btn_login.pack(pady=40)

def login(ventana):

    for borra in ventana.winfo_children():
        borra.destroy()


    titulo_parqueadero_uleam(ventana)

    tk.Label(
        ventana, 
        text="Iniciar Sesión - Guardia",  
        fg="black", 
        font=("Times New Roman", 18), 
        width=30
    ).pack(pady=(0, 10))

    tk.Label(ventana, text="Usuario", bg="gray13", fg="white", font=("Times New Roman", 12)).pack(pady=(5, 2))
    ingreso_usuario = tk.Entry(ventana, font=("Times New Roman", 12), width=25)
    ingreso_usuario.pack()

    tk.Label(ventana, text="Contraseña", bg="gray13", fg="white", font=("Times New Roman", 12)).pack(pady=(5, 2))
    ingreso_contrasena = tk.Entry(ventana, font=("Times New Roman", 12), width=25, show="*")
    ingreso_contrasena.pack()
    
    contenedor_botones = tk.Frame(ventana, bg="gray13")
    contenedor_botones.pack(pady=15)
    
    tk.Button(
        contenedor_botones,
        text="Iniciar Sesión",
        font=("Times New Roman", 12),
        bg="snow",
        fg="black",
        command=lambda: validar_usuario_contrasena(ingreso_usuario, ingreso_contrasena, ventana),
        cursor="hand2"
    ).pack(side="left", padx=5)

    tk.Button(
        contenedor_botones, 
        text="Registrar Guardia",
        font=("Times New Roman", 12), 
        bg="snow", 
        fg="black", 
        command=lambda: registrar_guardia(ventana), 
        cursor="hand2"
    ).pack(side="left", padx=5)

    tk.Button(
        ventana, 
        text="Volver",
        font=("Times New Roman", 12), 
        bg="forestgreen", 
        fg="white", 
        command=lambda: login_guardia(ventana), 
        cursor="hand2"
    ).pack(pady=10)

def registrar_guardia(ventana):
    for borra in ventana.winfo_children():
        borra.destroy()

    titulo_parqueadero_uleam(ventana)

    tk.Label(ventana, text="Registrar Guardia", fg="black", font=("Times New Roman", 18)).pack(pady=(0, 10))

    tk.Label(ventana, text="Usuario", bg="gray13", fg="white", font=("Times New Roman", 12)).pack(pady=(5, 2))
    ingreso_usuario = tk.Entry(ventana, font=("Times New Roman", 12), width=25)
    ingreso_usuario.pack()

    tk.Label(ventana, text="Contraseña", bg="gray13", fg="white", font=("Times New Roman", 12)).pack(pady=(5, 2))
    ingreso_contrasena = tk.Entry(ventana, font=("Times New Roman", 12), width=25, show="*")
    ingreso_contrasena.pack()
    
    contenedor_botones = tk.Frame(ventana, bg="gray13")
    contenedor_botones.pack(pady=15)
    
    tk.Button(
        contenedor_botones,
        text="Registrar",
        font=("Times New Roman", 12),
        bg="snow",
        fg="black",
        command=lambda: registro(ingreso_contrasena, ingreso_usuario, ventana),
        cursor="hand2"
    ).pack(side="left", padx=5)

    tk.Button(
        ventana, 
        text="Volver",
        font=("Times New Roman", 12), 
        bg="forestgreen", 
        fg="white", 
        command=lambda: login(ventana), # Corregido: Se añade "ventana" para evitar el TypeError
        cursor="hand2"
    ).pack(pady=10)

def registro(ingreso_contrasena, ingreso_usuario, ventana):
    user = ingreso_usuario.get()
    clave = ingreso_contrasena.get()
    
    if not user or not clave:
        messagebox.showwarning("Advertencia", "Por favor llene todos los campos")
        return

    # Reutilizamos tu función del archivo database.py
    exito = insertar_guardia(user, clave)
    if exito:
        messagebox.showinfo("Éxito", "Guardia registrado correctamente")
        login(ventana)
    else:
        messagebox.showerror("Error", "El usuario ya existe en el sistema")

def validar_usuario_contrasena(ingreso_usuario, ingreso_contrasena, ventana):
    user = ingreso_usuario.get()
    contrasena = ingreso_contrasena.get()

    # Primero validamos contra las cuentas locales "hardcoded" que dejaste escritas
    cuentas_local = [
        {"usuario": "guardia1", "contrasena": "1234"},
        {"usuario": "guardia2", "contrasena": "5678"}
    ]
    
    for cuenta in cuentas_local:
        if cuenta["usuario"] == user and cuenta["contrasena"] == contrasena:
            menu_guardia(ventana)
            return

    # Si no está en las locales, buscamos de verdad en la Base de Datos SQLite
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM guardias WHERE usuario = ? AND clave = ?", (user, contrasena))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            menu_guardia(ventana)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    except sqlite3.Error as e:
        messagebox.showerror("Error de BD", f"No se pudo consultar la base de datos: {e}")

def menu_guardia(ventana):

    for borra in ventana.winfo_children():
        borra.destroy()


    titulo_parqueadero_uleam(ventana)

    btn_volver = tk.Button(
        ventana, 
        text="Cerrar Sesión",
        font=("Times New Roman", 10), 
        bg="forestgreen",
        fg="white",
        command=lambda: login_guardia(ventana), 
        padx=5,
        cursor="hand2"
    )
    btn_volver.pack(pady=5, anchor="ne", padx=(0, 20))

    frame_menu_guardia = tk.Frame(ventana, bg="gray25")
    frame_menu_guardia.pack(pady=10)
    
    btn_registrar_ingreso = tk.Button(
        frame_menu_guardia, 
        text="Registro de Vehículo", 
        font=("Times New Roman", 12),
        command=lambda: usuario(ventana)
    )
    btn_registrar_ingreso.pack(pady=10, padx=20)
    
    btn_asignar_espacio = tk.Button(
        frame_menu_guardia, 
        text="Asignar/Desasignar Espacio", 
        font=("Times New Roman", 12),
        command=lambda: vehiculos(ventana)
    )
    btn_asignar_espacio.pack(pady=10, padx=20)
