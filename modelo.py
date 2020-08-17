import sqlite3

class Modelo(object):
    def __init__(self):
        self.conn= sqlite3.connect('/home/pi/Documents/proyectos/proyectoSL/db/tablas.db')

    def closeConection(self):
        self.conn.close()

    def getUsuario(self, documento):
        c = self.conn.cursor()
        query= "select id_usuario, permiso from usuario where documento = ?"
        c.execute(query,(documento,))

        return (c.fetchone())



