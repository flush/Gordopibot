import mariadb
from datetime import datetime, timedelta
class SesionHandler():
    def __init__(self,sesionTimeout):
        self.sesionTimeout = timedelta(minutes=sesionTimeout)
        self.sesiones = []

    #Borra las sesiones que viejas
    def borrarSesionesViejas(self):
        fechaExpiracion = datetime.now() - self.sesionTimeout
        for sesion in self.sesiones:
            if sesion.fechaInicio < fechaExpiracion:
                self.sesiones.remove(sesion);
        
        
            

    #crea una nueva sesion
    def crearSesion(self,usuario):
        #Si existe una sesión anterior, se borrar
        sesion = self.getSesion(usuario.id)
        if sesion:
            self.sesiones.remove(sesion);
        self.sesiones.append(Sesion(usuario));
                
    #Obitene la sesión actual del usuario
    def getSesion(self,id):
        self.borrarSesionesViejas();
        for sesion in self.sesiones:
            if sesion.usuario.id == id:
                return sesion
        
class Sesion():

    def __init__(self,usuario):
        self.usuario = usuario;
        self.fechaInicio = datetime.now()
        #self.fechaInicioApertura
        #self.fechaFinApertura
        
        
        


