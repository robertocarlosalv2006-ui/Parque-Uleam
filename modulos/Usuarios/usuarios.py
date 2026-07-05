import sqlite3
import tkinter as tk
# Importaciones correctas según tu estructura de módulos
from modulos.Usuarios.usuarios_estudiante import menu_registro_buscar_estudiante
from modulos.Usuarios.usuarios_profesor import menu_registro_buscar_profesor
from modulos.Usuarios.usuarios_invitado import menu_registro_buscar_invitado

def titulo_parqueadero_uleam(ventana):
    try:
        logo_uleam = tk.PhotoImage(file="assets/logo_uleam.png")
    except Exception:
        logo_uleam = None  # Evita que falle si la ruta de la imagen cambia

    parqueadero_uleam = tk.Label(
        ventana,
        image=logo_uleam,
        text=" PARQUEADERO ULEAM", 
        bg="red3", 
        fg="white", 
        font=("Times New Roman", 18),
        pady=10,
        compound="left"
    )
    if logo_uleam:
        parqueadero_uleam.image = logo_uleam
    parqueadero_uleam.pack(pady=(0, 10), fill="x")

def usuario(ventana):
    # Limpiar la ventana actual por completo
    for borra in ventana.winfo_children():
        borra.destroy()

    # Dibujar el encabezado de la ULEAM
    titulo_parqueadero_uleam(ventana)

    # Botón para regresar al menú anterior (Guardia) posicionado arriba a la derecha
    from modulos.guardia import menu_guardia  # Importación local para evitar bucles de importación
    btn_volver = tk.Button(
        ventana, 
        text="Volver al Menú",
        font=("Times New Roman", 10), 
        bg="forestgreen", 
        fg="white", 
        command=lambda: menu_guardia(ventana),
        cursor="hand2"
    )
    btn_volver.pack(pady=5, anchor="ne", padx=(0, 20))

    # Crear y empaquetar el contenedor principal de botones
    frame_menu_usuario = tk.Frame(ventana, bg="gray13")
    frame_menu_usuario.pack(pady=10) # Removido expand=True para conservar proporciones en 400x400

    # Botón Estudiante
    btn_registrar_usuario_estudiante = tk.Button(
        frame_menu_usuario,
        text="Registrar Estudiante",
        font=("Times New Roman", 12),
        bg="snow",
        fg="black",
        width=22,
        cursor="hand2",
        command=lambda: menu_registro_buscar_estudiante(ventana)
    )
    btn_registrar_usuario_estudiante.pack(pady=8, padx=20)

    # Botón Profesor
    btn_registrar_usuario_profesor = tk.Button(
        frame_menu_usuario,
        text="Registrar Profesor",
        font=("Times New Roman", 12),
        bg="snow",
        fg="black",
        width=22,
        cursor="hand2",
        command=lambda: menu_registro_buscar_profesor(ventana)
    )
    btn_registrar_usuario_profesor.pack(pady=8, padx=20)

    # Botón Invitado
    btn_registrar_usuario_invitado = tk.Button(
        frame_menu_usuario,
        text="Registrar Invitado",
        font=("Times New Roman", 12),
        bg="snow",
        fg="black",
        width=22,
        cursor="hand2",
        command=lambda: menu_registro_buscar_invitado(ventana)
    )
    btn_registrar_usuario_invitado.pack(pady=8, padx=20)
