import mariadb
class AperturasDB():
    def __init__(self,pool):
        self.pool = pool

    def insertarApertura(self,idUsuario,fechaApertura,fechaCierre):
        con = self.pool.get_connection()
        cur = con.cursor()
        sql  = "INSERT INTO aperturas_local (fechaApertura,fechaCierre) values (?,?);"
        cur.execute(sql,(fechaApertura,fechaCierre))
        idApertura =  cur.lastrowid
        sql = "INSERT INTO usuarios_aperturas values (?,?);"
        cur.execute(sql,(idUsuario,idApertura));
        con.commit();
        con.close() 
        
    
        
