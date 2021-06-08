

class UsuarioDB():
    def __init__(self, pool):

        self.pool = pool

    def insertarUsuario(self, id, nombre, categoria):
        con = self.pool.get_connection()
        cur = con.cursor()
        sql = "INSERT INTO usuarios values (?,?,?);"
        cur.execute(sql, (id, nombre, categoria))
        con.commit()
        con.close()
        return Usuario(id, nombre, categoria)
    
    def getUsuario(self, id):
        con = self.pool.get_connection()
        cur = con.cursor()
        sql = "SELECT * FROM usuarios WHERE id = %s"
        cur.execute(sql, (id,))
        usuario = cur.fetchone()
        con.close()
        if usuario:
            return Usuario(usuario[0], usuario[1], usuario[2])
        else:
            return

       
class Usuario():
    def __init__(self, id, nombre, categoria):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
