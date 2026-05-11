
#import de Tkinter
import tkinter as tk

cuentas_guardia = [
    {"usuario": "guardia1", "contrasena": "1234"},
    {"usuario": "guardia2", "contrasena": "5678"}]


def titulo_parqueadero_uleam(ventana):
    #Crea el logo de la ULEAM
    logo_uleam = tk.PhotoImage(file="assets/logo_uleam.png")

    #Titulo de parqueadero uleam
    Parqueadero_uleam = tk.Label(ventana,
                     image=logo_uleam,
                     text=" PARQUEADERO ULEAM", 
                     bg="gray25", 
                     fg="red", 
                     font=("Times New Roman", 60),  
                     pady=10,
                     compound="left")
    Parqueadero_uleam.image = logo_uleam
    Parqueadero_uleam.pack(pady=(0,60), fill="x")

#Funcion para el login de guardia
def login_guardia(ventana):
    
    #Limpiar la ventana
    for borra in ventana.winfo_children():
        borra.destroy()

    #titulo de parqueadero uleam
    titulo_parqueadero_uleam(ventana)
    
    #Boton para login de guardia

    btnestudiante =tk.Button(ventana, 
                             text="LOGIN GUARDIA",
                             font=("Times New Roman", 40), 
                             bg="forestgreen", fg="white",
                             command=lambda: login(ventana), 
                             padx=10,
                             cursor = "hand2")
    btnestudiante.pack(pady=110)

def login(ventana):
    #Limpiar la ventana
    for borra in ventana.winfo_children():
        borra.destroy()

    #titulo de parqueadero uleam
    titulo_parqueadero_uleam(ventana)

    #label e ingreso de usuario
    iniciarsesion_guardia = tk.Label(ventana, 
             text="Iniciar Sesión - Guardia",  
             fg="black", 
             font=("Times New Roman", 35), 
             width=30)
    iniciarsesion_guardia.pack(pady=(0, 20))

    #ENTRADA DE USUARIO Y CONTRASEÑA
    palabra_usuario = tk.Label(ventana, 
             text="Usuario",
             bg="gray13",
             fg="white", 
             font=("Times New Roman", 20), 
             width=30)
    palabra_usuario.pack(pady=(0, 10))

    ingreso_usuario = tk.Entry(ventana, 
             font=("Times New Roman", 20), 
             width=30)
    ingreso_usuario.pack(pady=(0, 20))

    palabra_contrasena = tk.Label(ventana, 
             text="Contraseña",
                bg="gray13",
                fg="white",
                font=("Times New Roman", 20), 
                width=30)
    palabra_contrasena.pack(pady=(0, 10))

    ingreso_contrasena = tk.Entry(ventana, 
             font=("Times New Roman", 20), 
             width=30, 
             show="*")
    ingreso_contrasena.pack(pady=(0, 20))
    
    btn_iniciar_sesion = tk.Button(ventana,
                                  text="Iniciar Sesión",
                                  font=("Times New Roman", 20),
                                  bg="snow",
                                  fg="black",
                                  command=lambda: validar_usuario_contrasena(ingreso_usuario, ingreso_contrasena, ventana),
                                  padx=10,
                                  cursor="hand2")
    btn_iniciar_sesion.pack(pady=10)

    btn_volver =tk.Button(ventana, 
                   text="Volver",
                   font=("Times New Roman", 20), 
                   bg="forestgreen", 
                   fg="black", 
                   command=lambda: login_guardia(ventana), 
                   padx=10,
                   cursor = "hand2")
    btn_volver.pack(pady=10, side="left", padx=(40 ,0) )

def validar_usuario_contrasena(ingreso_usuario, ingreso_contrasena, ventana):
    usuario = ingreso_usuario.get()
    contrasena = ingreso_contrasena.get()
    for cuenta in cuentas_guardia:
        if cuenta["usuario"] == usuario and cuenta["contrasena"] == contrasena:
            menu_guardia(ventana)
        else:
            tk.messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def menu_guardia(ventana):
    # Limpiar la ventana
    for borra in ventana.winfo_children():
        borra.destroy()

    #titulo de parqueadero uleam
    titulo_parqueadero_uleam(ventana)

    #Boton para cerrar sesion
    btn_volver =tk.Button(ventana, 
                   text="Cerrar Sesión",
                   font=("Times New Roman", 20), 
                   bg="forestgreen", 
                   fg="black", 
                   command=lambda: login_guardia(ventana), 
                   padx=10,
                   cursor = "hand2")
    btn_volver.pack(pady=20, anchor="ne", padx=(0, 40))

    #frame para el menu de guardia
    frame_menu_guardia = tk.Frame(ventana, 
                                  bg="gray25")
    frame_menu_guardia.pack(pady=10)
    
    #Boton para registrar ingreso de vehiculo
    btn_registrar_ingreso = tk.Button(frame_menu_guardia, 
                                      text="Registro de Vehículo", 
                                      font=("Times New Roman", 20))
    btn_registrar_ingreso.pack(pady=20, padx=20)
    
    #Boton para registrar salida de vehiculo
    btn_asignar_espacio_o_degsinacion_espacio = tk.Button(frame_menu_guardia, 
                                                          text="Asignar/Desasignar Espacio", 
                                                          font=("Times New Roman", 20))
    btn_asignar_espacio_o_degsinacion_espacio.pack(pady=20, padx=20)