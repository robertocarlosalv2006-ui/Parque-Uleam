import tkinter as tk
from modulos.guardia import login_guardia

ventana = tk.Tk()

#Esto es la configuracion de la ventana,
ventana.title("PARQUEADERO ULEAM")
ventana.geometry("1200x800")
ventana.minsize(1400, 800)
ventana.config(bg="gray13")

#Esto es el menu principal
def menu_principal():

    login_guardia(ventana)

menu_principal()
ventana.mainloop()