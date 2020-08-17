import tkinter as tk
import time
import datetime
import sqlite3
import sensorLibD6T as temperatura
import psutil
import os
from gtts import gTTS

def delPubDocumento(documento):
    if "PubDSK_1"in documento:
        return documento[8:]
    return documento

datos=""
while(True):

    datos=input("escane su documento\n")
    print(len(datos))
    conn = sqlite3.connect('/home/pi/Documents/proyectos/proyectoSL/db/tablas.db')


    texto=datos.split("-")
    documento = delPubDocumento(texto[0])	
    nombres = texto[3]+ " " + texto[4]
    apellidos = texto[1]+ " " + texto[2]
    generoL= texto[5]
    fecha_nacimento=texto[6]

    c = conn.cursor()
    query= "select id_usuario, permiso from usuario where documento = ?"
    c.execute(query,(documento,))
    result = c.fetchone()
    agregado= False
    if result is None:
        query= "insert into usuario (documento, nombres, apellidos, genero, fecha_nacimiento, permiso) values (?, ?, ?, ?, ?,1)"
        c.execute(query, (documento, nombres, apellidos, generoL, fecha_nacimento))
        conn.commit()
        c.execute("select id_usuario from usuario where documento = ?",(documento,))
        result = c.fetchone()
        if result is None:
            print("no se ha agregado, intente de nuevo");
        else:
            print("se agrego correctamente")
    else:
        print("su usuario ya ha sido registrado")
    conn.close()




