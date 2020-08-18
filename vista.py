import tkinter as tk
from modelo import *
import datetime
import RPi.GPIO as GPIO
import sensorLibD6T as temperatura
import os
import audios as audios


#audios.guardarAudios()

def configPulsador():
    #pulsadores config
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def getPulsador():
    pulsador = 0
    if GPIO.input(16) == 0:  # pulsador de arrendatarios
        pulsador = 1
    elif GPIO.input(18) == 0:  # pulsador de clientes
        pulsador = 2
    return pulsador


def decirIntro(genero):
    if genero == "F":
        os.system("mpg321 introMujer.mp3")
    else:
        os.system("mpg321 introHombre.mp3")


def decirBienvenida(genero):
    if genero == "F":
        os.system("mpg321 bienvenida.mp3")
    else:
        os.system("mpg321 bienvenido.mp3")


def validarFecha(documento):
    h = datetime.datetime.today().day % 2 == int(documento[-1]) % 2
    print(h)
    return h


def delPubDocumento(documento):
    if "PubDSK_1" in documento:
        return documento[8:]
    return documento


def getTexto(genero, nombres):
    if genero == 'F':
        return "Bienvenida señora " + nombres+"\nPor favor acérquese al sensor"
    return "Bienvenido señor " + nombres+"\nPor favor acérquese al sensor"


def validarEdad(genero):
    if texto[5] == '0':
        return True
    return False


def separarEntrada(entrada):
    texto = entrada.split('-')
    data = {
        "documento": delPubDocumento(texto[0]),
        "nombres": texto[3] + " " + texto[4],
        "apellidos": texto[1] + " " + texto[2],
        "genero": texto[5],
        "fecha_nacimiento": texto[6]
    }
    return data


def reinicio():
    global myLabel1
    global myLabel2
    global root
    texto = "Bienvenido.\nPor favor presente su documento en el lector"
    myLabel1.config(text=texto)
    myLabel2.config(text="")
    root.update()


root = tk.Tk()
root.title("lector ")

root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
texto = "Bienvenido \n Por favor presente su documento en el lector"
myLabel3 = tk.Label(root, text="Centro Comercial Tundama")
myLabel3.config(font=("Courier", 35))
myLabel3.grid(row=0, column=1)
myLabel3.grid(row=0, column=1)
entry = tk.Entry(root, width='50')
entry.grid(row=1, column=1)
entry.focus_set()
myLabel1 = tk.Label(root, text=texto)
myLabel1.config(font=("Courier", 35))
myLabel1.grid(row=2, column=1)
myLabel2 = tk.Label(root, text=" ")
myLabel2.config(font=("Courier", 35))
myLabel2.grid(row=3, column=1)


configPulsador()


estado = 0


def evento():
    global estado
    if estado == 0:
        estado = 1
        model = Modelo()
        data = separarEntrada(entry.get())
        entry.delete(0, "end")
        resultado = model.getUsuario(data["documento"])
        if (resultado is None):
            data["permiso"] = getPulsador()
            if data["permiso"] == 0 and validarEdad(data["genero"]):
                myLabel1.config(
                    text="eres menor de edad, no se te permite ingresar")
                root.update()
                estado = 0
                os.system("mpg321 menorEdad.mp3")
                reinicio()
                return
            reg = model.insertUsuario(data)
            resultado = {
                "id_usuario": reg,
                "permiso": data["permiso"]
            }
        if resultado["permiso"] == 0 and validarFecha(data["documento"]):
            myLabel1.config(
                text="Lo sentimos.\nHoy no tienes permitido ingresar.\nTe esperamos mañana")
            root.update()
            estado = 0
            os.system("mpg321 diaNoIngreso.mp3")
            reinicio()
            return

        myLabel1.config(text=getTexto(data["genero"], data["nombres"]))
        root.update()
        decirIntro(data["genero"])
        temp = temperatura.temp()
        myLabel1.config(text="Su temperatura es: " + str(temp) + "℃")
        root.update()
        if temp > 37.5:
            myLabel2.config(text="su temperatura se encuentra muy elevada")
            root.update()
            estado = 0
            os.system("mpg321 temperaturaElevada.mp3")
            reinicio()
            return
        registro = {
            "id_usuario": resultado["id_usuario"],
            "fecha_registro": datetime.datetime.today(),
            "temperatura": temp
        }
        model.insertRegistro(registro)
        myLabel2.config(text="Bienvenido")
        root.update()
        decirBienvenida(data["genero"])

        estado = 0
        reinicio()


button = tk.Button(root, command=evento)
button.grid(row=1, column=2)
root.bind('<Return>', lambda event=None: button.invoke())
root.mainloop()
