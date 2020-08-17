import sqlite3

class Modelo(object):
    def __init__(self):
        self.conn= sqlite3.connect('/run/user/1000/gvfs/sftp:host=192.168.0.26,user=pi/home/pi/Documents/proyectos/proyectoSL/db/tablas.db')
        self.conn.row_factory= sqlite3.Row

    def closeConection(self):
        self.conn.close()

    def query(self, sql, parametros=(), tipo=False):
        c = self.conn.cursor()
        c.execute(sql,parametros)
        if tipo:
            return dict(c.fetchall()[0])
        self.conn.commit() 

    def getUsuario(self, documento):
         sql= "select id_usuario, permiso from usuario where documento = ?"
         parametros=(documento,)
         return self.query(sql,parametros,True)
    
    def insertUsuario(self,data):
        sql= "insert into usuario (documento, nombres, apellidos, genero, fecha_nacimiento, permiso) values (?, ?, ?, ?, ?, ?)"
        parametros=(data["documento"],data["nombres"],data["apellidos"],data["genero"],data["fecha_nacimiento"],data["permiso"],)
        self.query(sql,parametros)

    def updateUsuario(self, data):
        sql= "update usuario set permiso = ? where documento =?"
        paramteros=(data["documento"],data["permiso"],)
        self.query(sql,paramteros)
    
    def insertRegistro(self, data):
        sql= "insert into registro (id_usuario, fecha_registro, temperatura) values (?, ?, ?)"
        parametros= (data["id_usuario"],data["fecha_registro"],data["temperatura"],)
        self.query(sql, parametros)




