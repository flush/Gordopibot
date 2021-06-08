import config
import botones
def dialogo_inicial(chatId, usuario):

    #Se crea la sesión y se manda el dialogo inicial
    config.sesionHandler.crearSesion(usuario);
    markup  = botones.getTeclado("ir_local","unirse_partida","crear_partida")
    texto = config.mensajes["saludo"].format(nombreUsuario = usuario.nombre)
    if usuario.categoria == "SP" or usuario.categoria == "AD":
        markup.add(botones.getBoton("abrir_local"))

    config.bot.send_message(chatId, text=texto, reply_markup=markup)
