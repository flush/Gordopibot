from  datetime import datetime,timedelta
from usuariosBO import Usuario
from flujoComun import ResultadoApuntar
import config
import traceback



class PartidasDB():
    def __init__(self, pool):
        self.pool = pool

    def insertarPartida(self, partida):
        con = self.pool.get_connection()
        cur = None
        try:
            cur = con.cursor()
            sql = "INSERT INTO partidas (fecha,nombreJuego,idJuego,idApertura,idCreador,plazas) values (?,?,?,?,?,?);"
            cur.execute(sql, ( partida.fecha,partida.nombreJuego,partida.idJuego,partida.idApertura, partida.idCreador, partida.plazas))
            idPartida = cur.lastrowid
            partida.id = cur.lastrowid            
            con.commit()
        except:
            traceback.print_exc()
            con.rollback()
        finally:
            cur.close()
            con.close()
        return partida
    

    def apuntarAPartida(self,idUsuario, idPartida):
        con = self.pool.get_connection()
        cur = None
        try:

            resultado = None
            partida = self.getPartida(idPartida)
            if config.aperturaDB.getPlazasLibres(partida.idApertura) > 0 or config.aperturaDB.estaUsuarioApuntado(partida.idApertura,idUsuario):
                if self.getPlazasLibres(idPartida) > 0:
                    cur = con.cursor()
                    sql = " select * from usuarios_partidas where idUsuario=? and idPartida = ?"
                    cur.execute(sql,(idUsuario,idPartida))
                    if len(cur.fetchall())==0:
                        sql = "INSERT INTO usuarios_partidas (idUsuario,idPartida) values (?,?);"
                        cur.execute(sql, (idUsuario, idPartida))
                        con.commit()
                        partida = self.getPartida(idPartida)
                        config.aperturaDB.apuntarASesion(idUsuario,partida.idApertura)
                        resultado = ResultadoApuntar.OK_PARTIDA
                    else:
                        resultado = ResultadoApuntar.YA_APUNTADO
                else:
                    resultado =  ResultadoApuntar.ROBO_PLAZA
            else:
                resultado =  ResultadoApuntar.SIN_AFORO
        except:
            traceback.print_exc()
            con.rollback()
        finally:
            cur.close()
            con.close()
        return resultado
    def getPartidas(self):
        con = self.pool.get_connection()
        cur = None
        partidas = []
        try:
            cur = con.cursor()
            sql = "select * from partidas where fecha >= ? "
            cur.execute(sql, (datetime.now()+timedelta(minutes=30),))
            filas = cur.fetchall()
            for fila in filas:
                partidas.append(Partida(fila[0], fila[1], fila[2],fila[3],fila[4],fila[5],fila[6]))
        except:
            traceback.print_exc()
        finally:
            cur.close()
            con.close()            
        return partidas

    def getPartida(self,id):
        con = self.pool.get_connection()
        cur = None
        fila = None
        try:
            cur = con.cursor()
            sql = "select * from partidas where id =?"
            cur.execute(sql, (id,))
            fila = cur.fetchone()

        except:
            traceback.print_exc()
        finally:
            cur.close()
            con.close()
        return Partida(fila[0], fila[1], fila[2],fila[3],fila[4],fila[5],fila[6])

    def getUsuariosApuntados(self,idPartida):
        con = self.pool.get_connection()
        usuarios=[]
        cur = None
        try:
            cur = con.cursor()
            sql = "select usu.* from usuarios usu, usuarios_partidas usu_partidas where usu_partidas.idPartida=? and usu_partidas.idUsuario=usu.id"
            cur.execute(sql, (idPartida,))
            filas = cur.fetchall()
            for fila in filas:
                usuarios.append(Usuario(fila[0], fila[1], fila[2]))
        except:
            traceback.print_exc()
        finally:
            cur.close()
            con.close()            
        return usuarios

    def getPlazasLibres(self,idPartida):
        partida = self.getPartida(idPartida)
        usuarios = self.getUsuariosApuntados(idPartida);
        return partida.plazas-len(usuarios)

        


class Partida():

    def __init__(self,id, fecha,nombreJuego,idJuego,idApertura, idCreador, plazas):
        self.id = id
        self.fecha = fecha
        self.nombreJuego = nombreJuego
        self.idJuego = idJuego
        self.idApertura = idApertura
        self.idCreador = idCreador
        self.plazas = plazas

    def toString(self):
           return self.nombreJuego + " " +self.fecha.strftime("%A %d de %B a las %H:%M")+". " + str(config.partidasDB.getPlazasLibres(self.id))  +"plazas."

    def getUrlBGGJuego(self):
        return "https://boardgamegeek.com/boardgame/"+str(self.idJuego)
    def resumen(self):
           return '<a href="'+self.getUrlBGGJuego() +'">'+ self.nombreJuego + "</a> " +self.fecha.strftime("%H:%M")+". " + str(config.partidasDB.getPlazasLibres(self.id))  +"plazas."


















