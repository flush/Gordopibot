from  datetime import datetime
from usuariosBO import Usuario
from flujoComun import ResultadoApuntar
import traceback


class AperturasDB():
    def __init__(self, pool,aforo):
        self.pool = pool
        self.aforo = aforo

    def insertarApertura(self, idUsuario, fechaApertura, fechaCierre):
        con = self.pool.get_connection()
        try:
            cur = con.cursor()
            sql = "INSERT INTO aperturas_local (fechaApertura,fechaCierre) values (?,?);"
            cur.execute(sql, (fechaApertura, fechaCierre))
            idApertura = cur.lastrowid
            sql = "INSERT INTO usuarios_aperturas values (?,?);"
            cur.execute(sql, (idUsuario, idApertura))
            con.commit()
            return Apertura(idApertura,fechaApertura,fechaCierre)
        except:
            traceback.print_exc()
            return None
        finally:
            con.close()


    def getAperturas(self):
        con = self.pool.get_connection()
        aperturas = []        
        try:
            cur = con.cursor()
            sql = "select id,fechaApertura,fechaCierre from aperturas_local where fechaCierre >= ?"
            cur.execute(sql, (datetime.now(),))
        
            filas = cur.fetchall()
            for fila in filas:
                aperturas.append(Apertura(fila[0], fila[1], fila[2]))

        except:
            traceback.print_exc()
        finally:
            con.close()
        return aperturas


    def getApertura(self,id):
        con = self.pool.get_connection()
        try:
            cur = con.cursor()
            sql = "select id,fechaApertura,fechaCierre from aperturas_local where id = ?"
            cur.execute(sql, (id,))
            apertura = cur.fetchone()
            return Apertura(apertura[0],apertura[1],apertura[2])            
        except:
            traceback.print_exc()
            return None
        finally:
            con.close()


    def apuntarASesion(self,idUsuario, idApertura):
        con = self.pool.get_connection()

        try:
            cur = con.cursor()
            sql = " select * from usuarios_aperturas where idUsuario=? and idApertura = ?"
            cur.execute(sql,(idUsuario,idApertura))
            resultado = None

            if len(cur.fetchall())==0:
                if self.getPlazasLibres(idApertura) > 0:
                    sql = "INSERT INTO usuarios_aperturas (idUsuario,idApertura) values (?,?);"
                    resultado = ResultadoApuntar.OK_SESION
                    cur.execute(sql, (idUsuario, idApertura))
                    con.commit()
                else :
                    resultado = ResultadoApuntar.SIN_AFORO
            else:
                resultado =  ResultadoApuntar.YA_APUNTADO

        except:
            traceback.print_exc()
        finally:
            con.close()
        return  resultado

    def getPlazasLibres(self,idApertura):
        usuarios = self.getUsuariosApuntados(idApertura)
        return self.aforo - len(usuarios)


    def getUsuariosApuntados(self,idApertura):
        con = self.pool.get_connection()
        usuarios = []
        try:
            cur = con.cursor()
            sql = "select usu.* from usuarios usu, usuarios_aperturas usu_aperturas where usu_aperturas.idApertura=? and usu_aperturas.idUsuario=usu.id"
            cur.execute(sql, (idApertura,))
            filas = cur.fetchall()
            for fila in filas:
                usuarios.append(Usuario(fila[0], fila[1], fila[2]))
        except:
            traceback.print_exc()
        finally:
            con.close()
        return usuarios
    def estaUsuarioApuntado(self,idApertura,idUsuario):
        usuarios = self.getUsuariosApuntados(idApertura);
        for usuario in usuarios:
            if usuario.id == idUsuario:
                return True
        return False

class Apertura():
    def __init__(self, id, fechaApertura, fechaCierre):
        self.id = id
        self.fechaApertura = fechaApertura
        self.fechaCierre = fechaCierre


    def toString(self):
           return self.fechaApertura.strftime("%A %d de %B a las %H:%M") + "-" +self.fechaCierre.strftime("%H:%M")
 


   
