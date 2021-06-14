import config
import botones
from enum import Enum
def dialogo_inicial(chatId, usuario):

    #Se crea la sesión y se manda el dialogo inicial
    config.sesionHandler.crearSesion(usuario);
    markup  = botones.getTeclado("unirse_partida","crear_partida","que_se_cuece","ir_local")
    texto = config.mensajes["saludo"].format(nombreUsuario = usuario.nombre)
    if usuario.categoria == "SP" or usuario.categoria == "AD":
        markup.add(botones.getBoton("abrir_local"))

    config.bot.send_message(chatId, text=texto, reply_markup=markup)



class ResultadoApuntar(Enum):
    OK_PARTIDA = "apuntado_partida"
    YA_APUNTADO = "ya_apuntado"
    ROBO_PLAZA = "robo_plaza"
    SIN_AFORO = "sin_aforo"
    OK_SESION = "apuntado_sesion"
