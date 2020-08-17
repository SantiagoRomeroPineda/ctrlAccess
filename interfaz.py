import tkinter as tk
import time
import datetime
import sqlite3
import sensorLibD6T as temperatura
import audios as audios
import psutil
import os
import RPi.GPIO as GPIO


#pulsadores config
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

estado=0
root = tk.Tk()
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


def delPubDocumento(documento):
    if "PubDSK_1"in documento:
        return documento[8:]
    return documento

#guardarAudios()
def hablar(frase):
    myobj = gTTS(text=frase, lang="es", slow=False)
    myobj.save("frase.mp3")
    os.system("mpg321 frase.mp3")



def cambio():
    global estado

    dt = datetime.datetime.today()
    dia= dt.day%2 == 0
    if estado==0:
        estado=1
        texto=entry.get().split('-')
        pulsador=GPIO.input(18)==0 or GPIO.input(16)==0
        izquierda=GPIO.input(18)
        derecha=GPIO.input(16)


        menor=False
        if texto[5]=='0':
            menor=True
        if menor==False:
            documento = delPubDocumento(texto[0])	
            nombres = texto[3]+ " " + texto[4]
            apellidos = texto[1]+ " " + texto[2]
            generoL= texto[5]
            fecha_nacimento=texto[6]
            fecha_entrada = datetime.datetime.now()

            genero= "señor "
            bienvenida="Bienvenido "
            print(texto)
            if texto[5]=="F":
                genero="señora "
                bienvenida="Bienvenida "
            conn = sqlite3.connect('/home/pi/Documents/proyectos/proyectoSL/db/tablas.db')


            c = conn.cursor()
            query= "select id_usuario, permiso from usuario where documento = ?"
            c.execute(query,(documento,))
            result = c.fetchone()
            permiso= False
            if result is not None:
                if derecha==0:

                    query= "update usuario set permiso = 1 where documento =?"
                    c.execute(query,(documento,))
                    conn.commit()
                    print("derecha")
                if izquierda==0:

                    query= "update usuario set permiso = 2 where documento =?"
                    c.execute(query,(documento,))
                    conn.commit()
                    print("izquierda")
                if result[1]==1 or result[1]==2 :
                    permiso=True


            if (dia != (int(texto[0][-1])%2 == 0)) or permiso or pulsador :

                myLabel1.config(text=bienvenida+genero+texto[3]+"\nPor favor acérquese al sensor")
                entry.delete(0,"end")
                root.update()
                if texto[5]=="F":
                    os.system("mpg321 introMujer.mp3")
                else:
                    os.system("mpg321 introHombre.mp3")
                temp=temperatura.temp()
                myLabel1.config(text="Su temperatura es: "+ str(temp)+ "℃")
                if temp<37.5:
                    valido= False
                    if result is not None:
                        id_usuario= result[0]
                        query= "insert into registro (id_usuario, fecha_registro, temperatura) values (?, ?, ?)"
                        c.execute(query, (id_usuario,str(fecha_entrada), temp ))
                        conn.commit()
                        valido=True
                    else:
                        #pulsador izquierda
                        if izquierda==0:
                            query= "insert into usuario (documento, nombres, apellidos, genero, fecha_nacimiento, permiso) values (?, ?, ?, ?, ?, 2)"
                        elif derecha==0:
                            query= "insert into usuario (documento, nombres, apellidos, genero, fecha_nacimiento, permiso) values (?, ?, ?, ?, ?, 1)"
                        else:
                            query= "insert into usuario (documento, nombres, apellidos, genero, fecha_nacimiento, permiso) values (?, ?, ?, ?, ?, 0)"

                        c.execute(query, (documento, nombres, apellidos, generoL, fecha_nacimento))
                        conn.commit()
                        c.execute("select id_usuario from usuario where documento = ?",(documento,))
                        result = c.fetchone()
                        if result is not None:
                            id_usuario= result[0]
                            query= "insert into registro (id_usuario, fecha_registro, temperatura) values (?, ?, ?)"
                            c.execute(query, (id_usuario,str(fecha_entrada), temp ))
                            conn.commit()
                            valido = True
                    conn.close()
                    if valido:
                        myLabel2.config(text="Bienvenido")
                        root.update()
                        frase = "Su temperatura es: "+ str(temp)+", "+ bienvenida
                        if texto[5]=="F":
                            os.system("mpg321 bienvenida.mp3")
                        else:
                            os.system("mpg321 bienvenido.mp3")
                    else:
                        frase= "por favor intente de nuevo"
                        myLabel2.config(text="intente de nuevo")
                        root.update()
                        hablar(frase)
                else:
                    #temperatura es elevada
                    myLabel2.config(text="su temperatura está elevada\nNo tiene permitido el ingreso")
                    root.update()
                    os.system("mpg321 temperaturaElevada.mp3")

            else:
                #no se puede ingresar
                myLabel1.config(text="Lo sentimos\nHoy no tienes permitido ingresar\nTe esperamos mañana")
                entry.delete(0,"end")
                root.update()
                os.system("mpg321 diaNoIngreso.mp3")

        else:
            #menor de edad
            myLabel1.config(text="eres menor de edad, no se te permite ingresar")
            entry.delete(0,"end")
            root.update()
            os.system("mpg321 menorEdad.mp3")
        estado=0
        entry.delete(0,"end")
        texto="Bienvenido.\nPor favor presente su documento en el lector"
        myLabel1.config(text=texto )
        myLabel2.config(text="")
        root.update()







button= tk.Button(root, command=cambio)
button.grid(row=1, column=2)
root.bind('<Return>', lambda event=None: button.invoke())



root.mainloop()