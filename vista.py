import tkinter as tk
from modelo import *
import datetime
import RPi.GPIO as GPIO




def configurarPulsadores():
    #pulsadores config
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def getFecha():
    return datetime.datetime.today() 
def getParidadFecha():
    return getFecha().day%2 == 0


root = tk.Tk()


def getRoot():
    global root
    root.title("lector ")

    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    texto="Bienvenido \n Por favor presente su documento en el lector"
    myLabel3 =tk.Label(root, text="Centro Comercial Tundama")
    myLabel3.config(font=("Courier", 35))
    myLabel3.grid(row=0, column=1)
    myLabel3.grid(row=0, column=1)
    entry = tk.Entry(root, width= '50')
    entry.grid(row=1, column=1)
    entry.focus_set()
    myLabel1 =tk.Label(root, text=texto)
    myLabel1.config(font=("Courier", 35))
    myLabel1.grid(row=2, column=1)
    myLabel2 =tk.Label(root, text=" ")
    myLabel2.config(font=("Courier", 35))
    myLabel2.grid(row=3, column=1)

    button= tk.Button(root, command=evento)
    button.grid(row=1, column=2)
    root.bind('<Return>', lambda event=None: button.invoke())
    
    return root


estado=0

def evento():
    global estado
    if estado==0:
        
        

        estado=1


getRoot().mainloop()