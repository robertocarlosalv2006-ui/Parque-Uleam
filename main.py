import tkinter as tk
from modulos.guardia import login_guardia
from database import tabla_datos

tabla_datos()  # Llamada a la función para crear las tablas de la base de datos

ventana = tk.Tk()

#Esto es la configuracion de la ventana,
ventana.title("PARQUEADERO ULEAM")
ventana.geometry("400x400")
ventana.config(bg="gray13")

#Esto es el menu principal
def menu_principal():

    login_guardia(ventana)



menu_principal()
ventana.mainloop()