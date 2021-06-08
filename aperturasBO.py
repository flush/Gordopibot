from  datetime import datetime


class AperturasDB():
    def __init__(self, pool):
        self.pool = pool

    def insertarApertura(self, idUsuario, fechaApertura, fechaCierre):
        con = self.pool.get_connection()
        cur = con.cursor()
        sql = "INSERT INTO aperturas_local (fechaApertura,fechaCierre) values (?,?);"
        cur.execute(sql, (fechaApertura, fechaCierre))
        idApertura = cur.lastrowid
        sql = "INSERT INTO usuarios_aperturas values (?,?);"
        cur.execute(sql, (idUsuario, idApertura))
        con.commit()
        con.close()

    def getAperturas(self):
        con = self.pool.get_connection()
        cur = con.cursor()
        sql = "select id,fechaApertura,fechaCierre from aperturas_local where fechaCierre >= ?"
        cur.execute(sql, (datetime.now(),))
        filas = cur.fetchall()
        aperturas = []
        for fila in filas:
            aperturas.append(Apertura(fila[0], fila[1], fila[2]))
        return aperturas
        con.close()


class Apertura():
    def __init__(self, id, fechaApertura, fechaCierre):
        self.id = id
        self.fechaApertura = fechaApertura
        self.fechaCierre = fechaCierre


   
