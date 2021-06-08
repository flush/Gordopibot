from telebot import types

import config
import botones
import flujoAltaUsuario
import flujoApertura
import flujoComun
#Start handler
@config.bot.message_handler(commands=['jugar'])
def jugar(message):
    usuario = config.usuarioDB.getUsuario(message.from_user.id);
    if not usuario and not grupoAutorizado(message.chat.id):
        markup  = types.InlineKeyboardMarkup()
        texto="""Lo siento, no estás en un grupo autorizado."""
        config.bot.send_message(message.chat.id, text=texto, reply_markup=markup)
    else:
        if not usuario:
            markup  = types.InlineKeyboardMarkup()
            texto = config.mensajes["darse_de_alta"]
            markup.add(botones.getBoton("alta_usuario"))
            markup.add(botones.getBoton("cancelar"))
            config.bot.send_message(message.chat.id, text=texto, reply_markup=markup)
        else:
            flujoComun.dialogo_inicial(message.chat.id,usuario)

    
@config.bot.callback_query_handler(lambda call: call.data == "cancelar")
def adios (call):
    config.bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id,text=config.mensajes["adios"],reply_markup= types.InlineKeyboardMarkup())
    

config.bot.polling()
